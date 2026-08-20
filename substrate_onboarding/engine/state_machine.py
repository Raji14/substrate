"""State Machine for Onboarding Workflow with Option A PRFAQ sequencing."""

from __future__ import annotations

from typing import Callable, List, Optional
from substrate_onboarding.config import OnboardingStep, UserSetupState


class OnboardingStateMachine:
    """Manages consecutive onboarding state transitions with history and rollback support.
    
    Option A Step Order:
      0. Welcome (Hero Splash)
      1. Pre-Flight Doctor (GKE Context & Prereqs)
      2. Platform Setup (WorkerPools & Isolation)
      3. Agent Deployment (ActorTemplates & Credentials)
      4. Launchpad (Summary, atectl top, precache & ready state)
      5. Complete
    """

    STEPS_ORDER: List[OnboardingStep] = [
        OnboardingStep.WELCOME,
        OnboardingStep.DOCTOR,
        OnboardingStep.QUESTIONNAIRE,
        OnboardingStep.AUTH,
        OnboardingStep.SUMMARY,
        OnboardingStep.COMPLETE,
    ]

    def __init__(self, state: Optional[UserSetupState] = None):
        self.state = state or UserSetupState()
        self.history: List[OnboardingStep] = []
        self._listeners: List[Callable[[OnboardingStep, OnboardingStep], None]] = []

    @property
    def current_step(self) -> OnboardingStep:
        return self.state.current_step

    def add_listener(self, listener: Callable[[OnboardingStep, OnboardingStep], None]) -> None:
        """Register a callback when state transitions occur."""
        self._listeners.append(listener)

    def transition_to(self, new_step: OnboardingStep) -> bool:
        """Transition to a specific step, updating history and notifying listeners."""
        old_step = self.state.current_step
        if old_step == new_step:
            return False

        self.history.append(old_step)
        self.state.current_step = new_step

        if new_step == OnboardingStep.COMPLETE:
            self.state.is_complete = True

        for listener in self._listeners:
            listener(old_step, new_step)
        return True

    def next_step(self) -> Optional[OnboardingStep]:
        """Advance to the subsequent onboarding step."""
        try:
            curr_idx = self.STEPS_ORDER.index(self.current_step)
            if curr_idx < len(self.STEPS_ORDER) - 1:
                next_step = self.STEPS_ORDER[curr_idx + 1]
                self.transition_to(next_step)
                return next_step
        except ValueError:
            pass
        return None

    def previous_step(self) -> Optional[OnboardingStep]:
        """Rollback to the previous onboarding step if history exists."""
        if not self.history:
            # Fallback to previous in linear order
            try:
                curr_idx = self.STEPS_ORDER.index(self.current_step)
                if curr_idx > 0:
                    prev = self.STEPS_ORDER[curr_idx - 1]
                    self.transition_to(prev)
                    return prev
            except ValueError:
                pass
            return None

        prev_step = self.history.pop()
        old_step = self.state.current_step
        self.state.current_step = prev_step

        for listener in self._listeners:
            listener(old_step, prev_step)
        return prev_step

    def step_number(self) -> int:
        """Returns 1-based current step index (excluding complete)."""
        try:
            return self.STEPS_ORDER.index(self.current_step) + 1
        except ValueError:
            return 1

    def total_steps(self) -> int:
        """Total number of visible interactive onboarding steps (4 core steps)."""
        return len(self.STEPS_ORDER) - 1
