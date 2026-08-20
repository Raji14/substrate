"""End-to-end headless Textual test suite for Substrate Onboarding TUI with 6-step Day-0 sequencing."""

import pytest
from substrate_onboarding.app import SubstrateOnboardingApp
from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.screens.welcome_screen import WelcomeScreen
from substrate_onboarding.screens.doctor_screen import DoctorScreen
from substrate_onboarding.screens.wizard_screen import QuestionnaireScreen
from substrate_onboarding.screens.auth_screen import AuthScreen
from substrate_onboarding.screens.deploy_wp_screen import DeployWorkerPoolScreen
from substrate_onboarding.screens.summary_screen import SummaryScreen


@pytest.mark.asyncio
async def test_tui_full_flow():
    state = UserSetupState()
    app = SubstrateOnboardingApp(initial_state=state)

    async with app.run_test() as pilot:
        # 1. Verify Step 1: Cluster Detection Screen
        assert app.state_machine.current_step == OnboardingStep.CLUSTER
        assert isinstance(app.screen, WelcomeScreen)

        # Press Enter to select cluster -> goes to Step 2: Control Plane
        await pilot.press("enter")
        await pilot.pause(0.1)

        # 2. Verify Step 2: Control Plane Screen
        assert app.state_machine.current_step == OnboardingStep.CONTROL_PLANE
        assert isinstance(app.screen, DoctorScreen)

        # Advance to Step 3: Node Pool & CCC
        await pilot.press("enter")
        await pilot.pause(0.1)

        # 3. Verify Step 3: Node Pool Screen
        assert app.state_machine.current_step == OnboardingStep.NODE_POOL
        assert isinstance(app.screen, QuestionnaireScreen)

        # Select option and advance to Step 4: Autoscaling
        await pilot.press("enter")
        await pilot.pause(0.1)

        # 4. Verify Step 4: Autoscaling Screen
        assert app.state_machine.current_step == OnboardingStep.AUTOSCALING
        assert isinstance(app.screen, AuthScreen)

        # Advance to Step 5: Deploy WorkerPool
        await pilot.press("enter")
        await pilot.pause(0.1)

        # 5. Verify Step 5: Deploy WorkerPool Screen
        assert app.state_machine.current_step == OnboardingStep.DEPLOY_WORKERPOOL
        assert isinstance(app.screen, DeployWorkerPoolScreen)

        # Advance to Step 6: Launchpad & Verification
        await pilot.press("enter")
        await pilot.pause(0.1)

        # 6. Verify Step 6: Launchpad Screen
        assert app.state_machine.current_step == OnboardingStep.LAUNCHPAD
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
