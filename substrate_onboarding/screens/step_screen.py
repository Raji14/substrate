"""Generic interactive StepScreen with cluster selection, control plane probe, and generous whitespace."""

from __future__ import annotations

import asyncio
from typing import Optional
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Label, Static, Button
from rich.text import Text
from substrate_onboarding.config import OnboardingStep, STEP_CONFIGS, AVAILABLE_CLUSTERS, StepMetadata
from substrate_onboarding.widgets.status_bar import TopHeader, BottomBar
from substrate_onboarding.widgets.sidebar_nav import SidebarNav


class GenericStepScreen(Screen[None]):
    """Generic high-fidelity step screen rendering 2-column layout with generous whitespace and cluster verification."""

    selected_cluster_idx: reactive[int] = reactive(0)

    BINDINGS = [
        ("enter", "proceed_next", "Proceed"),
        ("space", "proceed_next", "Proceed"),
        ("b", "previous_step", "Back"),
        ("1", "select_cluster_1", "Select Cluster 1"),
        ("2", "select_cluster_2", "Select Cluster 2"),
        ("3", "select_cluster_3", "Select Cluster 3"),
        ("4", "select_cluster_4", "Select Cluster 4"),
        ("up", "navigate_up", "Previous"),
        ("down", "navigate_down", "Next"),
        ("k", "navigate_up", "Previous"),
        ("j", "navigate_down", "Next"),
    ]

    def __init__(self, step_key: OnboardingStep, name: Optional[str] = None):
        screen_name = name or step_key.value
        super().__init__(name=screen_name)
        self.step_key = step_key
        self.meta: StepMetadata = STEP_CONFIGS[step_key]
        self.clusters = AVAILABLE_CLUSTERS
        self._checklist_progress = 0
        self._timer = None

    def compose(self) -> ComposeResult:
        yield TopHeader(initial_step=self.step_key)
        with Horizontal(id="workspace-layout"):
            yield SidebarNav(current_step=self.step_key)
            with Vertical(id="content-area"):
                with Vertical(id="content-panel"):
                    # Step Number & Title
                    yield Label(f"Step {self.meta.step_num} of 9", classes="step-indicator-label")
                    yield Label(self.meta.heading, classes="wizard-step-title")
                    yield Label(self.meta.description, classes="wizard-step-description")

                    # Real Command Callout Card
                    yield Static(self._render_command_callout(), id="command-callout-card")

                    # Interactive Cluster Selection & Verification (Step 2)
                    if self.step_key == OnboardingStep.CONNECT_CLUSTER:
                        yield Label("Select target cluster from kubeconfig (Press [1-4]):", classes="section-subtitle-label")
                        with Vertical(id="cluster-selection-list"):
                            for idx in range(len(self.clusters)):
                                yield Static(self._render_cluster_row(idx), id=f"cluster-item-{idx}", classes="cluster-option-row")
                        yield Static(self._render_cluster_verification_box(), id="cluster-verification-box")

                    # Specialized Interactive Box (Private GA Agreement)
                    elif self.step_key == OnboardingStep.PRIVATE_GA_AGREEMENT:
                        yield Static(self._render_agreement_box(), id="agreement-card")

                    # Live Execution Checklist Card
                    yield Static(self._render_checklist_box(), id="execution-checklist-card")

                    # Persistent Visualization Card (Benchmark or Live Fleet Table)
                    if self.meta.benchmark_text:
                        yield Static(self._render_benchmark_card(), id="benchmark-visualization-card")
                    elif self.step_key == OnboardingStep.SCALE_UP:
                        yield Static(self._render_fleet_table(), id="fleet-visualization-card")

                    # Action Button Row with tactile keycap badges
                    with Horizontal(classes="action-button-row"):
                        btn_back = Button("← Back [b]", id="btn-back", classes="secondary-button")
                        btn_back.can_focus = False
                        yield btn_back

                        btn_proceed = Button(
                            self.meta.next_action_label,
                            variant="primary",
                            id="btn-proceed",
                            classes="action-button",
                        )
                        btn_proceed.can_focus = False
                        yield btn_proceed

        yield BottomBar(
            initial_tip=self.meta.done_message,
            initial_hints="[1-4] Select  [Enter ↵] Proceed  [b] Back  [/help] Help  [Ctrl+C] Exit",
        )

    def on_mount(self) -> None:
        self._checklist_progress = 0
        self._timer = self.set_interval(0.12, self._tick_checklist)

    def _tick_checklist(self) -> None:
        if self._checklist_progress < len(self.meta.checklist_items):
            self._checklist_progress += 1
            try:
                box = self.query_one("#execution-checklist-card", Static)
                box.update(self._render_checklist_box())
            except Exception:
                pass
        else:
            if self._timer:
                self._timer.stop()

    def _render_command_callout(self) -> Text:
        t = Text()
        t.append(" ▼ Show the real command \n", style="bold #ffffff on #1565c0")
        t.append(f"\n  {self.meta.real_command}", style="#70d6ff")
        return t

    def _render_cluster_row(self, idx: int) -> Text:
        cluster = self.clusters[idx]
        is_selected = idx == self.selected_cluster_idx
        t = Text()

        keycap = f" [{idx + 1}] "
        if is_selected:
            t.append(f" ▶ {keycap}", style="bold #ffffff on #1565c0")
            t.append(f" {cluster.icon}   {cluster.title}\n", style="bold #70d6ff on #1565c0")
            t.append(f"        {cluster.description}\n", style="#e3e3e3 on #1565c0")
            t.append(f"        💡 {cluster.tip}", style="italic #81c995 on #1565c0")
        else:
            t.append(f" ○ {keycap}", style="#80868b")
            t.append(f" {cluster.icon}   {cluster.title}\n", style="bold #e3e3e3")
            t.append(f"        {cluster.description}\n", style="#80868b")
            t.append(f"        💡 {cluster.tip}", style="italic #5f6368")

        return t

    def _render_cluster_verification_box(self) -> Text:
        cluster = self.clusters[self.selected_cluster_idx]
        t = Text()
        t.append("🌐 CLUSTER TYPE & CONTROL PLANE VERIFICATION:\n\n", style="bold #70d6ff")
        t.append(f"  •  Provider Type   :  {cluster.provider} (v1.31 Compatible)  [Verified ✓]\n\n", style="bold #ffffff")
        t.append(f"  •  Node Capacity   :  {cluster.nodes} ready nodes (Hardware virtualization / KVM ready)\n\n", style="#81c995")
        t.append(f"  •  Substrate Probe :  Checked namespace [substrate-system] ➔  {cluster.control_plane_status}", style="bold #fdd663")
        return t

    def _render_agreement_box(self) -> Text:
        t = Text()
        t.append("📝 PRIVATE GA GATED REGISTRATION & CONTRACTUAL AGREEMENT:\n\n", style="bold #fdd663")
        t.append("  •  Customer Org  :  Acme Corporation\n\n", style="bold #ffffff")
        t.append("  •  Contact Email :  rajithal@enterprise.com\n\n", style="#e3e3e3")
        t.append("  •  GA Token      :  ga-sub-8f92a-live-contract  [Verified ✓]\n\n", style="bold #81c995")
        t.append("  [✓] I acknowledge that Agent Substrate is provided under Private GA terms.\n", style="bold #70d6ff")
        t.append("      Production support and enterprise SLAs require an explicit agreement with Google Cloud.", style="italic #80868b")
        return t

    def _render_checklist_box(self) -> Text:
        t = Text()
        t.append(f"{self.meta.checklist_title}\n\n", style="bold #70d6ff")

        for i, item in enumerate(self.meta.checklist_items):
            if i < self._checklist_progress:
                t.append("✓  ", style="bold #81c995")
                t.append(f"{item}\n\n", style="bold #ffffff")
            elif i == self._checklist_progress:
                t.append("⠋  ", style="bold #70d6ff")
                t.append(f"{item}\n\n", style="#70d6ff")
            else:
                t.append("○  ", style="#5f6368")
                t.append(f"{item}\n\n", style="#5f6368")

        if self._checklist_progress >= len(self.meta.checklist_items):
            t.append("Done\n\n", style="bold #81c995")
            t.append(self.meta.done_message, style="#e3e3e3")

        return t

    def _render_benchmark_card(self) -> Text:
        t = Text()
        t.append("⚡ LIVE DATA PLANE BENCHMARK:\n\n", style="bold #70d6ff")
        t.append(f"  {self.meta.benchmark_text}\n", style="bold #81c995")
        return t

    def _render_fleet_table(self) -> Text:
        t = Text()
        t.append("$ atectl get workerpools\n", style="#70d6ff")
        t.append("WORKERPOOL        NAMESPACE         ISOLATION  READY  STANDBY  CPU  MEM  QUEUE\n", style="bold #80868b")
        t.append("production-fleet  substrate-system  microvm    20/20  3        4%   8%   0\n", style="bold #81c995")
        return t

    def action_proceed_next(self) -> None:
        if hasattr(self.app, "advance_step"):
            self.app.advance_step()

    def action_previous_step(self) -> None:
        if hasattr(self.app, "previous_step"):
            self.app.previous_step()

    def action_select_cluster_1(self) -> None:
        if self.step_key == OnboardingStep.CONNECT_CLUSTER:
            self.selected_cluster_idx = 0
            self._refresh_cluster_list()

    def action_select_cluster_2(self) -> None:
        if self.step_key == OnboardingStep.CONNECT_CLUSTER:
            self.selected_cluster_idx = 1
            self._refresh_cluster_list()

    def action_select_cluster_3(self) -> None:
        if self.step_key == OnboardingStep.CONNECT_CLUSTER:
            self.selected_cluster_idx = 2
            self._refresh_cluster_list()

    def action_select_cluster_4(self) -> None:
        if self.step_key == OnboardingStep.CONNECT_CLUSTER:
            self.selected_cluster_idx = 3
            self._refresh_cluster_list()

    def action_navigate_up(self) -> None:
        if self.step_key == OnboardingStep.CONNECT_CLUSTER and self.selected_cluster_idx > 0:
            self.selected_cluster_idx -= 1
            self._refresh_cluster_list()

    def action_navigate_down(self) -> None:
        if self.step_key == OnboardingStep.CONNECT_CLUSTER and self.selected_cluster_idx < len(self.clusters) - 1:
            self.selected_cluster_idx += 1
            self._refresh_cluster_list()

    def _refresh_cluster_list(self) -> None:
        for idx in range(len(self.clusters)):
            try:
                row = self.query_one(f"#cluster-item-{idx}", Static)
                row.update(self._render_cluster_row(idx))
            except Exception:
                pass
        try:
            ver_box = self.query_one("#cluster-verification-box", Static)
            ver_box.update(self._render_cluster_verification_box())
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-proceed":
            self.action_proceed_next()
        elif event.button.id == "btn-back":
            self.action_previous_step()
