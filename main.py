# taku
from typing import Optional
import argparse
import sys

# Import the project modules. If they are missing, show a friendly error.
try:
    from src.preprocessor import insert_concatenation_operator
    from src.parser import shunting_yard
    from src.converter import postfix_to_nfa
    from src.display import display_nfa
except Exception as e:
    msg = (
        "Failed to import project modules from src/. Make sure your project has:\n"
        "  src/preprocessor.py (insert_concatenation_operator)\n"
        "  src/parser.py (shunting_yard)\n"
        "  src/converter.py (postfix_to_nfa)\n"
        "  src/display.py (display_nfa)\n\n"
        "Original error: {}"
    ).format(e)
    raise ImportError(msg)


def process_regex(regex: str, output_filename: str = "nfa_graph", show_steps: bool = False) -> None:
    """
    Run the full pipeline on a single regex and save the graph.

    Parameters
    ----------
    regex : str
        The raw regular expression provided by the user.
    output_filename : str
        Name for the output graph files (without extension).
    show_steps : bool
        If True, print the preprocessed and postfix representations.
    """
    if not regex:
        raise ValueError("Empty regular expression provided.")

    # 1. Preprocess: insert explicit concatenation operators
    try:
        preprocessed = insert_concatenation_operator(regex)
    except Exception as e:
        print(f"[error] Preprocessing failed: {e}", file=sys.stderr)
        raise

    # 2. Convert to postfix using shunting-yard
    try:
        postfix = shunting_yard(preprocessed)
    except Exception as e:
        print(f"[error] Parsing to postfix failed: {e}", file=sys.stderr)
        raise

    # Print intermediate representations if requested
    if show_steps:
        print(f"Raw regex      : {regex}")
        print(f"Preprocessed   : {preprocessed}")
        print(f"Postfix        : {postfix}")

    # 3. Build NFA from postfix
    try:
        nfa = postfix_to_nfa(postfix)
    except Exception as e:
        print(f"[error] Converting postfix to NFA failed: {e}", file=sys.stderr)
        raise

    # 4. Display/render the NFA using graphviz
    try:
        display_nfa(nfa, output_filename)
    except Exception as e:
        print(
            "[warning] display_nfa raised an exception. "
            "Make sure graphviz (system tool) is installed and python graphviz is available.\n"
            f"Original error: {e}",
            file=sys.stderr,
        )
        raise

    print(f"[ok] NFA rendered and saved as files with base name: '{output_filename}'")


def interactive_prompt() -> None:
    """Run a small interactive loop requesting regex from the user."""
    print("Regular Expression -> NFA Converter (interactive mode)")
    print("Type 'quit' or empty input to exit.")
    while True:
        try:
            regex = input("\nEnter a regular expression > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            return

        if not regex or regex.lower() in ("quit", "exit"):
            print("Goodbye.")
            return

        output = input("Output filename (default 'nfa_graph') > ").strip()
        if not output:
            output = "nfa_graph"

        show = input("Show preprocessing and postfix? [y/N] > ").strip().lower()
        show_steps = show in ("y", "yes")

        try:
            process_regex(regex, output, show_steps)
        except Exception as e:
            print(f"[error] Failed to process regex: {e}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a regular expression into an NFA and render it as a graph."
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
        help="Base name for output graph files (no extension). Default: 'nfa_graph'.",
    )
    parser.add_argument(
        "-s",
        "--show-steps",
        action="store_true",
        help="Print preprocessed and postfix representations.",
    )
    return parser


def main(argv: Optional[list] = None) -> None:
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
