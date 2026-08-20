"""Header and status bar widgets with Google Material 3 styling and brand tokens.

Provides:
- TopHeader: Google Cloud branding, active cluster context, and quick action shortcuts.
- BottomBar: Contextual interactive tip and keyboard shortcuts legend.
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


class TopHeader(Widget):
    """Global top navigation bar with Google Cloud branding and quick status badges."""

    current_step: reactive[OnboardingStep] = reactive(OnboardingStep.CLUSTER)

    def __init__(
        self,
        initial_step: OnboardingStep = OnboardingStep.CLUSTER,
        cluster_name: str = "demo-cluster",
        id: str = "top-header",
    ):
        super().__init__(id=id)
        self.current_step = initial_step
        self.cluster_name = cluster_name

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(self._render_brand(), id="header-brand")
            yield Label(self._render_quick_actions(), id="header-stepper")

    def _render_brand(self) -> Text:
        t = Text("⚡ Google Cloud ", style="bold #8ab4f8")
        t.append("│ Agent Substrate on GKE", style="bold #ffffff")
        return t

    def _render_quick_actions(self) -> Text:
        t = Text()
        t.append(" [ 🌐 Cluster: ", style="#9aa0a6")
        t.append(f"{self.cluster_name} ", style="bold #8ab4f8")
        t.append("] ", style="#9aa0a6")
        t.append(" [ ? Help (F1) ] ", style="bold #d3e3fd on #0842a0")
        t.append(" [ ⏻ Exit ] ", style="#9aa0a6")
        return t

    def watch_current_step(self, step: OnboardingStep) -> None:
        try:
            stepper_label = self.query_one("#header-stepper", Label)
            stepper_label.update(self._render_quick_actions())
        except Exception:
            pass


class BottomBar(Widget):
    """Dynamic bottom status bar displaying contextual tips and keyboard legend."""

    tip_text: reactive[str] = reactive("Welcome to Agent Substrate. Press [Enter] to begin.")
    hint_text: reactive[str] = reactive("[Enter] Proceed  [↑/↓] Select  [b] Back  [/help] Commands")

    def __init__(
        self,
        initial_tip: str = "Welcome to Agent Substrate. Press [Enter] to begin.",
        initial_hints: str = "[Enter] Proceed  [↑/↓] Select  [b] Back  [/help] Commands",
        tip: Optional[str] = None,
        hints: Optional[str] = None,
        id: str = "bottom-bar",
    ):
        super().__init__(id=id)
        self.tip_text = tip or initial_tip
        self.hint_text = hints or initial_hints

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
