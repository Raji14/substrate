"""Main Textual Application orchestrating the Substrate Onboarding TUI with Welcome Screen."""

from __future__ import annotations

import sys
from typing import Optional
from textual.app import App, ComposeResult
from textual.binding import Binding

from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.engine.state_machine import OnboardingStateMachine
from substrate_onboarding.engine.commands import CommandRegistry
from substrate_onboarding.theme import APP_CSS
from substrate_onboarding.screens.welcome_screen import WelcomeScreen
from substrate_onboarding.screens.step_screen import GenericStepScreen
from substrate_onboarding.screens.help_modal import HelpModal
from substrate_onboarding.screens.exit_modal import ExitConfirmModal


class SubstrateOnboardingApp(App[UserSetupState]):
    """Delightful, high-taste Textual TUI for developer onboarding with Welcome Screen."""

    CSS = APP_CSS
    TITLE = "Substrate — Getting set up (Private GA)"

    BINDINGS = [
        Binding("ctrl+c", "request_exit", "Exit", show=False, priority=True),
        Binding("ctrl+d", "request_exit", "Exit", show=False, priority=True),
        Binding("f1", "show_help", "Help", show=True),
        Binding("slash", "show_help", "Help", show=False),
        Binding("b", "previous_step", "Back", show=False),
    ]

    SCREENS = {
        "welcome": WelcomeScreen,
        "check_setup": lambda: GenericStepScreen(OnboardingStep.CHECK_SETUP, name="check_setup"),
        "connect_cluster": lambda: GenericStepScreen(OnboardingStep.CONNECT_CLUSTER, name="connect_cluster"),
        "turn_on_sub": lambda: GenericStepScreen(OnboardingStep.TURN_ON_SUBSTRATE, name="turn_on_sub"),
        "compatible_nodepool": lambda: GenericStepScreen(OnboardingStep.COMPATIBLE_NODEPOOL, name="compatible_nodepool"),
        "config_autoscaling": lambda: GenericStepScreen(OnboardingStep.CONFIG_AUTOSCALING, name="config_autoscaling"),
        "deploy_workerpool": lambda: GenericStepScreen(OnboardingStep.DEPLOY_WORKERPOOL, name="deploy_workerpool"),
        "install_cli": lambda: GenericStepScreen(OnboardingStep.INSTALL_CLI, name="install_cli"),
        "first_actor": lambda: GenericStepScreen(OnboardingStep.FIRST_ACTOR, name="first_actor"),
        "send_request": lambda: GenericStepScreen(OnboardingStep.SEND_REQUEST, name="send_request"),
        "pause_resume": lambda: GenericStepScreen(OnboardingStep.PAUSE_RESUME, name="pause_resume"),
        "scale_up": lambda: GenericStepScreen(OnboardingStep.SCALE_UP, name="scale_up"),
        # Backward compatibility aliases
        "private_ga": lambda: GenericStepScreen(OnboardingStep.CONNECT_CLUSTER, name="connect_cluster"),
        "cluster": lambda: GenericStepScreen(OnboardingStep.CONNECT_CLUSTER, name="connect_cluster"),
        "create_cluster": lambda: GenericStepScreen(OnboardingStep.CONNECT_CLUSTER, name="connect_cluster"),
        "control_plane": lambda: GenericStepScreen(OnboardingStep.TURN_ON_SUBSTRATE, name="turn_on_sub"),
        "node_pool": lambda: GenericStepScreen(OnboardingStep.COMPATIBLE_NODEPOOL, name="compatible_nodepool"),
        "autoscaling": lambda: GenericStepScreen(OnboardingStep.CONFIG_AUTOSCALING, name="config_autoscaling"),
        "deploy_wp": lambda: GenericStepScreen(OnboardingStep.DEPLOY_WORKERPOOL, name="deploy_workerpool"),
        "launchpad": lambda: GenericStepScreen(OnboardingStep.SCALE_UP, name="scale_up"),
        "doctor": lambda: GenericStepScreen(OnboardingStep.CHECK_SETUP, name="check_setup"),
        "questionnaire": lambda: GenericStepScreen(OnboardingStep.CONNECT_CLUSTER, name="connect_cluster"),
        "auth": lambda: GenericStepScreen(OnboardingStep.CONNECT_CLUSTER, name="connect_cluster"),
        "summary": lambda: GenericStepScreen(OnboardingStep.SCALE_UP, name="scale_up"),
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
            else "welcome"
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
            self.state_machine.transition_to(OnboardingStep.CHECK_SETUP)
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
