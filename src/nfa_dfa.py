# src/nfa_to_dfa.py

from collections import deque

class DFAState:
    """Represents a DFA state, which is a set of NFA states."""
    def __init__(self, nfa_states):
        self.nfa_states = frozenset(nfa_states)  # Immutable set for dict keys
        self.transitions = {}                     # symbol -> DFAState
        self.is_accept = any(s.is_accepting for s in nfa_states)

    def __repr__(self):
        return f"DFAState({[s.id for s in self.nfa_states]})"


def epsilon_closure(states):
    """Return ε-closure of a set of NFA states."""
    stack = list(states)
    closure = set(states)

    while stack:
        state = stack.pop()
        if '' in state.transitions:
            for nxt in state.transitions['']:
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
    return closure


def move(states, symbol):
    """Return the set of NFA states reachable on a symbol."""
    result = set()
    for s in states:
        if symbol in s.transitions:
            result.update(s.transitions[symbol])
    return result


def collect_all_states(start_state):
    """Return a set of all states reachable from start_state."""
    visited = set()
    stack = [start_state]

    while stack:
        s = stack.pop()
        if s not in visited:
            visited.add(s)
            for targets in s.transitions.values():
                stack.extend(targets)
    return visited


def nfa_to_dfa(nfa):
    """
    Convert an NFA into a DFA using subset construction.
    Returns the start DFA state and a dict of all DFA states.
    """
    start_closure = frozenset(epsilon_closure({nfa.start_state}))
    start_dfa = DFAState(start_closure)

    dfa_states = {start_closure: start_dfa}
    queue = deque([start_dfa])

    # Collect alphabet from all reachable NFA states (ignore epsilon)
    alphabet = set()
    for s in collect_all_states(nfa.start_state):
        for symbol in s.transitions:
            if symbol != '':
                alphabet.add(symbol)

    while queue:
        dfa_state = queue.pop()

        for symbol in alphabet:
            # Move on symbol, then take epsilon-closure
            target_states = epsilon_closure(move(dfa_state.nfa_states, symbol))
            if not target_states:
                continue

            frozen = frozenset(target_states)
            if frozen not in dfa_states:
                new_dfa = DFAState(target_states)
                dfa_states[frozen] = new_dfa
                queue.append(new_dfa)

            dfa_state.transitions[symbol] = dfa_states[frozen]

    return start_dfa, dfa_states
