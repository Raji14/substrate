"""State 1: Welcome and Branding Screen with Google Material 3 Design."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Label, Static
from rich.cells import cell_len
from rich.text import Text
from substrate_onboarding.config import OnboardingStep
from substrate_onboarding.widgets.status_bar import TopHeader, BottomBar
from substrate_onboarding.widgets.ascii_art import get_rendered_logo
from substrate_onboarding.widgets.typewriter import TypewriterWidget


class WelcomeScreen(Screen[None]):
    """State 1: Welcome and Branding (ASCII Splash) Screen."""

    BINDINGS = [
        ("enter", "start_setup", "Start Setup"),
        ("space", "start_setup", "Start Setup"),
    ]

    def __init__(self, name: str = "welcome"):
        super().__init__(name=name)
        self._pulse_visible = True
        self._pulse_timer = None

    def compose(self) -> ComposeResult:
        yield TopHeader(initial_step=OnboardingStep.WELCOME)
        with Vertical(id="screen-container"):
            with Vertical(id="welcome-box"):
                # ASCII Art with Google 4-color gradient
                yield Static(get_rendered_logo(), id="ascii-container")

                # Typewriter welcome tagline
                intro_text = (
                    "Welcome to Agent Substrate on GKE — the high-density execution plane with a "
                    "pierceable abstraction for Platform Engineers and AI Engineers."
                )
                yield TypewriterWidget(
                    full_text=intro_text,
                    char_delay=0.015,
                    id="typewriter-text",
                )

                # Feature Highlights Card with enhanced spacing and legible title
                yield Static(self._render_feature_card(), id="welcome-features-card")

                # Blinking call to action
                yield Label(self._render_cta(), id="cta-prompt")
        yield BottomBar(
            initial_tip="Welcome to Agent Substrate. Press [Enter] to start your onboarding.",
            initial_hints="[Enter] Start  [/help] Help  [Ctrl+C] Exit",
        )

    def _render_feature_card(self, width: int = 84) -> Text:
        """Render a spacious, highly legible Core Capabilities card with perfect Unicode alignment."""
        inner_w = width - 2  # Subtract left and right border width
        t = Text()

        # High-Contrast Title with Google Blue Accent
        title = " ⚡ CORE SUBSTRATE CAPABILITIES "
        dashes_left = 2
        dashes_right = max(2, inner_w - dashes_left - cell_len(title))

        t.append("╭" + "─" * dashes_left, style="bold #8ab4f8")
        t.append(title, style="bold #ffffff on #0842a0")
        t.append("─" * dashes_right + "╮\n", style="bold #8ab4f8")

        # Top buffer line
        t.append("│" + " " * inner_w + "│\n", style="bold #8ab4f8")

        rows = [
            ("🛠️", "Platform Fleet ", "#a8c7fa", "Warm worker pools on GKE with MicroVM & Spot buffers"),
            ("🤖", "Agent Workloads", "#81c995", "No-YAML container templates, turn hooks & request parking"),
            ("⚡", "Instant Resume ", "#fdd663", "Suspend idle actors to 0% CPU; restore state in <200ms"),
        ]

        for i, (icon, label, color, desc) in enumerate(rows):
            line_content = f"  {icon}  {label} : {desc}"
            pad = max(0, inner_w - cell_len(line_content))

            t.append("│  ", style="bold #8ab4f8")
            t.append(f"{icon}  {label} : ", style=f"bold {color}")
            t.append(desc, style="#ffffff")
            t.append(" " * pad + "│\n", style="bold #8ab4f8")

            # Generous inter-row vertical spacing
            if i < len(rows) - 1:
                t.append("│" + " " * inner_w + "│\n", style="bold #8ab4f8")

        # Bottom buffer line
        t.append("│" + " " * inner_w + "│\n", style="bold #8ab4f8")
        t.append("╰" + "─" * inner_w + "╯", style="bold #8ab4f8")
        return t

    def on_mount(self) -> None:
        self._pulse_timer = self.set_interval(0.6, self._toggle_pulse)

    def _toggle_pulse(self) -> None:
        self._pulse_visible = not self._pulse_visible
        try:
            cta_label = self.query_one("#cta-prompt", Label)
            cta_label.update(self._render_cta())
        except Exception:
            pass

    def _render_cta(self) -> Text:
        t = Text()
        if self._pulse_visible:
            t.append("▶  ", style="bold #a8c7fa")
            t.append("Press [ENTER] to start Pre-Flight Diagnostics  ", style="bold #ffffff on #0842a0")
            t.append("(or /help for commands)", style="italic #9aa0a6")
        else:
            t.append("▷  ", style="#8ab4f8")
            t.append("Press [ENTER] to start Pre-Flight Diagnostics  ", style="bold #d3e3fd on #1a3c75")
            t.append("(or /help for commands)", style="italic #9aa0a6")
        return t

    def action_start_setup(self) -> None:
        if hasattr(self.app, "advance_step"):
            self.app.advance_step()
