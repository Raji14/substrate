"""Step 6: Launchpad & Live Cluster Verification Screen."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Label, Static, Button
from rich.text import Text
from substrate_onboarding.config import OnboardingStep
from substrate_onboarding.widgets.status_bar import TopHeader, BottomBar
from substrate_onboarding.widgets.sidebar_nav import SidebarNav


class SummaryScreen(Screen[None]):
    """Step 6: Launchpad & Live Verification Screen."""

    BINDINGS = [
        ("enter", "finish_onboarding", "Finish & Launch"),
        ("q", "finish_onboarding", "Finish & Launch"),
        ("b", "previous_step", "Back"),
    ]

    def __init__(self, name: str = "launchpad"):
        super().__init__(name=name)

    def compose(self) -> ComposeResult:
        yield TopHeader(initial_step=OnboardingStep.LAUNCHPAD)
        with Horizontal(id="workspace-layout"):
            yield SidebarNav(current_step=OnboardingStep.LAUNCHPAD)
            with Vertical(id="content-area"):
                with Vertical(id="content-panel"):
                    yield Label("[6/6] LAUNCHPAD & LIVE CLUSTER VERIFICATION", classes="wizard-step-title")
                    yield Label(
                        "✔ Agent Substrate on GKE Installation Complete! Cluster [demo-cluster] is ready for agent workloads.",
                        classes="wizard-step-subtitle",
                    )

                    # Live Verification Table
                    yield Static(self._render_verification_card(), id="terminal-log-card")

                    # Runbook Card
                    yield Static(self._render_runbook_card(), id="remedy-card")

                    # Button Row
                    with Horizontal(classes="action-button-row"):
                        btn_back = Button("← Back (b)", id="btn-back", classes="secondary-button")
                        btn_back.can_focus = False
                        yield btn_back

                        btn_finish = Button(
                            "🚀 Finish & Launch CLI (Enter)",
                            variant="primary",
                            id="btn-finish",
                            classes="action-button",
                        )
                        btn_finish.can_focus = False
                        yield btn_finish

        yield BottomBar(
            initial_tip="Agent Substrate installed successfully! Press [Enter] to exit to shell.",
            initial_hints="[Enter] Finish  [b] Back  [/help] Help  [q] Quit",
        )

    def _render_verification_card(self) -> Text:
        t = Text()
        t.append("╭── 📊 LIVE WORKERPOOL READINESS ($ atectl get workerpools) ───────────────────────╮\n", style="bold #8ab4f8")
        t.append("│                                                                                  │\n", style="#8ab4f8")
        t.append("│  ", style="#8ab4f8")
        t.append("WORKERPOOL           NAMESPACE         ISOLATION  READY  STANDBY  CPU  MEM  QUEUE", style="bold #d3e3fd")
        t.append("  │\n", style="#8ab4f8")
        t.append("│  ", style="#8ab4f8")
        t.append("default-worker-pool  substrate-system  microvm    10/10  10       4%   8%   0    ", style="bold #81c995")
        t.append("  │\n", style="#8ab4f8")
        t.append("│                                                                                  │\n", style="#8ab4f8")
        t.append("╰──────────────────────────────────────────────────────────────────────────────────╯", style="bold #8ab4f8")
        return t

    def _render_runbook_card(self) -> Text:
        t = Text()
        t.append("🚀 DAY-0 QUICKSTART RUNBOOK (NEXT STEPS):\n\n", style="bold #81c995")
        t.append("  1. Deploy your first agent session (No-YAML):\n", style="bold #ffffff")
        t.append("     $ atectl actor create my-first-actor --template=default-agent --atespace=default-atespace\n\n", style="bold #8ab4f8")
        t.append("  2. Inspect live standby workers and memory overcommit:\n", style="bold #ffffff")
        t.append("     $ atectl top workers\n\n", style="bold #8ab4f8")
        t.append("  3. Pre-cache large AI container images to node SSDs:\n", style="bold #ffffff")
        t.append("     $ atectl precache image gcr.io/rl-lab/env:v3.0 --workerpool=default-worker-pool", style="bold #8ab4f8")
        return t

    def action_finish_onboarding(self) -> None:
        if hasattr(self.app, "finish_onboarding"):
            self.app.finish_onboarding()

    def action_previous_step(self) -> None:
        if hasattr(self.app, "previous_step"):
            self.app.previous_step()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-finish":
            self.action_finish_onboarding()
        elif event.button.id == "btn-back":
            self.action_previous_step()
