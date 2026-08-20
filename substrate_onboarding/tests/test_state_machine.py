"""Unit tests for OnboardingStateMachine with Pre-existing Cluster, Private GA Agreement, and WorkerPool CCC."""

import pytest
from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.engine.state_machine import OnboardingStateMachine


def test_state_machine_initialization():
    sm = OnboardingStateMachine()
    assert sm.current_step == OnboardingStep.WELCOME
    assert sm.step_number() == 0
    assert not sm.state.is_complete


def test_state_machine_sequential_transitions():
    sm = OnboardingStateMachine()
    transitions = []

    sm.add_listener(lambda old_s, new_s: transitions.append((old_s, new_s)))

    expected_steps = [
        OnboardingStep.CHECK_SETUP,
        OnboardingStep.CONNECT_CLUSTER,
        OnboardingStep.PRIVATE_GA_AGREEMENT,
        OnboardingStep.TURN_ON_SUBSTRATE,
        OnboardingStep.COMPATIBLE_NODEPOOL,
        OnboardingStep.CONFIG_AUTOSCALING,
        OnboardingStep.DEPLOY_WORKERPOOL,
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
    assert len(transitions) == len(expected_steps)


def test_state_machine_previous_step():
    sm = OnboardingStateMachine()
    sm.next_step()  # To CHECK_SETUP
    sm.next_step()  # To CONNECT_CLUSTER

    assert sm.current_step == OnboardingStep.CONNECT_CLUSTER
    prev = sm.previous_step()
    assert prev == OnboardingStep.CHECK_SETUP
    assert sm.current_step == OnboardingStep.CHECK_SETUP

    prev = sm.previous_step()
    assert prev == OnboardingStep.WELCOME
    assert sm.current_step == OnboardingStep.WELCOME


def test_state_machine_direct_transition():
    sm = OnboardingStateMachine()
    res = sm.transition_to(OnboardingStep.CONNECT_CLUSTER)
    assert res is True
    assert sm.current_step == OnboardingStep.CONNECT_CLUSTER

    # Transitioning to same step returns False
    res2 = sm.transition_to(OnboardingStep.CONNECT_CLUSTER)
    assert res2 is False
