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
        - '?' is zero or one
        - '&' is intersection
    """

    nfa_stack = []

    for char in postfix_regex:

        # 1. OPERAND (a, b, c, ...)
        if char not in {'.', '|', '*', '+', '?', '&'}:
            start = State()
            accept = State(is_accepting=True)
            start.add_transition(char, accept)
            nfa_stack.append(NFA(start, accept))

        # 2. CONCATENATION
        elif char == '.':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()

            nfa1.accept_state.is_accepting = False
            nfa1.accept_state.add_transition("eps", nfa2.start_state)

            new_nfa = NFA(nfa1.start_state, nfa2.accept_state)
            nfa_stack.append(new_nfa)


        # 3. UNION
        elif char == '|':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()

            start = State()
            accept = State(is_accepting=True)

            start.add_transition("eps", nfa1.start_state)
            start.add_transition("eps", nfa2.start_state)

            nfa1.accept_state.is_accepting = False
            nfa2.accept_state.is_accepting = False

            nfa1.accept_state.add_transition("eps", accept)
            nfa2.accept_state.add_transition("eps", accept)

            new_nfa = NFA(start, accept)
            nfa_stack.append(new_nfa)

        # 4. KLEENE STAR (*)
        elif char == '*':
            nfa1 = nfa_stack.pop()

            start = State()
            accept = State(is_accepting=True)

            start.add_transition("eps", nfa1.start_state)
            start.add_transition("eps", accept)

            nfa1.accept_state.is_accepting = False
            nfa1.accept_state.add_transition("eps", nfa1.start_state)
            nfa1.accept_state.add_transition("eps", accept)

            new_nfa = NFA(start, accept)
            nfa_stack.append(new_nfa)


        # 5. KLEENE PLUS (+)
        elif char == '+':
            nfa1 = nfa_stack.pop()

            start = State()
            accept = State(is_accepting=True)

            start.add_transition("eps", nfa1.start_state)

            nfa1.accept_state.is_accepting = False
            nfa1.accept_state.add_transition("eps", nfa1.start_state)
            nfa1.accept_state.add_transition("eps", accept)

            new_nfa = NFA(start, accept)
            nfa_stack.append(new_nfa)

        #  EX: a?  →  (a | ε)
        elif char == '?':
            nfa1 = nfa_stack.pop()

            start = State()
            accept = State(is_accepting=True)

            # either skip or take nfa1
            start.add_transition("eps", nfa1.start_state)
            start.add_transition("eps", accept)

            nfa1.accept_state.is_accepting = False
            nfa1.accept_state.add_transition("eps", accept)

            new_nfa = NFA(start, accept)
            nfa_stack.append(new_nfa)

        #  Build cross-product NFA
        #  Accepts only if BOTH NFAs accept.
        elif char == '&':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()

            # Cross-product mapping (State1, State2) → NewState
            state_map = {}

            def get_pair_state(s1, s2):
                if (s1, s2) not in state_map:
                    state_map[(s1, s2)] = State()
                return state_map[(s1, s2)]

            # Start state is the pair (start1, start2)
            start = get_pair_state(nfa1.start_state, nfa2.start_state)

            # BFS queue
            queue = [(nfa1.start_state, nfa2.start_state)]
            visited = set(queue)

            while queue:
                s1, s2 = queue.pop(0)
                combined_state = get_pair_state(s1, s2)

                # Find all transitions possible
                for label1, targets1 in s1.transitions.items():
                    for label2, targets2 in s2.transitions.items():

                        # Intersection requires same label (except epsilon)
                        if label1 == label2:
                            for t1 in targets1:
                                for t2 in targets2:
                                    ns = get_pair_state(t1, t2)
                                    combined_state.add_transition(label1, ns)

                                    if (t1, t2) not in visited:
                                        visited.add((t1, t2))
                                        queue.append((t1, t2))

            # Accepting states = any pair where both are accepting
            accept = State(is_accepting=True)

            for (s1, s2), new_s in state_map.items():
                if s1.is_accepting and s2.is_accepting:
                    new_s.add_transition("eps", accept)

            new_nfa = NFA(start, accept)
            nfa_stack.append(new_nfa)

        else:
            raise ValueError(f"Unexpected character in postfix regex: {char}")

    if len(nfa_stack) != 1:
        raise ValueError("Invalid postfix expression: stack does not contain exactly one NFA at the end.")

    return nfa_stack.pop()
