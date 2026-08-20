"""State 3: Environment Pre-flight Check (The Doctor Step)."""

from __future__ import annotations

import asyncio
from typing import Dict, Optional
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Label, Button
from rich.text import Text
from substrate_onboarding.config import OnboardingStep, CheckResult
from substrate_onboarding.checks.runner import PreflightRunner
from substrate_onboarding.widgets.status_bar import TopHeader, BottomBar
from substrate_onboarding.widgets.doctor_item import DoctorItemWidget


class DoctorScreen(Screen[None]):
    """State 3: Pre-flight Diagnostic Doctor Step."""

    BINDINGS = [
        ("enter", "proceed_next", "Proceed"),
        ("space", "proceed_next", "Proceed"),
        ("r", "rerun_checks", "Re-run Checks"),
        ("c", "copy_remedy_command", "Copy Fix"),
        ("b", "previous_step", "Back"),
    ]

    def __init__(self, name: str = "doctor"):
        super().__init__(name=name)
        self.runner = PreflightRunner()
        self._run_task: Optional[asyncio.Task] = None
        self._is_finished = False

    def compose(self) -> ComposeResult:
        yield TopHeader(initial_step=OnboardingStep.DOCTOR)
        with Vertical(id="screen-container"):
            with Vertical(id="doctor-box"):
                yield Label("🩺  STEP 1: PRE-FLIGHT ENVIRONMENT & GKE DIAGNOSTICS", classes="wizard-step-title")
                yield Label(
                    "Checking your local tools, connected GKE cluster, and cloud storage before starting...",
                    classes="wizard-step-subtitle",
                )

                with Vertical(id="doctor-list"):
                    for key, name, _ in PreflightRunner.CHECK_DEFINITIONS:
                        yield DoctorItemWidget(key=key, name=name, id=f"doc-widget-{key}")

                with Horizontal(classes="auth-button-row"):
                    btn_back = Button("← Back (b)", id="btn-doc-back", classes="secondary-button")
                    btn_back.can_focus = False
                    yield btn_back

                    btn_rerun = Button("Re-run Checks (r)", id="btn-doc-rerun", classes="secondary-button")
                    btn_rerun.can_focus = False
                    yield btn_rerun

                    btn_proceed = Button("Proceed to Platform Setup (Enter) →", id="btn-doc-proceed", classes="action-button")
                    btn_proceed.can_focus = False
                    yield btn_proceed
        yield BottomBar(
            initial_tip="Checking your computer and cluster tools. You can proceed at any time.",
            initial_hints="[Enter] Proceed  [r] Re-run  [c] Copy Fix Command  [/help] Help",
        )

    def on_mount(self) -> None:
        self.start_diagnostics()

    def start_diagnostics(self) -> None:
        self._is_finished = False
        self.runner.set_callbacks(
            on_start=self._on_check_start,
            on_complete=self._on_check_complete,
        )
        self._run_task = asyncio.create_task(self._run_checks_async())

    async def _run_checks_async(self) -> None:
        await self.runner.run_all()
        self._is_finished = True
        try:
            bottom = self.query_one(BottomBar)
            bottom.set_tip("Pre-flight checks complete. Press [Enter] to proceed.")
            bottom.set_hints("[r] Re-run  [Enter] Proceed  [/help] Help")
        except Exception:
            pass

    def _on_check_start(self, key: str, name: str) -> None:
        try:
            widget = self.query_one(f"#doc-widget-{key}", DoctorItemWidget)
            widget.set_running()
        except Exception:
            pass

    def _on_check_complete(self, key: str, result: CheckResult) -> None:
        try:
            widget = self.query_one(f"#doc-widget-{key}", DoctorItemWidget)
            widget.set_result(result)
        except Exception:
            pass

    def action_proceed_next(self) -> None:
        if hasattr(self.app, "advance_step"):
            self.app.advance_step()

    def action_rerun_checks(self) -> None:
        if self._run_task and not self._run_task.done():
            self._run_task.cancel()
        self.start_diagnostics()

    def action_copy_remedy_command(self) -> None:
        """Copy active remedy command to clipboard or display it clearly."""
        for key, res in self.runner.results.items():
            if res.status in ("warning", "failed") and res.fix_command:
                try:
                    import subprocess
                    subprocess.run(["pbcopy"], input=res.fix_command.encode("utf-8"), check=False)
                except Exception:
                    pass
                try:
                    bottom = self.query_one(BottomBar)
                    bottom.set_tip(f"📋 Copied fix command to clipboard: {res.fix_command}")
                except Exception:
                    pass
                return

    def action_previous_step(self) -> None:
        if hasattr(self.app, "previous_step"):
            self.app.previous_step()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-doc-proceed":
            self.action_proceed_next()
        elif event.button.id == "btn-doc-rerun":
            self.action_rerun_checks()
        elif event.button.id == "btn-doc-back":
            self.action_previous_step()
