# taku
from graphviz import Digraph
from src.nfa_structure import NFA, State


def display_nfa(nfa: NFA, output_filename: str = "nfa_graph") -> None:
    """
    Traverses the NFA and draws it as an image using Graphviz.

    Parameters:
        nfa (NFA): The NFA to visualize.
        output_filename (str): Name of the image file (no extension).

    Returns:
        None — This function writes files to disk (.gv and .png).
    """

    # Create directed graph
    graph = Digraph(format="png")
    graph.attr(rankdir="LR")  # Left → Right orientation for readability

    visited = set()           # States already drawn
    queue = [nfa.start_state]  # BFS queue starting from start state

    while queue:
        state = queue.pop(0)

        if state in visited:
            continue
        
        visited.add(state)

        # --- Draw State Node ---
        # Accepting (final) states get a double-circle shape
        if state.is_accepting:
            graph.node(
                name=str(id(state)),
                label=f"S{state.id}",
                shape="doublecircle"
            )
        else:
            graph.node(
                name=str(id(state)),
                label=f"S{state.id}",
                shape="circle"
            )

        # --- Draw Transitions (Edges) ---
        for symbol, target_states in state.transitions.items():
            for target in target_states:

                # Label ε transitions correctly
                label = symbol if symbol != "" else "ε"

                graph.edge(
                    str(id(state)),
                    str(id(target)),
                    label=label
                )

                # Add unvisited states to BFS queue
                if target not in visited:
                    queue.append(target)

    # Save and render graph
    graph.render(filename=output_filename, cleanup=True)
    print(f"NFA visual saved as: {output_filename}.png")