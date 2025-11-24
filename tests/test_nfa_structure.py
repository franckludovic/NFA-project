# tests/test_nfa_structure.py

import pytest
from src.nfa_structure import State, NFA


def test_state_creation_defaults():
    s = State()
    assert s.is_accepting is False
    assert isinstance(s.transitions, dict)
    assert len(s.transitions) == 0


def test_state_creation_accepting():
    s = State(is_accepting=True)
    assert s.is_accepting is True


def test_add_single_transition():
    s1 = State()
    s2 = State()

    s1.add_transition('a', s2)

    assert 'a' in s1.transitions
    assert s2 in s1.transitions['a']


def test_add_multiple_transitions_same_symbol():
    s1 = State()
    s2 = State()
    s3 = State()

    s1.add_transition('a', s2)
    s1.add_transition('a', s3)

    assert len(s1.transitions['a']) == 2
    assert s2 in s1.transitions['a']
    assert s3 in s1.transitions['a']


def test_nfa_class_structure():
    start = State()
    accept = State(is_accepting=True)
    nfa = NFA(start, accept)

    assert nfa.start_state is start
    assert nfa.accept_state is accept
