from typing import Optional
import argparse
import sys

# Import project modules (original)
try:
    from src.prepocessor import insert_concatenation_operator
    from src.parser import regex_shunting_yard
    from src.converter import postfix_to_nfa
    from src.display import display_nfa
    from src.nfa_dfa import nfa_to_dfa 
except Exception as e:
    msg = (
        "Failed to import project modules from src/. Make sure your project has:\n"
        "  src/preprocessor.py (insert_concatenation_operator)\n"
        "  src/parser.py (shunting_yard)\n"
        "  src/converter.py (postfix_to_nfa)\n"
        "  src/display.py (display_nfa)\n\n"
        f"Original error: {e}"
    )
    raise ImportError(msg)

# NEW IMPORT for NFA → DFA
try:
    from src.nfa_to_dfa import nfa_to_dfa
except Exception:
    print("[warning] nfa_to_dfa not found. DFA conversion will be unavailable.")


# GLOBAL: stores last built NFA
LAST_NFA = None


def process_regex(regex: str, output_filename: str = "nfa_graph", show_steps: bool = False):
    """
    (unchanged) – Now additionally stores the resulting NFA for DFA conversion later.
    """
    global LAST_NFA

    if not regex:
        raise ValueError("Empty regular expression provided.")

    # 1. Preprocess
    preprocessed = insert_concatenation_operator(regex)

    # 2. Convert to postfix
    postfix = regex_shunting_yard(preprocessed)

    if show_steps:
        print(f"Raw regex      : {regex}")
        print(f"Preprocessed   : {preprocessed}")
        print(f"Postfix        : {postfix}")

    # 3. Build NFA
    nfa = postfix_to_nfa(postfix)

    # Save globally for DFA conversion
    LAST_NFA = nfa

    # 4. Display NFA
    display_nfa(nfa, output_filename)

    print(f"[ok] NFA rendered and saved as '{output_filename}'")


def convert_last_nfa_to_dfa():
    """
    NEW – Converts stored NFA to DFA.
    """
    global LAST_NFA

    if LAST_NFA is None:
        print("[error] No NFA available. Build one first.")
        return

    print("[info] Converting NFA to DFA...")

    try:
        start_dfa, all_dfa_states = nfa_to_dfa(LAST_NFA)
    except Exception as e:
        print(f"[error] DFA conversion failed: {e}")
        return

    print("\n--- DFA States ---")
    for st in all_dfa_states.values():
        ids = sorted([s.id for s in st.nfa_states])
        print(f"State {ids} (accept={st.is_accept})")
        for sym, nxt in st.transitions.items():
            nxt_ids = sorted([s.id for s in nxt.nfa_states])
            print(f"  {sym} → {nxt_ids}")

    print("\n[ok] DFA successfully built (no image display yet).")


def interactive_prompt():
    """
    EXTENDED – includes new menu options for DFA.
    """
    print("Regular Expression -> NFA/DFA Tool (interactive mode)")
    print("Type 'quit' or empty input to exit.")

    while True:
        print("\nOPTIONS:")
        print("  1. Build NFA from regex")
        print("  2. Convert last NFA to DFA")
        print("  3. Enter new regex (restart)")
        print("  4. Exit")

        choice = input("\nSelect option > ").strip()

        if choice in ("4", "quit", "exit", ""):
            print("Goodbye.")
            return

        elif choice == "1" or choice == "3":
            regex = input("Enter a regular expression > ").strip()
            if not regex:
                continue

            output = input("Output filename (default 'nfa_graph') > ").strip() or "nfa_graph"

            show = input("Show preprocessing and postfix? [y/N] > ").lower()
            show_steps = show in ("y", "yes")

            try:
                process_regex(regex, output, show_steps)
            except Exception as e:
                print(f"[error] Failed: {e}")

        elif choice == "2":
            convert_last_nfa_to_dfa()

        else:
            print("[error] Invalid option")


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Convert a regular expression into an NFA and optionally a DFA."
    )
    parser.add_argument(
        "regex",
        type=str,
        nargs="?",
        default=None,
        help="Regular expression to convert. If omitted, runs in interactive mode.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="nfa_graph",
        help="Base name for output graph files.",
    )
    parser.add_argument(
        "-s",
        "--show-steps",
        action="store_true",
        help="Print preprocessing and postfix.",
    )
    return parser


def main(argv: Optional[list] = None):
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if args.regex is None:
        interactive_prompt()
    else:
        try:
            process_regex(args.regex, args.output, args.show_steps)
        except Exception as e:
            print(f"[error] {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
