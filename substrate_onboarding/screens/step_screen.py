"""Generic interactive StepScreen for the 8-Step Substrate Onboarding Journey."""

from __future__ import annotations

import asyncio
from typing import Optional
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Label, Static, Button
from rich.text import Text
from substrate_onboarding.config import OnboardingStep, STEP_CONFIGS, StepMetadata
from substrate_onboarding.widgets.status_bar import TopHeader, BottomBar
from substrate_onboarding.widgets.sidebar_nav import SidebarNav


class GenericStepScreen(Screen[None]):
    """Generic high-fidelity step screen rendering the 2-column layout."""

    BINDINGS = [
        ("enter", "proceed_next", "Proceed"),
        ("space", "proceed_next", "Proceed"),
        ("b", "previous_step", "Back"),
    ]

    def __init__(self, step_key: OnboardingStep, name: Optional[str] = None):
        screen_name = name or step_key.value
        super().__init__(name=screen_name)
        self.step_key = step_key
        self.meta: StepMetadata = STEP_CONFIGS[step_key]
        self._checklist_progress = 0
        self._timer = None

    def compose(self) -> ComposeResult:
        yield TopHeader(initial_step=self.step_key)
        with Horizontal(id="workspace-layout"):
            yield SidebarNav(current_step=self.step_key)
            with Vertical(id="content-area"):
                with Vertical(id="content-panel"):
                    # Step Number & Title
                    yield Label(f"Step {self.meta.step_num} of 8", classes="step-indicator-label")
                    yield Label(self.meta.heading, classes="wizard-step-title")
                    yield Label(self.meta.description, classes="wizard-step-description")

                    # Real Command Callout Card
                    yield Static(self._render_command_callout(), id="command-callout-card")

                    # Live Execution Checklist Card
                    yield Static(self._render_checklist_box(), id="execution-checklist-card")

                    # Action Button Row
                    with Horizontal(classes="action-button-row"):
                        if self.meta.step_num > 1:
                            btn_back = Button("← Back (b)", id="btn-back", classes="secondary-button")
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
            initial_hints="[Enter] Proceed  [b] Back  [/help] Help  [Ctrl+C] Exit",
        )

    def on_mount(self) -> None:
        self._checklist_progress = 0
        self._timer = self.set_interval(0.2, self._tick_checklist)

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
        # Blue pill badge
        t.append(" ▼ Show the real command \n", style="bold #ffffff on #1565c0")
        t.append(f"\n  {self.meta.real_command}", style="#70d6ff")
        return t

    def _render_checklist_box(self) -> Text:
        t = Text()
        t.append(f"{self.meta.checklist_title}\n\n", style="bold #70d6ff")

        for i, item in enumerate(self.meta.checklist_items):
            if i < self._checklist_progress:
                t.append("✓ ", style="bold #81c995")
                t.append(f"{item}\n", style="bold #ffffff")
            elif i == self._checklist_progress:
                t.append("⠋ ", style="bold #70d6ff")
                t.append(f"{item}\n", style="#70d6ff")
            else:
                t.append("○ ", style="#5f6368")
                t.append(f"{item}\n", style="#5f6368")

        if self._checklist_progress >= len(self.meta.checklist_items):
            t.append("\nDone\n\n", style="bold #81c995")
            t.append(self.meta.done_message, style="#e3e3e3")

        return t

    def action_proceed_next(self) -> None:
        if hasattr(self.app, "advance_step"):
            self.app.advance_step()

    def action_previous_step(self) -> None:
        if hasattr(self.app, "previous_step"):
            self.app.previous_step()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-proceed":
            self.action_proceed_next()
        elif event.button.id == "btn-back":
            self.action_previous_step()
