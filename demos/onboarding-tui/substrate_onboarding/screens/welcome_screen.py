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
    "    _    ____ _____ _   _ _____        ____  _   _ ____  ____ _____ ____     _  _____ _____ ",
    "   / \\  / ___| ____| \\ | |_   _|      / ___|| | | | __ )/ ___|_   _|  _ \\   / \\|_   _| ____|",
    "  / _ \\| |  _|  _| |  \\| | | |        \\___ \\| | | |  _ \\\\___ \\ | | | |_) | / _ \\ | | |  _|  ",
    " / ___ \\ |_| | |___| |\\  | | |         ___) | |_| | |_) |___) || | |  _ < / ___ \\| | | |___ ",
    "/_/   \\_\\____|_____|_| \\_| |_|        |____/ \\___/|____/|____/ |_| |_| \\_\\_/   \\_\\_| |_____|",
]

INTRO_TEXT = "Welcome to Agent Substrate — the high-density execution runtime with a pierceable abstraction for Platform Engineers and AI Application Developers."


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
            # Crisp Hero Logo for AGENT SUBSTRATE
            yield Static(self._render_hero_logo(), id="welcome-hero-logo")

            # Clean Tagline
            yield Label(
                "High-Density AI Agent Sandboxing on Kubernetes [UX Prototype Simulation]",
                id="welcome-hero-subtitle",
            )

            # Mode / Track Selection Title with Keyboard Shortcuts Hint
            yield Label("Choose installation track (Press [1] or [2]):", id="welcome-tracks-title")

            # Track Cards Container (2 Choices)
            with Vertical(id="welcome-tracks-list"):
                for idx, track in enumerate(self.tracks):
                    yield Static(self._render_track_card(idx), id=f"track-card-{idx}", classes="track-option-card")

            # Clean Diagnostics Summary Badge
            yield Static(self._render_preflight_badge(), id="welcome-preflight-badge")

        yield BottomBar(
            keymaps=[
                ("Enter ↵", "Begin Setup", True),
                ("1", "Quickstart", False),
                ("2", "Advanced", False),
                ("?", "Help", False),
            ],
            step_badge="Welcome",
        )

    def _render_hero_logo(self) -> Text:
        t = Text()
        # Bright, vivid saturated colors for the 5 ASCII logo lines
        line_styles = [
            "bold #00f0ff",  # Vivid Electric Cyan
            "bold #ff3b69",  # Vivid Crimson Red
            "bold #ffd000",  # Vivid Bright Gold
            "bold #00ff88",  # Vivid Emerald Neon Green
            "bold #38b6ff",  # Vivid Sky Blue
        ]
        for y, line in enumerate(LOGO_LINES):
            style_color = line_styles[y % len(line_styles)]
            t.append(line + "\n", style=style_color)
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
        t.append("●  ", style="bold #81c995")
        t.append("K8s Context: ", style="#80868b")
        t.append("gke_enterprise_us-central1_prod    •    ", style="bold #ffffff")
        t.append("●  ", style="bold #81c995")
        t.append("Preflight: ", style="#80868b")
        t.append("Ready", style="bold #ffffff")
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
        self.action_confirm_selection()

    def action_select_track_2(self) -> None:
        self.selected_index = 1
        self._refresh_tracks()
        self.action_confirm_selection()

    def _refresh_tracks(self) -> None:
        for idx in range(len(self.tracks)):
            try:
                card = self.query_one(f"#track-card-{idx}", Static)
                card.update(self._render_track_card(idx))
            except Exception:
                pass
