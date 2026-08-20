"""Generic interactive StepScreen with side-by-side cluster selection, Region info, conditional GKE Private GA agreement, and WorkerPool setup."""

from __future__ import annotations

import asyncio
from typing import List, Optional
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Label, Static, Button
from rich.text import Text
from substrate_onboarding.config import (
    OnboardingStep,
    STEP_CONFIGS,
    AVAILABLE_CLUSTERS,
    NODEPOOL_OPTIONS,
    AUTOSCALING_OPTIONS,
    DEPLOY_WP_OPTIONS,
    OptionItem,
    StepMetadata,
)
from substrate_onboarding.widgets.status_bar import TopHeader, BottomBar
from substrate_onboarding.widgets.sidebar_nav import SidebarNav


class GenericStepScreen(Screen[None]):
    """Generic high-fidelity step screen rendering 2-column layout with options, probe checklists, region info, and YAML notices."""

    selected_option_idx: reactive[int] = reactive(0)

    BINDINGS = [
        ("enter", "proceed_next", "Proceed"),
        ("space", "proceed_next", "Proceed"),
        ("b", "previous_step", "Back"),
        ("a", "toggle_agreement", "Acknowledge"),
        ("1", "select_opt_1", "Select 1"),
        ("2", "select_opt_2", "Select 2"),
        ("3", "select_opt_3", "Select 3"),
        ("4", "select_opt_4", "Select 4"),
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
        self.nodepool_opts = NODEPOOL_OPTIONS
        self.autoscaling_opts = AUTOSCALING_OPTIONS
        self.deploy_wp_opts = DEPLOY_WP_OPTIONS
        self.gke_agreement_accepted = True
        self._checklist_progress = 0
        self._timer = None

    def compose(self) -> ComposeResult:
        yield TopHeader(initial_step=self.step_key)
        with Horizontal(id="workspace-layout"):
            yield SidebarNav(current_step=self.step_key)
            with Vertical(id="content-area"):
                with Vertical(id="content-panel"):
                    # Step Number & Title
                    yield Label(f"Step {self.meta.step_num} of 11", classes="step-indicator-label")
                    yield Label(self.meta.heading, classes="wizard-step-title")
                    yield Label(self.meta.description, classes="wizard-step-description")

                    # Step 2: Side-by-side Cluster Selection with Region & Conditional GKE Private GA Agreement
                    if self.step_key == OnboardingStep.CONNECT_CLUSTER:
                        with Horizontal(id="cluster-side-by-side-layout"):
                            # Left Column: Cluster List (with Region info)
                            with Vertical(id="cluster-picker-column"):
                                yield Label("Select target cluster (Press [1-4]):", classes="column-header-label")
                                for idx in range(len(self.clusters)):
                                    yield Static(
                                        self._render_cluster_row(idx),
                                        id=f"cluster-item-{idx}",
                                        classes="compact-cluster-card",
                                    )

                            # Right Column: Cluster Type, Region & Substrate Probe Verification
                            with Vertical(id="cluster-inspection-column"):
                                yield Label("Cluster Type & Substrate Probe:", classes="column-header-label")
                                yield Static(self._render_cluster_verification_box(), id="cluster-verification-box")
                                yield Static(self._render_gke_agreement_box(), id="cluster-gke-agreement-box")
                                yield Static(self._render_compact_checklist(), id="cluster-compact-checklist")

                    elif self.step_key == OnboardingStep.COMPATIBLE_NODEPOOL:
                        # Step 4: Compatible Node Pool (CCC Selection)
                        yield Label("Choose node pool configuration (Press [1-3]):", classes="column-header-label")
                        with Vertical(id="nodepool-options-list"):
                            for idx in range(len(self.nodepool_opts)):
                                yield Static(
                                    self._render_option_card(self.nodepool_opts, idx),
                                    id=f"nodepool-opt-{idx}",
                                    classes="compact-cluster-card",
                                )
                        if self.meta.yaml_notice:
                            yield Static(self._render_yaml_notice(), id="yaml-notice-box")
                        yield Static(self._render_checklist_box(), id="execution-checklist-card")

                    elif self.step_key == OnboardingStep.CONFIG_AUTOSCALING:
                        # Step 5: WorkerPool Autoscaling (HPA & CapacityBuffer)
                        yield Label("Choose autoscaling configuration (Press [1-3]):", classes="column-header-label")
                        with Vertical(id="autoscaling-options-list"):
                            for idx in range(len(self.autoscaling_opts)):
                                yield Static(
                                    self._render_option_card(self.autoscaling_opts, idx),
                                    id=f"autoscaling-opt-{idx}",
                                    classes="compact-cluster-card",
                                )
                        if self.meta.yaml_notice:
                            yield Static(self._render_yaml_notice(), id="yaml-notice-box")
                        yield Static(self._render_checklist_box(), id="execution-checklist-card")

                    elif self.step_key == OnboardingStep.DEPLOY_WORKERPOOL:
                        # Step 6: Confirm & Deploy WorkerPool
                        yield Label("Deploy default Substrate WorkerPool (Press [1-2]):", classes="column-header-label")
                        with Vertical(id="deploy-wp-options-list"):
                            for idx in range(len(self.deploy_wp_opts)):
                                yield Static(
                                    self._render_option_card(self.deploy_wp_opts, idx),
                                    id=f"deploy-wp-opt-{idx}",
                                    classes="compact-cluster-card",
                                )
                        yield Static(self._render_checklist_box(), id="execution-checklist-card")

                    else:
                        # Other steps: Sleek command callout
                        yield Static(self._render_command_callout(), id="command-callout-card")

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
                if self.step_key == OnboardingStep.CONNECT_CLUSTER:
                    box = self.query_one("#cluster-compact-checklist", Static)
                    box.update(self._render_compact_checklist())
                else:
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
        t.append(f"  {self.meta.real_command}", style="#70d6ff")
        return t

    def _render_yaml_notice(self) -> Text:
        t = Text()
        t.append("💡 Note: ", style="bold #fdd663")
        t.append(self.meta.yaml_notice or "", style="#e3e3e3")
        return t

    def _render_cluster_row(self, idx: int) -> Text:
        cluster = self.clusters[idx]
        is_selected = idx == self.selected_option_idx
        t = Text()

        keycap = f" [{idx + 1}] "
        if is_selected:
            t.append(f" ▶ {keycap}", style="bold #ffffff on #1565c0")
            t.append(f" {cluster.icon} {cluster.title[:38]}\n", style="bold #70d6ff on #1565c0")
            t.append(f"        Region: {cluster.region} • {cluster.nodes} nodes", style="#e3e3e3 on #1565c0")
        else:
            t.append(f" ○ {keycap}", style="#80868b")
            t.append(f" {cluster.icon} {cluster.title[:38]}\n", style="bold #e3e3e3")
            t.append(f"        Region: {cluster.region} • {cluster.nodes} nodes", style="#80868b")

        return t

    def _render_option_card(self, opt_list: List[OptionItem], idx: int) -> Text:
        opt = opt_list[idx]
        is_selected = idx == self.selected_option_idx
        t = Text()

        keycap = f" [{idx + 1}] "
        if is_selected:
            t.append(f" ▶ {keycap}", style="bold #ffffff on #1565c0")
            t.append(f" {opt.icon} {opt.title}\n", style="bold #70d6ff on #1565c0")
            t.append(f"        {opt.description}\n", style="#e3e3e3 on #1565c0")
            t.append(f"        💡 {opt.tip}", style="italic #81c995 on #1565c0")
        else:
            t.append(f" ○ {keycap}", style="#80868b")
            t.append(f" {opt.icon} {opt.title}\n", style="bold #e3e3e3")
            t.append(f"        {opt.description}\n", style="#80868b")
            t.append(f"        💡 {opt.tip}", style="italic #5f6368")

        return t

    def _render_cluster_verification_box(self) -> Text:
        cluster = self.clusters[self.selected_option_idx if self.selected_option_idx < len(self.clusters) else 0]
        t = Text()
        t.append("🌐 CLUSTER VERIFICATION:\n", style="bold #70d6ff")
        t.append(f"  Provider : {cluster.provider}\n", style="bold #ffffff")
        t.append(f"  Region   : {cluster.region}\n", style="bold #8ab4f8")
        t.append(f"  Nodes    : {cluster.nodes} ready (KVM / microVM enabled)\n", style="#81c995")
        t.append(f"  Probe    : [substrate-system] ➔ {cluster.control_plane_status}", style="bold #fdd663")
        return t

    def _render_gke_agreement_box(self) -> Text:
        cluster = self.clusters[self.selected_option_idx if self.selected_option_idx < len(self.clusters) else 0]
        t = Text()
        if cluster.is_gke:
            t.append("📝 PRIVATE GA GATED ACKNOWLEDGMENT (GKE ONLY):\n", style="bold #fdd663")
            t.append("  • Org: Acme Corp  │  Token: ga-sub-8f92a [Verified ✓]\n", style="#e3e3e3")
            if self.gke_agreement_accepted:
                t.append("  [✓] I acknowledge production support requires an explicit agreement with Google. [Accepted]", style="bold #70d6ff")
            else:
                t.append("  [ ] Press [a] to accept Google Cloud Private GA support agreement", style="bold #fdd663")
        return t

    def _render_compact_checklist(self) -> Text:
        t = Text()
        t.append("⚡ PROBE CHECKLIST:\n", style="bold #70d6ff")
        for i, item in enumerate(self.meta.checklist_items):
            if i < self._checklist_progress:
                t.append("  ✓ ", style="bold #81c995")
                t.append(f"{item}\n", style="#ffffff")
            elif i == self._checklist_progress:
                t.append("  ⠋ ", style="bold #70d6ff")
                t.append(f"{item}\n", style="#70d6ff")
            else:
                t.append("  ○ ", style="#5f6368")
                t.append(f"{item}\n", style="#5f6368")
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

    def action_select_opt_1(self) -> None:
        self.selected_option_idx = 0
        self._refresh_screen_options()

    def action_select_opt_2(self) -> None:
        self.selected_option_idx = 1
        self._refresh_screen_options()

    def action_select_opt_3(self) -> None:
        self.selected_option_idx = 2
        self._refresh_screen_options()

    def action_select_opt_4(self) -> None:
        self.selected_option_idx = 3
        self._refresh_screen_options()

    def action_toggle_agreement(self) -> None:
        if self.step_key == OnboardingStep.CONNECT_CLUSTER:
            self.gke_agreement_accepted = not self.gke_agreement_accepted
            try:
                gke_box = self.query_one("#cluster-gke-agreement-box", Static)
                gke_box.update(self._render_gke_agreement_box())
            except Exception:
                pass

    def action_navigate_up(self) -> None:
        if self.selected_option_idx > 0:
            self.selected_option_idx -= 1
            self._refresh_screen_options()

    def action_navigate_down(self) -> None:
        max_len = 4
        if self.step_key == OnboardingStep.CONNECT_CLUSTER:
            max_len = len(self.clusters)
        elif self.step_key == OnboardingStep.COMPATIBLE_NODEPOOL:
            max_len = len(self.nodepool_opts)
        elif self.step_key == OnboardingStep.CONFIG_AUTOSCALING:
            max_len = len(self.autoscaling_opts)
        elif self.step_key == OnboardingStep.DEPLOY_WORKERPOOL:
            max_len = len(self.deploy_wp_opts)

        if self.selected_option_idx < max_len - 1:
            self.selected_option_idx += 1
            self._refresh_screen_options()

    def _refresh_screen_options(self) -> None:
        if self.step_key == OnboardingStep.CONNECT_CLUSTER:
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
            try:
                gke_box = self.query_one("#cluster-gke-agreement-box", Static)
                gke_box.update(self._render_gke_agreement_box())
            except Exception:
                pass
        elif self.step_key == OnboardingStep.COMPATIBLE_NODEPOOL:
            for idx in range(len(self.nodepool_opts)):
                try:
                    row = self.query_one(f"#nodepool-opt-{idx}", Static)
                    row.update(self._render_option_card(self.nodepool_opts, idx))
                except Exception:
                    pass
        elif self.step_key == OnboardingStep.CONFIG_AUTOSCALING:
            for idx in range(len(self.autoscaling_opts)):
                try:
                    row = self.query_one(f"#autoscaling-opt-{idx}", Static)
                    row.update(self._render_option_card(self.autoscaling_opts, idx))
                except Exception:
                    pass
        elif self.step_key == OnboardingStep.DEPLOY_WORKERPOOL:
            for idx in range(len(self.deploy_wp_opts)):
                try:
                    row = self.query_one(f"#deploy-wp-opt-{idx}", Static)
                    row.update(self._render_option_card(self.deploy_wp_opts, idx))
                except Exception:
                    pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-proceed":
            self.action_proceed_next()
        elif event.button.id == "btn-back":
            self.action_previous_step()
