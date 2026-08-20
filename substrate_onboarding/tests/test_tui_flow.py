"""End-to-end headless Textual test suite for Substrate Onboarding TUI with 8-step journey."""

import pytest
from substrate_onboarding.app import SubstrateOnboardingApp
from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.screens.step_screen import GenericStepScreen


@pytest.mark.asyncio
async def test_tui_full_flow():
    state = UserSetupState()
    app = SubstrateOnboardingApp(initial_state=state)

    async with app.run_test() as pilot:
        # Step 1: Check your setup
        assert app.state_machine.current_step == OnboardingStep.CHECK_SETUP
        assert isinstance(app.screen, GenericStepScreen)

        # Step 2: Create a cluster
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.CREATE_CLUSTER

        # Step 3: Turn on Substrate
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.TURN_ON_SUBSTRATE

        # Step 4: Install the CLI
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.INSTALL_CLI

        # Step 5: First actor
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.FIRST_ACTOR

        # Step 6: Send a request
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.SEND_REQUEST

        # Step 7: Pause & resume
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.PAUSE_RESUME

        # Step 8: Scale it up
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.SCALE_UP

        # Finish onboarding
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state.is_complete is True


@pytest.mark.asyncio
async def test_tui_help_modal():
    app = SubstrateOnboardingApp()
    async with app.run_test() as pilot:
        initial_depth = len(app.screen_stack)
        await pilot.press("f1")
        await pilot.pause(0.05)
        assert len(app.screen_stack) == initial_depth + 1
        # Close help modal with escape
        await pilot.press("escape")
        await pilot.pause(0.05)
        assert len(app.screen_stack) == initial_depth
