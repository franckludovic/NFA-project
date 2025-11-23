# tests/test_converter.py

import pytest
from src.converter import postfix_to_nfa
from src.nfa_structure import State, NFA


def collect_all_states(start_state):
    """Helper BFS traversal to gather all reachable states."""
    visited = set()
    queue = [start_state]

    while queue:
        state = queue.pop(0)
        if state not in visited:
            visited.add(state)
            for targets in state.transitions.values():
                for next_state in targets:
                    queue.append(next_state)
    return visited


def test_single_operand_nfa():
    nfa = postfix_to_nfa("a")

    # Start must have a single outgoing transition on 'a'
    assert "a" in nfa.start_state.transitions
    assert len(nfa.start_state.transitions["a"]) == 1
    assert nfa.accept_state in nfa.start_state.transitions["a"]

    # Accept state must be accepting
    assert nfa.accept_state.is_accepting is True

def test_concatenation():
    # postfix for "ab"
    nfa = postfix_to_nfa("ab.")

    states = collect_all_states(nfa.start_state)

    # There should be 4 states (a_start, a_accept, b_start, b_accept)
    assert len(states) == 4

    # Check epsilon from a_accept to b_start
    a_accept = list(nfa.start_state.transitions["a"])[0]
    assert "eps" in a_accept.transitions



def test_union():
    # postfix for "a|b"
    nfa = postfix_to_nfa("ab|")

    states = collect_all_states(nfa.start_state)

    # At least 4 states (start, a-fragment, b-fragment, final)
    assert len(states) >= 4

    # Start should have epsilon transitions to both a and b branches
    eps_targets = nfa.start_state.transitions.get("eps", set())
    assert len(eps_targets) == 2


def test_kleene_star():
    # postfix for "a*"
    nfa = postfix_to_nfa("a*")

    states = collect_all_states(nfa.start_state)

    # Start must have two epsilon transitions:
    #   to old_start AND to new_accept
    eps_targets = nfa.start_state.transitions.get("eps", set())
    assert len(eps_targets) == 2


def test_complex_expression():
    # postfix for (a|b)*c = "ab|*c."
    nfa = postfix_to_nfa("ab|*c.")

    states = collect_all_states(nfa.start_state)

    # Final accept state should be accepting
    assert nfa.accept_state.is_accepting is True

    # There must be multiple states (>=6)
    assert len(states) >= 6
