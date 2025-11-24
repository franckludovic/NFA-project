# tests/test_display_nfa.py

import os
import pytest
from src.display import display_nfa
from src.nfa_structure import State, NFA

def build_sample_nfa():
    """
    Creates a tiny NFA: a --> b
    Used only for testing display output.
    """
    s1 = State()
    s2 = State(is_accepting=True)
    s1.add_transition("a", s2)
    return NFA(start_state=s1, accept_state=s2)


def test_display_creates_image_file(tmp_path):
    """
    This test ensures that display_nfa successfully generates
    a Graphviz output file (PNG or other supported formats).

    Why this matters:
    - Confirms Graphviz is installed and callable.
    - Ensures display_nfa traverses all states without errors.
    - Detects structural issues in NFA objects.
    - Guarantees file creation works on the current machine.
    """

    # Build simple NFA
    nfa = build_sample_nfa()

    # Output path inside pytest temporary directory
    output_file = tmp_path / "test_output"

    # Call the display function
    display_nfa(nfa, output_filename=str(output_file))

    # Graphviz will append `.png`, `.svg`, etc.
    produced_files = list(tmp_path.iterdir())

    # Assertions: at least one file created
    assert len(produced_files) >= 1, "display_nfa did not produce any output files."

    # Validate file extension
    allowed_ext = {".png", ".svg", ".pdf", ".gv"}
    assert any(f.suffix in allowed_ext for f in produced_files), \
        "display_nfa produced files, but not valid Graphviz output formats."


def test_display_runs_without_crashing(tmp_path):
    """
    Ensures display_nfa runs with no exceptions.
    Even if the file isn't created, crashing indicates deeper issues.
    """
    nfa = build_sample_nfa()
    output_file = tmp_path / "basic_run"

    try:
        display_nfa(nfa, output_filename=str(output_file))
    except Exception as e:
        pytest.fail(f"display_nfa raised an exception: {e}")
