"""State 5: Summary and Launch Transition Screen with Google Material 3 Design."""

from __future__ import annotations

import asyncio
from typing import Optional
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Label, Button, ProgressBar, Static
from rich.cells import cell_len
from rich.text import Text
from substrate_onboarding.config import OnboardingStep
from substrate_onboarding.widgets.status_bar import TopHeader, BottomBar


class SummaryScreen(Screen[None]):
    """State 5: Summary card, workspace compilation progress, and launch celebration."""

    BINDINGS = [
        ("enter", "launch_workspace", "Launch Workspace"),
        ("q", "finish_and_exit", "Exit"),
        ("b", "previous_step", "Back"),
    ]

    PROGRESS_STAGES = [
        (0.20, "Generating substrate.yaml & WorkerPool CRD manifests..."),
        (0.45, "Allocating GKE worker pool (50 pre-warmed idle standby pods)..."),
        (0.70, "Testing data plane: Cold Boot (912ms) → Suspend (42ms) → Warm Resume (120ms)..."),
        (0.90, "Configuring /idle turn-completion hooks & GCS snapshot storage..."),
        (1.00, "Workspace configured successfully! Worker pool ready for high-density dispatch."),
    ]

    def __init__(self, name: str = "summary"):
        super().__init__(name=name)
        self._is_compiled = False
        self._compile_task: Optional[asyncio.Task] = None

    def compose(self) -> ComposeResult:
        yield TopHeader(initial_step=OnboardingStep.SUMMARY)
        with Vertical(id="screen-container"):
            with Vertical(id="summary-box"):
                yield Label("🛸  STEP 4: CLUSTER LAUNCHPAD & 3-PHASE OPERATIONS RUNBOOK", classes="wizard-step-title")
                yield Label(
                    "Review your GKE Substrate profile before compiling manifests & starting worker pools:",
                    classes="wizard-step-subtitle",
                )

                # Summary Card
                yield Static("", id="summary-card")

                # Compilation progress container
                with Vertical(id="progress-container"):
                    yield ProgressBar(total=100, show_eta=False, id="launch-progress-bar")
                    yield Label("Preparing workspace compiler...", id="launch-progress-label")

                # Post-compilation celebration container
                with Vertical(id="celebration-container"):
                    yield Static("", id="celebration-banner")

                with Horizontal(classes="auth-button-row"):
                    btn_back = Button("← Modify Settings (b)", id="btn-summary-back", classes="secondary-button")
                    btn_back.can_focus = False
                    yield btn_back

                    btn_launch = Button("Launch Agent Substrate (Enter) 🚀", id="btn-launch-app", classes="action-button")
                    yield btn_launch
        yield BottomBar(
            initial_tip="Compiling substrate manifests and initializing worker pools...",
            initial_hints="[Enter] Launch Agent Substrate  [/help] Help",
        )

    def on_mount(self) -> None:
        self._render_summary_card()
        cel = self.query_one("#celebration-container", Vertical)
        cel.display = False
        self._compile_task = asyncio.create_task(self._animate_compilation())

    def _render_summary_card(self, width: int = 84) -> None:
        if not hasattr(self.app, "state"):
            return

        summary_dict = self.app.state.to_summary_dict()
        inner_w = width - 2
        title = " ⚙ GKE SUBSTRATE PROFILE "
        dashes_left = 2
        dashes_right = max(2, inner_w - dashes_left - cell_len(title))

        t = Text()
        t.append("╭" + "─" * dashes_left, style="bold #a8c7fa")
        t.append(title, style="bold #003062 on #a8c7fa")
        t.append("─" * dashes_right + "╮\n", style="bold #a8c7fa")

        for key, val in summary_dict.items():
            line_text = f"  {key.ljust(22)}: {val}"
            pad = max(0, inner_w - cell_len(line_text))
            t.append("│  ", style="bold #a8c7fa")
            t.append(f"{key.ljust(22)}: ", style="#9aa0a6")
            t.append(f"{val}", style="bold #ffffff")
            t.append(" " * pad + "│\n", style="bold #a8c7fa")

        t.append("╰" + "─" * inner_w + "╯", style="bold #a8c7fa")

        try:
            card = self.query_one("#summary-card", Static)
            card.update(t)
        except Exception:
            pass

    async def _animate_compilation(self) -> None:
        pbar = self.query_one("#launch-progress-bar", ProgressBar)
        plabel = self.query_one("#launch-progress-label", Label)

        try:
            for pct, stage_text in self.PROGRESS_STAGES:
                pbar.progress = int(pct * 100)
                plabel.update(Text(f"⚙ {stage_text}", style="italic #a8c7fa"))
                await asyncio.sleep(0.55)

            self._is_compiled = True
            prog_box = self.query_one("#progress-container", Vertical)
            prog_box.display = False

            # Display celebration
            cel = self.query_one("#celebration-container", Vertical)
            cel.display = True
            banner = self.query_one("#celebration-banner", Static)

            t = Text()
            t.append("🎉 SUBSTRATE CONFIGURED — READY FOR PLATFORM & AI WORKLOADS!\n", style="bold #81c995")
            t.append("🚀 Phase 1: Platform Setup : ", style="bold #a8c7fa")
            t.append("curl -sSL ate.dev/install.sh | bash && atectl create workerpools ...\n", style="#ffffff")
            t.append("🤖 Phase 2: Agent Deploy   : ", style="bold #81c995")
            t.append("atectl create template my-agent --image gcr.io/repo/my-agent:v1 ...\n", style="#ffffff")
            t.append("📊 Phase 3: Observability  : ", style="bold #fdd663")
            t.append("atectl top workers | atectl precache image gcr.io/rl-lab/env:v3.0", style="#ffffff")

            banner.update(t)

            try:
                bottom = self.query_one(BottomBar)
                bottom.set_tip("Onboarding successfully finished! Press [Enter] or click Launch.")
                bottom.set_hints("[Enter] Launch Agent Substrate  [/help] Help")
            except Exception:
                pass
        except asyncio.CancelledError:
            pass

    def action_launch_workspace(self) -> None:
        if hasattr(self.app, "advance_step"):
            self.app.advance_step()

    def action_finish_and_exit(self) -> None:
        if hasattr(self.app, "exit"):
            self.app.exit(self.app.state if hasattr(self.app, "state") else None)

    def action_previous_step(self) -> None:
        if hasattr(self.app, "previous_step"):
            self.app.previous_step()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-launch-app":
            self.action_launch_workspace()
        elif event.button.id == "btn-summary-back":
            self.action_previous_step()
