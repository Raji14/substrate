"""Unit tests for OnboardingStateMachine with Option A PRFAQ sequencing."""

import pytest
from substrate_onboarding.config import OnboardingStep, UserSetupState
from substrate_onboarding.engine.state_machine import OnboardingStateMachine


def test_state_machine_initialization():
    sm = OnboardingStateMachine()
    assert sm.current_step == OnboardingStep.WELCOME
    assert sm.step_number() == 1
    assert not sm.state.is_complete


def test_state_machine_sequential_transitions():
    sm = OnboardingStateMachine()
    transitions = []

    sm.add_listener(lambda old_s, new_s: transitions.append((old_s, new_s)))

    step = sm.next_step()
    assert step == OnboardingStep.DOCTOR
    assert sm.current_step == OnboardingStep.DOCTOR
    assert sm.step_number() == 2

    step = sm.next_step()
    assert step == OnboardingStep.QUESTIONNAIRE
    assert sm.current_step == OnboardingStep.QUESTIONNAIRE

    step = sm.next_step()
    assert step == OnboardingStep.AUTH
    assert sm.current_step == OnboardingStep.AUTH

    step = sm.next_step()
    assert step == OnboardingStep.SUMMARY
    assert sm.current_step == OnboardingStep.SUMMARY

    step = sm.next_step()
    assert step == OnboardingStep.COMPLETE
    assert sm.state.is_complete

    assert len(transitions) == 5


def test_state_machine_previous_step():
    sm = OnboardingStateMachine()
    sm.next_step()  # To DOCTOR
    sm.next_step()  # To QUESTIONNAIRE

    assert sm.current_step == OnboardingStep.QUESTIONNAIRE
    prev = sm.previous_step()
    assert prev == OnboardingStep.DOCTOR
    assert sm.current_step == OnboardingStep.DOCTOR

    prev = sm.previous_step()
    assert prev == OnboardingStep.WELCOME
    assert sm.current_step == OnboardingStep.WELCOME


def test_state_machine_direct_transition():
    sm = OnboardingStateMachine()
    res = sm.transition_to(OnboardingStep.DOCTOR)
    assert res is True
    assert sm.current_step == OnboardingStep.DOCTOR

    # Transitioning to same step returns False
    res2 = sm.transition_to(OnboardingStep.DOCTOR)
    assert res2 is False
