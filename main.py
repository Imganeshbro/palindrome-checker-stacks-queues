"""
Main Entry Point for the Palindrome Checker Project.
Supports GUI Mode, Interactive Terminal CLI Mode, Unit Testing, and Asset Generation.
"""

import sys
import os
import argparse

# Ensure standard output uses UTF-8 or ASCII safe encoding on Windows terminals
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from palindrome_core import PalindromeChecker


def print_banner():
    banner = r"""
========================================================================
    PALINDROME CHECKER (STACKS & QUEUES DATA STRUCTURES)
    Demonstrating LIFO (Stack) vs FIFO (Queue) Algorithmic Symmetry
========================================================================
"""
    print(banner)


def run_cli(text: str, ignore_case: bool = True, ignore_punct: bool = True):
    print_banner()
    checker = PalindromeChecker(ignore_case=ignore_case, ignore_spaces_and_punct=ignore_punct)
    print(f"[*] Input Text:               '{text}'")
    print(f"[*] Ignore Case:              {ignore_case}")
    print(f"[*] Ignore Spaces/Punct:      {ignore_punct}")
    print("-" * 72)

    result = checker.check(text)

    print(f"[*] Cleaned Text:             '{result.cleaned_text}' (len={len(result.cleaned_text)})")
    print(f"[*] Verdict:                  {'PALINDROME [YES]' if result.is_palindrome else 'NOT A PALINDROME [NO]'}")
    print(f"[*] Total Step Count:         {result.total_step_count}")
    print(f"[*] Comparisons Made:         {result.comparisons_made}")
    print(f"[*] Theoretical Complexity:   Time {result.time_complexity} | Space {result.space_complexity}")
    print("-" * 72)
    print(f"{'Step #':<8} {'Phase':<12} {'Stack Pop':<12} {'Queue Deq':<12} {'Match?':<10} {'Details'}")
    print("-" * 72)

    for s in result.steps:
        comp_str = "MATCH" if s.is_match else ("MISMATCH" if s.is_match is False else "-")
        s_char = s.stack_char or "-"
        q_char = s.queue_char or "-"
        print(f"{s.step_number:<8} {s.phase:<12} {s_char:<12} {q_char:<12} {comp_str:<10} {s.description}")

    print("-" * 72)
    if result.is_palindrome:
        print("[PASS] SUCCESS: The input string is a valid palindrome.")
    else:
        print(f"[FAIL] MISMATCH: {result.mismatch_details}")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(
        description="Palindrome Checker using Stacks (LIFO) and Queues (FIFO) with Interactive GUI & CLI."
    )
    parser.add_argument("--cli", action="store_true", help="Run in command line interface mode instead of GUI.")
    parser.add_argument("--text", "-t", type=str, default="racecar", help="Text to test in CLI mode.")
    parser.add_argument("--test", action="store_true", help="Run automated unit test suite.")
    parser.add_argument("--assets", action="store_true", help="Regenerate report image assets.")
    parser.add_argument("--strict", action="store_true", help="Strict mode (do not ignore case or punctuation).")

    args = parser.parse_args()

    if args.test:
        import unittest
        import test_palindrome
        suite = unittest.TestLoader().loadTestsFromModule(test_palindrome)
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
        return

    if args.assets:
        import generate_assets
        print("Regenerating report assets...")
        return

    if args.cli:
        run_cli(args.text, ignore_case=not args.strict, ignore_punct=not args.strict)
        return

    # Default: Run Graphical User Interface (GUI)
    try:
        from palindrome_gui import run_gui
        print("Starting Palindrome Checker GUI...")
        run_gui()
    except Exception as e:
        print(f"Notice: GUI could not be opened in current terminal session ({e}).")
        print("Falling back to interactive CLI demonstration:")
        run_cli("A man, a plan, a canal: Panama!")


if __name__ == "__main__":
    main()
