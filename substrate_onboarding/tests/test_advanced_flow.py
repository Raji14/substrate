"""Advanced interaction tests for slash commands, modals, and navigation."""

import pytest
from substrate_onboarding.app import SubstrateOnboardingApp
from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.screens.exit_modal import ExitConfirmModal
from substrate_onboarding.screens.help_modal import HelpModal


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

        # Test /skip command (advances from CLUSTER to CONTROL_PLANE)
        handled_skip = app.execute_slash_command("/skip")
        assert handled_skip is True
        assert app.state_machine.current_step == OnboardingStep.CONTROL_PLANE

        # Test /skip command again (advances from CONTROL_PLANE to NODE_POOL)
        handled_skip2 = app.execute_slash_command("/skip")
        assert handled_skip2 is True
        assert app.state_machine.current_step == OnboardingStep.NODE_POOL

        # Test /doctor jump
        handled_doc = app.execute_slash_command("/doctor")
        assert handled_doc is True
        assert app.state_machine.current_step == OnboardingStep.CONTROL_PLANE

        # Test /back command (returns to previous step in history: NODE_POOL)
        handled_back = app.execute_slash_command("/back")
        assert handled_back is True
        assert app.state_machine.current_step == OnboardingStep.NODE_POOL


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
