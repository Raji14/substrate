"""Advanced interaction tests for slash commands, modals, error validation, and OAuth."""

import pytest
from textual.widgets import Input
from substrate_onboarding.app import SubstrateOnboardingApp
from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.screens.auth_screen import AuthScreen
from substrate_onboarding.screens.exit_modal import ExitConfirmModal
from substrate_onboarding.screens.help_modal import HelpModal
from substrate_onboarding.widgets.command_bar import InlineErrorBanner


@pytest.mark.asyncio
async def test_slash_command_execution():
    app = SubstrateOnboardingApp()
    async with app.run_test() as pilot:
        # Test /help command
        handled = app.execute_slash_command("/help")
        assert handled is True
        await pilot.pause(0.05)
        assert isinstance(app.screen, HelpModal)

        # Close help modal
        await pilot.press("escape")
        await pilot.pause(0.05)

        # Test /skip command (advances from WELCOME to DOCTOR)
        handled_skip = app.execute_slash_command("/skip")
        assert handled_skip is True
        assert app.state_machine.current_step == OnboardingStep.DOCTOR

        # Test /skip command again (advances from DOCTOR to QUESTIONNAIRE)
        handled_skip2 = app.execute_slash_command("/skip")
        assert handled_skip2 is True
        assert app.state_machine.current_step == OnboardingStep.QUESTIONNAIRE

        # Test /doctor jump
        handled_doc = app.execute_slash_command("/doctor")
        assert handled_doc is True
        assert app.state_machine.current_step == OnboardingStep.DOCTOR

        # Test /back command (returns to previous step in history: QUESTIONNAIRE)
        handled_back = app.execute_slash_command("/back")
        assert handled_back is True
        assert app.state_machine.current_step == OnboardingStep.QUESTIONNAIRE


@pytest.mark.asyncio
async def test_auth_error_validation_and_recovery():
    state = UserSetupState(current_step=OnboardingStep.AUTH)
    app = SubstrateOnboardingApp(initial_state=state)

    async with app.run_test() as pilot:
        # Move directly to Auth screen
        app.state_machine.transition_to(OnboardingStep.AUTH)
        await pilot.pause(0.05)
        assert isinstance(app.screen, AuthScreen)

        auth_screen: AuthScreen = app.screen
        error_banner = auth_screen.query_one("#auth-error-banner", InlineErrorBanner)
        key_input = auth_screen.query_one("#api-key-input", Input)

        # 1. Attempt submitting with empty key -> error banner visible
        auth_screen.action_submit_credentials()
        await pilot.pause(0.05)
        assert error_banner.has_class("-visible")
        assert app.state_machine.current_step == OnboardingStep.AUTH

        # 2. Attempt invalid short key -> error banner visible
        key_input.value = "abc"
        auth_screen.action_submit_credentials()
        await pilot.pause(0.05)
        assert error_banner.has_class("-visible")
        assert app.state_machine.current_step == OnboardingStep.AUTH

        # 3. Enter valid Substrate API key -> advances to Summary
        key_input.value = "sb-live-1234567890abcdef"
        auth_screen.action_submit_credentials()
        await pilot.pause(0.1)
        assert not error_banner.has_class("-visible")
        assert app.state_machine.current_step == OnboardingStep.SUMMARY
        assert app.state.auth_mode == "api_key"
        assert app.state.api_key_masked.startswith("sb-l")


@pytest.mark.asyncio
async def test_exit_modal_interactions():
    app = SubstrateOnboardingApp()
    async with app.run_test() as pilot:
        # Trigger Ctrl+C / request exit
        app.action_request_exit()
        await pilot.pause(0.05)
        assert isinstance(app.screen, ExitConfirmModal)

        # Press 'n' to cancel exit
        await pilot.press("n")
        await pilot.pause(0.05)
        assert not isinstance(app.screen, ExitConfirmModal)
        assert app.is_running is True


@pytest.mark.asyncio
async def test_oauth_auth_flow():
    state = UserSetupState(current_step=OnboardingStep.AUTH)
    app = SubstrateOnboardingApp(initial_state=state)

    async with app.run_test() as pilot:
        app.state_machine.transition_to(OnboardingStep.AUTH)
        await pilot.pause(0.05)
        assert isinstance(app.screen, AuthScreen)

        auth_screen: AuthScreen = app.screen
        # Trigger OAuth flow
        auth_screen.action_start_oauth()
        # Wait for handshake simulation to complete
        await pilot.pause(3.0)

        assert app.state.auth_mode == "oauth"
        assert app.state_machine.current_step == OnboardingStep.SUMMARY
