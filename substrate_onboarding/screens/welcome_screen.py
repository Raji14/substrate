"""Welcome Screen with 'Agent Substrate' splash title, two streamlined setup choices, and tactile keyboard shortcuts."""

from __future__ import annotations

from typing import List, Optional
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Label, Static
from rich.text import Text

from substrate_onboarding.config import OnboardingStep, SETUP_TRACKS, OptionItem
from substrate_onboarding.widgets.status_bar import TopHeader, BottomBar

LOGO_LINES = [
    "    _    ____ _____ _   _ _____   ____  _   _ ____  ____ _____ ____     _  _____ _____ ",
    "   / \\  / ___| ____| \\ | |_   _| / ___|| | | | __ )/ ___|_   _|  _ \\   / \\|_   _| ____|",
    "  / _ \\| |  _|  _| |  \\| | | |   \\___ \\| | | |  _ \\\\___ \\ | | | |_) | / _ \\ | | |  _|  ",
    " / ___ \\ |_| | |___| |\\  | | |    ___) | |_| | |_) |___) || | |  _ < / ___ \\| | | |___ ",
    "/_/   \\_\\____|_____|_| \\_| |_|   |____/ \\___/|____/|____/ |_| |_| \\_\\_/   \\_\\_| |_____|",
]

INTRO_TEXT = "Welcome to Agent Substrate — the high-density execution runtime with a pierceable abstraction for Platform Engineers and AI Application Developers (Private GA)."


