# franck

class State:
    """
    Represents one state in an NFA.
    Each state may have multiple transitions on different symbols.
    """
    _counter = 0
    def __init__(self, is_accepting: bool = False):
        self.id = State._counter
        State._counter += 1
        self.is_accepting = is_accepting

        # transitions is a dictionary:
        # key   -> symbol (str)
        # value -> set of next State objects
        self.transitions = {}
        
    def add_transition(self, symbol: str, next_state: 'State'):
        """
        Add a transition on `symbol` to `next_state`.
        Multiple states may exist for the same symbol → use a set.
        """
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(next_state)
class NFA:
    """
    Simple container for an NFA fragment.
    Used by Thompson's construction as building blocks.
    """
    def __init__(self, start_state: State, accept_state: State):
        self.start_state = start_state
        self.accept_state = accept_state
