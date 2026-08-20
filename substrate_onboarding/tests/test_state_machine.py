"""Unit tests for OnboardingStateMachine with 6-step Day-0 sequencing."""

import pytest
from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.engine.state_machine import OnboardingStateMachine


def test_state_machine_initialization():
    sm = OnboardingStateMachine()
    assert sm.current_step == OnboardingStep.CLUSTER
    assert sm.step_number() == 1
    assert not sm.state.is_complete


def test_state_machine_sequential_transitions():
    sm = OnboardingStateMachine()
    transitions = []

    sm.add_listener(lambda old_s, new_s: transitions.append((old_s, new_s)))

    step = sm.next_step()
    assert step == OnboardingStep.CONTROL_PLANE
    assert sm.current_step == OnboardingStep.CONTROL_PLANE
    assert sm.step_number() == 2

    step = sm.next_step()
    assert step == OnboardingStep.NODE_POOL
    assert sm.current_step == OnboardingStep.NODE_POOL

    step = sm.next_step()
    assert step == OnboardingStep.AUTOSCALING
    assert sm.current_step == OnboardingStep.AUTOSCALING

    step = sm.next_step()
    assert step == OnboardingStep.DEPLOY_WORKERPOOL
    assert sm.current_step == OnboardingStep.DEPLOY_WORKERPOOL

    step = sm.next_step()
    assert step == OnboardingStep.LAUNCHPAD
    assert sm.current_step == OnboardingStep.LAUNCHPAD

    step = sm.next_step()
    assert step == OnboardingStep.COMPLETE
    assert sm.state.is_complete

    assert len(transitions) == 6


def test_state_machine_previous_step():
    sm = OnboardingStateMachine()
    sm.next_step()  # To CONTROL_PLANE
    sm.next_step()  # To NODE_POOL

    assert sm.current_step == OnboardingStep.NODE_POOL
    prev = sm.previous_step()
    assert prev == OnboardingStep.CONTROL_PLANE
    assert sm.current_step == OnboardingStep.CONTROL_PLANE

    prev = sm.previous_step()
    assert prev == OnboardingStep.CLUSTER
    assert sm.current_step == OnboardingStep.CLUSTER


def test_state_machine_direct_transition():
    sm = OnboardingStateMachine()
    res = sm.transition_to(OnboardingStep.CONTROL_PLANE)
    assert res is True
    assert sm.current_step == OnboardingStep.CONTROL_PLANE

    # Transitioning to same step returns False
    res2 = sm.transition_to(OnboardingStep.CONTROL_PLANE)
    assert res2 is False
