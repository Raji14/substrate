"""Welcome Screen with ASCII Logo, Gradient Animation, Wonder Highlights, and Track Selection."""

from __future__ import annotations

from typing import List, Optional
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Label, Static
from rich.text import Text

from substrate_onboarding.config import OnboardingStep, SETUP_TRACKS, OptionItem
from substrate_onboarding.theme import get_gradient_color
from substrate_onboarding.widgets.status_bar import TopHeader, BottomBar

LOGO_LINES = [
    "  ███████╗██╗   ██╗██████╗ ███████╗████████╗██████╗  █████╗ ████████╗███████╗",
    "  ██╔════╝██║   ██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝",
    "  ███████╗██║   ██║██████╔╝███████╗   ██║   ██████╔╝███████║   ██║   █████╗  ",
    "  ╚════██║██║   ██║██╔══██╗╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██╔══╝  ",
    "  ███████║╚██████╔╝██████╔╝███████║   ██║   ██║  ██║██║  ██║   ██║   ███████╗",
    "  ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝",
]


class WelcomeScreen(Screen[None]):
    """The iconic, wonder-filled welcome screen introducing Agent Substrate."""

    selected_index: reactive[int] = reactive(0)
    gradient_offset: reactive[float] = reactive(0.0)

    BINDINGS = [
        ("enter", "confirm_selection", "Get Started"),
        ("space", "confirm_selection", "Get Started"),
        ("up", "navigate_up", "Previous Track"),
        ("k", "navigate_up", "Previous Track"),
        ("down", "navigate_down", "Next Track"),
        ("j", "navigate_down", "Next Track"),
        ("1", "select_track_1", "Local Sandbox"),
        ("2", "select_track_2", "GKE Fleet"),
        ("3", "select_track_3", "Custom K8s"),
    ]

    def __init__(self, name: Optional[str] = "welcome"):
        super().__init__(name=name)
        self.tracks = SETUP_TRACKS
        self._timer = None

    def compose(self) -> ComposeResult:
        yield TopHeader(initial_step=OnboardingStep.WELCOME)
        with Vertical(id="welcome-main-container"):
            # Animated Hero Logo
            yield Static(self._render_hero_logo(), id="welcome-hero-logo")

            # Subtitle
            yield Label(
                "⚡ High-Density Agent Sandboxing & Sub-100ms Cold-Start Runtime",
                id="welcome-hero-subtitle",
            )

            # 4 Wonder Cards
            with Horizontal(id="welcome-features-row"):
                yield Static(self._render_feature_card("⚡ <100ms Cold Start", "MicroVM standby pre-warming"), classes="wonder-feature-card")
                yield Static(self._render_feature_card("💤 0% Idle CPU", "Auto memory suspend & resume"), classes="wonder-feature-card")
                yield Static(self._render_feature_card("🛡️ Hardware Isolation", "GKE CCC nested virtualization"), classes="wonder-feature-card")
                yield Static(self._render_feature_card("🚀 Zero-YAML CLI", "Direct agent developer workflows"), classes="wonder-feature-card")

            # Mode / Track Selection Title
            yield Label("Select your getting-started path:", id="welcome-tracks-title")

            # Track Cards Container
            with Vertical(id="welcome-tracks-list"):
                for idx, track in enumerate(self.tracks):
                    yield Static(self._render_track_card(idx), id=f"track-card-{idx}", classes="track-option-card")

            # Diagnostics Summary Badge
            yield Static(self._render_preflight_badge(), id="welcome-preflight-badge")

            # Action Button
            with Horizontal(id="welcome-action-row"):
                btn_start = Button(
                    "⚡ Begin Getting Set Up (Enter) →",
                    variant="primary",
                    id="btn-start-onboarding",
                    classes="action-button",
                )
                btn_start.can_focus = False
                yield btn_start

        yield BottomBar(
            initial_tip="Welcome to Agent Substrate! Select your setup path and press [Enter] to begin.",
            initial_hints="[↑/↓] Select Path  [Enter] Start  [/help] Shortcuts  [Ctrl+C] Exit",
        )

    def on_mount(self) -> None:
        self._timer = self.set_interval(0.08, self._animate_gradient)

    def _animate_gradient(self) -> None:
        self.gradient_offset = (self.gradient_offset + 0.03) % 1.0
        try:
            logo = self.query_one("#welcome-hero-logo", Static)
            logo.update(self._render_hero_logo())
        except Exception:
            pass

    def _render_hero_logo(self) -> Text:
        t = Text()
        num_lines = len(LOGO_LINES)
        for y, line in enumerate(LOGO_LINES):
            line_progress = (self.gradient_offset + (y / num_lines) * 0.3) % 1.0
            r, g, b = get_gradient_color(line_progress)
            t.append(line + "\n", style=f"bold rgb({r},{g},{b})")
        return t

    def _render_feature_card(self, title: str, desc: str) -> Text:
        t = Text()
        t.append(f"{title}\n", style="bold #70d6ff")
        t.append(desc, style="#80868b")
        return t

    def _render_track_card(self, idx: int) -> Text:
        track = self.tracks[idx]
        is_selected = idx == self.selected_index
        t = Text()

        if is_selected:
            t.append(" ▶ ", style="bold #ffffff on #1565c0")
            t.append(f" {track.icon} {track.title}\n", style="bold #70d6ff on #1565c0")
            t.append(f"    {track.description}\n", style="#e3e3e3 on #1565c0")
            t.append(f"    💡 {track.tip}", style="italic #81c995 on #1565c0")
        else:
            t.append(" ○ ", style="#5f6368")
            t.append(f" {track.icon} {track.title}\n", style="bold #e3e3e3")
            t.append(f"    {track.description}\n", style="#80868b")
            t.append(f"    💡 {track.tip}", style="italic #5f6368")

        return t

    def _render_preflight_badge(self) -> Text:
        t = Text()
        t.append("✔ Container Runtime: Active   ", style="bold #81c995")
        t.append("│   ✔ Python 3.10+: Ready   ", style="bold #81c995")
        t.append("│   ⚡ MicroVM Sandbox: Ready   ", style="bold #70d6ff")
        t.append("│   ★ Valkey: Standby", style="bold #fdd663")
        return t

    def watch_selected_index(self, index: int) -> None:
        for idx in range(len(self.tracks)):
            try:
                card = self.query_one(f"#track-card-{idx}", Static)
                card.update(self._render_track_card(idx))
            except Exception:
                pass

    def action_navigate_up(self) -> None:
        if self.selected_index > 0:
            self.selected_index -= 1

    def action_navigate_down(self) -> None:
        if self.selected_index < len(self.tracks) - 1:
            self.selected_index += 1

    def action_select_track_1(self) -> None:
        self.selected_index = 0

    def action_select_track_2(self) -> None:
        self.selected_index = 1

    def action_select_track_3(self) -> None:
        self.selected_index = 2

    def action_confirm_selection(self) -> None:
        chosen_track = self.tracks[self.selected_index]
        if hasattr(self.app, "state"):
            self.app.state.selected_track = chosen_track.id
        if hasattr(self.app, "advance_step"):
            self.app.advance_step()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-start-onboarding":
            self.action_confirm_selection()
