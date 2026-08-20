"""End-to-end headless Textual test suite for Substrate Onboarding TUI with Option A PRFAQ sequencing."""

import pytest
from substrate_onboarding.app import SubstrateOnboardingApp
from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.screens.welcome_screen import WelcomeScreen
from substrate_onboarding.screens.wizard_screen import QuestionnaireScreen
from substrate_onboarding.screens.doctor_screen import DoctorScreen
from substrate_onboarding.screens.auth_screen import AuthScreen
from substrate_onboarding.screens.summary_screen import SummaryScreen


@pytest.mark.asyncio
async def test_tui_full_flow():
    state = UserSetupState()
    app = SubstrateOnboardingApp(initial_state=state)

    async with app.run_test() as pilot:
        # 1. Verify Welcome screen
        assert app.state_machine.current_step == OnboardingStep.WELCOME
        assert isinstance(app.screen, WelcomeScreen)

        # Press Enter to start setup -> goes to Step 1: Pre-Flight Doctor
        await pilot.press("enter")
        await pilot.pause(0.1)

        # 2. Verify Doctor screen (Step 1)
        assert app.state_machine.current_step == OnboardingStep.DOCTOR
        assert isinstance(app.screen, DoctorScreen)

        # Advance to Questionnaire screen (Step 2: Platform Setup)
        await pilot.press("enter")
        await pilot.pause(0.1)

        # 3. Verify Questionnaire screen (Step 2)
        assert app.state_machine.current_step == OnboardingStep.QUESTIONNAIRE
        assert isinstance(app.screen, QuestionnaireScreen)

        # Step 2.1: Down arrow and Enter
        await pilot.press("down")
        await pilot.press("enter")
        await pilot.pause(0.05)

        # Step 2.2: Enter
        await pilot.press("enter")
        await pilot.pause(0.05)

        # Step 2.3: Enter -> Auth screen (Step 3: Agent Deployment)
        await pilot.press("enter")
        await pilot.pause(0.1)

        # 4. Verify Auth screen (Step 3)
        assert app.state_machine.current_step == OnboardingStep.AUTH
        assert isinstance(app.screen, AuthScreen)

        # Skip credentials for offline local mode -> Summary screen (Step 4: Launchpad)
        auth_screen = app.screen
        auth_screen.action_skip_auth()
        await pilot.pause(0.1)

        # 5. Verify Summary screen (Step 4)
        assert app.state_machine.current_step == OnboardingStep.SUMMARY
        assert isinstance(app.screen, SummaryScreen)

        # Complete onboarding
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
