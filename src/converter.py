# franck

from src.nfa_structure import State, NFA


def postfix_to_nfa(postfix_regex: str) -> NFA:
    """
    Convert a postfix regular expression into an NFA using Thompson's construction.

    Supported operators:
        - symbol (a, b, c ...)
        - '.' is concatenation
        - '|' is union
        - '*' is kleene star (zero or more)
        - '+' is kleene plus (one or more)
    """

    # Stack used by Thompson's construction.
    # Each entry is an NFA fragment.
    nfa_stack = []

    # Process the postfix regex one character at a time
    for char in postfix_regex:


        # 1. OPERAND (a, b, c, ...)
        # Create a simple fragment:
        #   start --char--> accept

        if char not in {'.', '|', '*', '+'}:
            start = State()                          # new start state
            accept = State(is_accepting=True)        # new accept state
            start.add_transition(char, accept)       # char transition start to accept
            
            nfa_stack.append(NFA(start, accept))     # push fragment onto the stack


        # 2. OPERATORS

        elif char == '.':
            nfa2 = nfa_stack.pop()                   # second fragment
            nfa1 = nfa_stack.pop()                   # first fragment

            # nfa1.accept is no longer the final accepting state
            nfa1.accept_state.is_accepting = False

            # Add epsilon transition connecting the two fragments
            nfa1.accept_state.add_transition("eps", nfa2.start_state)

            # Combined NFA start = nfa1.start, accept = nfa2.accept
            new_nfa = NFA(start_state=nfa1.start_state,
                          accept_state=nfa2.accept_state)

            nfa_stack.append(new_nfa)


        elif char == '|':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()

            start = State()                          # new start state
            accept = State(is_accepting=True)        # new accept state

            # New start branches into both fragments
            start.add_transition("eps", nfa1.start_state)
            start.add_transition("eps", nfa2.start_state)

            # Neither old accept state is final anymore
            nfa1.accept_state.is_accepting = False
            nfa2.accept_state.is_accepting = False

            # Both fragments connect into the new accept
            nfa1.accept_state.add_transition("eps", accept)
            nfa2.accept_state.add_transition("eps", accept)

            new_nfa = NFA(start_state=start, accept_state=accept)
            nfa_stack.append(new_nfa)


        elif char == '*':
            nfa1 = nfa_stack.pop()

            start = State()                          # new start state
            accept = State(is_accepting=True)        # new accept state

            # Can skip the loop entirely
            start.add_transition("eps", nfa1.start_state)
            start.add_transition("eps", accept)

            # nfa1.accept is no longer final
            nfa1.accept_state.is_accepting = False

            # Loop back to start OR go to new accept
            nfa1.accept_state.add_transition("eps", nfa1.start_state)
            nfa1.accept_state.add_transition("eps", accept)

            new_nfa = NFA(start_state=start, accept_state=accept)
            nfa_stack.append(new_nfa)


        elif char == '+':
            nfa1 = nfa_stack.pop()

            start = State()                          # new start state
            accept = State(is_accepting=True)        # new accept state

            # Must enter nfa1 at least once
            start.add_transition("eps", nfa1.start_state)

            # Loop for repeated repetitions
            nfa1.accept_state.add_transition("eps", nfa1.start_state)

            # Exit after one or many repetitions
            nfa1.accept_state.add_transition("eps", accept)

            # old accept no longer final
            nfa1.accept_state.is_accepting = False

            new_nfa = NFA(start_state=start, accept_state=accept)
            nfa_stack.append(new_nfa)


        else:
            raise ValueError(f"Unexpected character in postfix regex: {char}")

    # At the end, there should be exactly one NFA on the stack
    if len(nfa_stack) != 1:
        raise ValueError("Invalid postfix expression: stack does not contain exactly one NFA at the end.")

    return nfa_stack.pop()
