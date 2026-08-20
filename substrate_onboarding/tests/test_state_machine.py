"""Unit tests for OnboardingStateMachine with 8-Step Interactive Journey."""

import pytest
from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.engine.state_machine import OnboardingStateMachine


def test_state_machine_initialization():
    sm = OnboardingStateMachine()
    assert sm.current_step == OnboardingStep.CHECK_SETUP
    assert sm.step_number() == 1
    assert not sm.state.is_complete


def test_state_machine_sequential_transitions():
    sm = OnboardingStateMachine()
    transitions = []

    sm.add_listener(lambda old_s, new_s: transitions.append((old_s, new_s)))

    expected_steps = [
        OnboardingStep.CREATE_CLUSTER,
        OnboardingStep.TURN_ON_SUBSTRATE,
        OnboardingStep.INSTALL_CLI,
        OnboardingStep.FIRST_ACTOR,
        OnboardingStep.SEND_REQUEST,
        OnboardingStep.PAUSE_RESUME,
        OnboardingStep.SCALE_UP,
        OnboardingStep.COMPLETE,
    ]

    for expected in expected_steps:
        step = sm.next_step()
        assert step == expected

    assert sm.state.is_complete
    assert len(transitions) == 8


def test_state_machine_previous_step():
    sm = OnboardingStateMachine()
    sm.next_step()  # To CREATE_CLUSTER
    sm.next_step()  # To TURN_ON_SUBSTRATE

    assert sm.current_step == OnboardingStep.TURN_ON_SUBSTRATE
    prev = sm.previous_step()
    assert prev == OnboardingStep.CREATE_CLUSTER
    assert sm.current_step == OnboardingStep.CREATE_CLUSTER

    prev = sm.previous_step()
    assert prev == OnboardingStep.CHECK_SETUP
    assert sm.current_step == OnboardingStep.CHECK_SETUP


def test_state_machine_direct_transition():
    sm = OnboardingStateMachine()
    res = sm.transition_to(OnboardingStep.CREATE_CLUSTER)
    assert res is True
    assert sm.current_step == OnboardingStep.CREATE_CLUSTER

    # Transitioning to same step returns False
    res2 = sm.transition_to(OnboardingStep.CREATE_CLUSTER)
    assert res2 is False