class WelcomeScreen(Screen[None]):
    """The iconic, wonder-filled welcome screen with 'Agent Substrate' splash title and 2 setup tracks."""

    selected_index: reactive[int] = reactive(0)
    typewriter_idx: reactive[int] = reactive(0)

    BINDINGS = [
        ("enter", "confirm_selection", "Get Started"),
        ("space", "confirm_selection", "Get Started"),
        ("up", "navigate_up", "Previous Track"),
        ("k", "navigate_up", "Previous Track"),
        ("down", "navigate_down", "Next Track"),
        ("j", "navigate_down", "Next Track"),
        ("1", "select_track_1", "Quickstart"),
        ("2", "select_track_2", "Advanced"),
    ]

    def __init__(self, name: Optional[str] = "welcome"):
        super().__init__(name=name)
        self.tracks = SETUP_TRACKS
        self._typewriter_timer = None

    def compose(self) -> ComposeResult:
        yield TopHeader(initial_step=OnboardingStep.WELCOME)
        with Vertical(id="welcome-main-container"):
            # Static 4-Color Gradient Hero Logo for AGENT SUBSTRATE
            yield Static(self._render_hero_logo(), id="welcome-hero-logo")

            # Punchy Tagline (No repetition of 'Agent Substrate')
            yield Label(
                "⚡ High-Density Sandboxing & Sub-100ms Cold-Start Runtime (Private GA)",
                id="welcome-hero-subtitle",
            )

            # Animated Typewriter Description
            yield Static(self._render_typewriter(), id="welcome-typewriter-box")

            # Core Capabilities Feature Card
            with Vertical(id="welcome-features-card"):
                yield Static(self._render_features_card(), id="welcome-features-content")

            # Mode / Track Selection Title with Keyboard Shortcuts Hint
            yield Label("Choose your installation path (Press [1] or [2]):", id="welcome-tracks-title")

            # Track Cards Container (2 Choices)
            with Vertical(id="welcome-tracks-list"):
                for idx, track in enumerate(self.tracks):
                    yield Static(self._render_track_card(idx), id=f"track-card-{idx}", classes="track-option-card")

            # Diagnostics Summary Badge
            yield Static(self._render_preflight_badge(), id="welcome-preflight-badge")

            # Action Button with prominent keyboard indicator
            with Horizontal(id="welcome-action-row"):
                btn_start = Button(
                    "▶  Press [Enter ↵] to Begin Getting Set Up →",
                    variant="primary",
                    id="btn-start-onboarding",
                    classes="action-button",
                )
                btn_start.can_focus = False
                yield btn_start

        yield BottomBar(
            initial_tip="Welcome to Agent Substrate! Press [1] for Quickstart, [2] for Advanced, or [Enter ↵] to start.",
            initial_hints="[1/2] Quick Select  [↑/↓] Navigate  [Enter ↵] Proceed  [b] Back  [/help] Help",
        )

    def on_mount(self) -> None:
        self.typewriter_idx = 0
        self._typewriter_timer = self.set_interval(0.02, self._tick_typewriter)

    def _tick_typewriter(self) -> None:
        if self.typewriter_idx < len(INTRO_TEXT):
            self.typewriter_idx += 1
            try:
                box = self.query_one("#welcome-typewriter-box", Static)
                box.update(self._render_typewriter())
            except Exception:
                pass
        else:
            if self._typewriter_timer:
                self._typewriter_timer.stop()

    def _render_hero_logo(self) -> Text:
        t = Text()
        # Google 4-Color Gradient lines
        line_styles = [
            "#8ab4f8",  # Google Blue
            "#f28b82",  # Google Red
            "#fdd663",  # Google Yellow
            "#81c995",  # Google Green
            "#a8c7fa",  # Google Light Blue
        ]
        for y, line in enumerate(LOGO_LINES):
            style_color = line_styles[y % len(line_styles)]
            t.append(line + "\n", style=f"bold {style_color}")
        return t

    def _render_typewriter(self) -> Text:
        t = Text()
        typed_str = INTRO_TEXT[: self.typewriter_idx]
        t.append(typed_str, style="#e3e3e3")
        if self.typewriter_idx < len(INTRO_TEXT):
            t.append(" ▌", style="bold #8ab4f8")
        return t

    def _render_features_card(self) -> Text:
        t = Text()
        t.append("⚡ CORE SUBSTRATE CAPABILITIES:\n", style="bold #70d6ff")
        t.append("  🛠️   Platform Fleet   : ", style="bold #8ab4f8")
        t.append("Warm worker pools on pre-existing K8s with MicroVM & capacity buffers\n", style="#ffffff")
        t.append("  🤖   Agent Workloads  : ", style="bold #81c995")
        t.append("No-YAML container templates, turn hooks & request parking\n", style="#ffffff")
        t.append("  ⚡   Instant Resume   : ", style="bold #fdd663")
        t.append("Suspend idle actors to 0% CPU; restore state in <200ms\n", style="#ffffff")
        t.append("  🔒   Private GA Gated : ", style="bold #f28b82")
        t.append("Customer registration & explicit Google support terms acknowledgment", style="#ffffff")
        return t

    def _render_track_card(self, idx: int) -> Text:
        track = self.tracks[idx]
        is_selected = idx == self.selected_index
        t = Text()

        keycap = f" [{idx + 1}] "
        if is_selected:
            t.append(f" ▶ {keycap}", style="bold #ffffff on #1565c0")
            t.append(f" {track.icon}   {track.title}\n", style="bold #70d6ff on #1565c0")
            t.append(f"        {track.description}\n", style="#e3e3e3 on #1565c0")
            t.append(f"        💡 {track.tip}", style="italic #81c995 on #1565c0")
        else:
            t.append(f" ○ {keycap}", style="#80868b")
            t.append(f" {track.icon}   {track.title}\n", style="bold #e3e3e3")
            t.append(f"        {track.description}\n", style="#80868b")
            t.append(f"        💡 {track.tip}", style="italic #5f6368")

        return t

    def _render_preflight_badge(self) -> Text:
        t = Text()
        t.append(" ✔  ", style="bold #81c995")
        t.append("Pre-configured K8s: Connected    │    ", style="#e3e3e3")
        t.append("✔  ", style="bold #81c995")
        t.append("Python 3.10+: Ready    │    ", style="#e3e3e3")
        t.append("⚡  ", style="bold #81c995")
        t.append("MicroVM Sandbox: Ready    │    ", style="#e3e3e3")
        t.append("★  ", style="bold #fdd663")
        t.append("Private GA: Gated", style="#fdd663")
        return t

    def action_confirm_selection(self) -> None:
        if hasattr(self.app, "advance_step"):
            self.app.advance_step()

    def action_navigate_up(self) -> None:
        if self.selected_index > 0:
            self.selected_index -= 1
            self._refresh_tracks()

    def action_navigate_down(self) -> None:
        if self.selected_index < len(self.tracks) - 1:
            self.selected_index += 1
            self._refresh_tracks()

    def action_select_track_1(self) -> None:
        self.selected_index = 0
        self._refresh_tracks()

    def action_select_track_2(self) -> None:
        self.selected_index = 1
        self._refresh_tracks()

    def _refresh_tracks(self) -> None:
        for idx in range(len(self.tracks)):
            try:
                card = self.query_one(f"#track-card-{idx}", Static)
                card.update(self._render_track_card(idx))
            except Exception:
                pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-start-onboarding":
            self.action_confirm_selection()
