"""Header and status bar widgets with Google Material 3 styling and brand tokens.

Option A Stepper Alignment:
  1. Pre-Flight (Diagnostics & GKE Cluster Context)
  2. Platform Setup (WorkerPools, MicroVM / gVisor isolation & capacity buffers)
  3. Agent Deployment (ActorTemplates, OCI images & credentials)
  4. Launchpad (Compilation, atectl top workers, precache & ready state)
"""

from __future__ import annotations

from typing import Optional
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label
from rich.text import Text
from substrate_onboarding.config import OnboardingStep


STEP_NAMES = {
    OnboardingStep.WELCOME: "🩺 1. Pre-Flight",
    OnboardingStep.DOCTOR: "🩺 1. Pre-Flight",
    OnboardingStep.QUESTIONNAIRE: "🛠️ 2. Platform Setup",
    OnboardingStep.AUTH: "🤖 3. Agent Deployment",
    OnboardingStep.SUMMARY: "🛸 4. Launchpad",
    OnboardingStep.COMPLETE: "Launch",
}


class TopHeader(Widget):
    """Global top navigation bar with Option A 4-phase PRFAQ breadcrumbs."""

    current_step: reactive[OnboardingStep] = reactive(OnboardingStep.DOCTOR)

    def __init__(self, initial_step: OnboardingStep = OnboardingStep.DOCTOR, id: str = "top-header"):
        super().__init__(id=id)
        self.current_step = initial_step

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(self._render_brand(), id="header-brand")
            yield Label(self._render_stepper(), id="header-stepper")

    def _render_brand(self) -> Text:
        t = Text("⚡ Google Cloud ", style="bold #8ab4f8")
        t.append("│ Agent Substrate", style="bold #ffffff")
        return t

    def _render_stepper(self) -> Text:
        t = Text()
        steps = [
            OnboardingStep.DOCTOR,
            OnboardingStep.QUESTIONNAIRE,
            OnboardingStep.AUTH,
            OnboardingStep.SUMMARY,
        ]
        step_order = {
            OnboardingStep.WELCOME: 0,
            OnboardingStep.DOCTOR: 1,
            OnboardingStep.QUESTIONNAIRE: 2,
            OnboardingStep.AUTH: 3,
            OnboardingStep.SUMMARY: 4,
            OnboardingStep.COMPLETE: 5,
        }
        current_idx = step_order.get(self.current_step, 1)

        for i, step in enumerate(steps):
            step_num = i + 1
            name = STEP_NAMES[step]
            if step_num == current_idx or (current_idx == 0 and step_num == 1):
                t.append(f" [ {name} ] ", style="bold #003062 on #a8c7fa")
            elif step_num < current_idx:
                t.append(f" ✓ {name} ", style="bold #81c995")
            else:
                t.append(f" {name} ", style="#9aa0a6")
            if i < len(steps) - 1:
                t.append(" › ", style="#444746")
        return t

    def watch_current_step(self, step: OnboardingStep) -> None:
        try:
            stepper_label = self.query_one("#header-stepper", Label)
            stepper_label.update(self._render_stepper())
        except Exception:
            pass


class BottomBar(Widget):
    """Dynamic bottom status bar displaying contextual tips and keyboard legend."""

    tip_text: reactive[str] = reactive("Welcome to Agent Substrate. Press [Enter] to begin.")
    hint_text: reactive[str] = reactive("[Enter] Proceed  [/help] Commands  [Ctrl+C] Exit")

    def __init__(
        self,
        initial_tip: str = "Welcome to Agent Substrate. Press [Enter] to begin.",
        initial_hints: str = "[Enter] Proceed  [/help] Commands  [Ctrl+C] Exit",
        id: str = "bottom-bar",
    ):
        super().__init__(id=id)
        self.tip_text = initial_tip
        self.hint_text = initial_hints

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(Text(f"💡  {self.tip_text}", style="#d3e3fd"), id="status-tip")
            yield Label(Text(self.hint_text, style="bold #9aa0a6"), id="keyboard-hints")

    def set_tip(self, text: str) -> None:
        self.tip_text = text
        try:
            tip_label = self.query_one("#status-tip", Label)
            tip_label.update(Text(f"💡  {text}", style="#d3e3fd"))
        except Exception:
            pass

    def set_hints(self, text: str) -> None:
        self.hint_text = text
        try:
            hint_label = self.query_one("#keyboard-hints", Label)
            hint_label.update(Text(text, style="bold #9aa0a6"))
        except Exception:
            pass
