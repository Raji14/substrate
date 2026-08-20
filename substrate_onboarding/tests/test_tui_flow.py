"""End-to-end headless Textual test suite for Substrate Onboarding TUI with Welcome Screen & 12 steps."""

import pytest
from substrate_onboarding.app import SubstrateOnboardingApp
from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.screens.welcome_screen import WelcomeScreen
from substrate_onboarding.screens.step_screen import GenericStepScreen


@pytest.mark.asyncio
async def test_tui_full_flow():
    state = UserSetupState(current_step=OnboardingStep.WELCOME)
    app = SubstrateOnboardingApp(initial_state=state)

    async with app.run_test() as pilot:
        # Step 0: Welcome Screen
        assert app.state_machine.current_step == OnboardingStep.WELCOME
        assert isinstance(app.screen, WelcomeScreen)

        # Step 1: Check your setup
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.CHECK_SETUP
        assert isinstance(app.screen, GenericStepScreen)

        # Step 2: Connect pre-existing cluster (portability)
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.CONNECT_CLUSTER

        # Step 3: Private GA Agreement (gated access & terms)
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.PRIVATE_GA_AGREEMENT

        # Step 4: Turn on Substrate
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.TURN_ON_SUBSTRATE

        # Step 5: Compatible Node Pool (CCC / Nested-Virt)
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.COMPATIBLE_NODEPOOL

        # Step 6: Configure Autoscaling (HPA & CapacityBuffer)
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.CONFIG_AUTOSCALING

        # Step 7: Deploy WorkerPool
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.DEPLOY_WORKERPOOL

        # Step 8: Install the CLI
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.INSTALL_CLI

        # Step 9: First actor
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.FIRST_ACTOR

        # Step 10: Send a request
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.SEND_REQUEST

        # Step 11: Pause & resume
        await pilot.press("enter")
        await pilot.pause(0.1)
        assert app.state_machine.current_step == OnboardingStep.PAUSE_RESUME

        # Step 12: Scale it up
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
