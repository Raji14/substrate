"""Main Textual Application orchestrating the Substrate Onboarding TUI."""

from __future__ import annotations

import sys
from typing import Optional
from textual.app import App, ComposeResult
from textual.binding import Binding
from rich.text import Text

from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.engine.state_machine import OnboardingStateMachine
from substrate_onboarding.engine.commands import CommandRegistry
from substrate_onboarding.theme import APP_CSS
from substrate_onboarding.widgets.status_bar import TopHeader, BottomBar
from substrate_onboarding.screens.welcome_screen import WelcomeScreen
from substrate_onboarding.screens.doctor_screen import DoctorScreen
from substrate_onboarding.screens.wizard_screen import QuestionnaireScreen
from substrate_onboarding.screens.auth_screen import AuthScreen
from substrate_onboarding.screens.deploy_wp_screen import DeployWorkerPoolScreen
from substrate_onboarding.screens.summary_screen import SummaryScreen
from substrate_onboarding.screens.help_modal import HelpModal
from substrate_onboarding.screens.exit_modal import ExitConfirmModal


class SubstrateOnboardingApp(App[UserSetupState]):
    """Delightful, high-taste Textual TUI for developer onboarding on GKE."""

    CSS = APP_CSS
    TITLE = "Agent Substrate Onboarding on GKE"

    BINDINGS = [
        Binding("ctrl+c", "request_exit", "Exit", show=False, priority=True),
        Binding("ctrl+d", "request_exit", "Exit", show=False, priority=True),
        Binding("f1", "show_help", "Help", show=True),
        Binding("slash", "show_help", "Help", show=False),
        Binding("b", "previous_step", "Back", show=False),
    ]

    SCREENS = {
        "cluster": WelcomeScreen,
        "control_plane": DoctorScreen,
        "node_pool": QuestionnaireScreen,
        "autoscaling": AuthScreen,
        "deploy_wp": DeployWorkerPoolScreen,
        "launchpad": SummaryScreen,
        # Aliases for backward compatibility
        "welcome": WelcomeScreen,
        "doctor": DoctorScreen,
        "questionnaire": QuestionnaireScreen,
        "auth": AuthScreen,
        "summary": SummaryScreen,
    }

    def __init__(self, initial_state: Optional[UserSetupState] = None):
        super().__init__()
        self.state = initial_state or UserSetupState()
        self.state_machine = OnboardingStateMachine(self.state)

    def compose(self) -> ComposeResult:
        return []

    def on_mount(self) -> None:
        """Initialize and push the initial active screen."""
        self.state_machine.add_listener(self._on_state_transition)
        initial_screen = (
            self.state.current_step.value
            if self.state.current_step.value in self.SCREENS
            else "cluster"
        )
        self.push_screen(initial_screen)

    def _on_state_transition(self, old_step: OnboardingStep, new_step: OnboardingStep) -> None:
        """Switch active screen upon state machine transition."""
        screen_name = new_step.value

        if screen_name in self.SCREENS:
            try:
                if self.screen is None or self.screen.name != screen_name:
                    self.switch_screen(screen_name)
            except Exception:
                self.switch_screen(screen_name)

    def advance_step(self) -> None:
        """Move forward to the next onboarding state."""
        self.state_machine.next_step()

    def previous_step(self) -> None:
        """Move backward to the previous onboarding state."""
        self.state_machine.previous_step()

    def action_show_help(self) -> None:
        """Display the global help modal overlay."""
        self.push_screen(HelpModal())

    def action_request_exit(self) -> None:
        """Intercept termination (Ctrl+C / Ctrl+D) and display confirmation modal."""
        def handle_exit(confirmed: Optional[bool]) -> None:
            if confirmed:
                self.exit(self.state)

        self.push_screen(ExitConfirmModal(), handle_exit)

    def execute_slash_command(self, raw_text: str) -> bool:
        """Execute a parsed slash command from any input prompt."""
        cmd = CommandRegistry.parse_command(raw_text)
        if not cmd:
            return False

        if cmd.action_key == "help":
            self.action_show_help()
        elif cmd.action_key == "skip":
            self.advance_step()
        elif cmd.action_key == "back":
            self.previous_step()
        elif cmd.action_key == "doctor":
            self.state_machine.transition_to(OnboardingStep.CONTROL_PLANE)
        elif cmd.action_key == "exit":
            self.action_request_exit()
        return True

    def finish_onboarding(self) -> None:
        """Conclude onboarding successfully."""
        self.state.is_complete = True
        self.exit(self.state)


def run_onboarding() -> UserSetupState:
    """Entrypoint function to run the TUI app."""
    app = SubstrateOnboardingApp()
    return app.run()
