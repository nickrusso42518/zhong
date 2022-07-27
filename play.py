#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Description: Chinese language trainer. See README.md for details.
"""

import argparse
import csv
import random
import subprocess
import string
import sys

from colorama import Fore, Back, Style

# Rare cases of chinese symbols not in the correct unicode range
C_SYM_EXCEPTIONS = ["〇"]

# Identify valid pinyin characters. Numbers 1-4 map to the chinese tones.
# The -> symbol represents a non-written tone transition or special rule.
# The space is used for cleanliness to separate pinyin words.
VALID_PINYIN = string.ascii_lowercase + "->1234 "


def main(args):
    """
    Main game code.
    """

    # Initialize counters and load symbols
    symbols = load_symbols(args.infile)
    count = 1
    total = len(symbols)

    print("HOW TO PLAY:")
    print("  Provide the pinyin and english for the chinese phrase shown.")
    print("  Unicode values for chinese characters are shown in parenthesis.")
    print("  MacOS users can enable narration of the chinese symbols.")
    print("  Press ENTER by itself (no input) to reprint/restate the phrase.")
    print("  Enter a comma (,) character to skip/forfeit a question.")
    print("  Enter a period (.) character to quit gracefully.")

    # Keep looping while more symbols exist
    while symbols:

        # Select a random symbol by index
        index = random.randint(0, len(symbols) - 1)
        sym = symbols[index]

        # Extract chinese, pinyin, and english from the symbol entry
        chinese, pinyin, english = [s.lower().strip() for s in sym]

        # Attempt to collect input and unpack returned 2-tuple
        in1, in2 = run_attempt(args, chinese, count, total)

        # Test for proper pinyin and english, then colorize it
        p_color = Fore.GREEN if in1.lower().strip() == pinyin else Fore.RED
        in2 = in2.lower().strip()
        e_color = Fore.GREEN if len(in2) > 0 and in2 in english else Fore.RED

        # Print results using proper colors
        print(f"pinyin: {p_color}{pinyin}{Style.RESET_ALL}", end="")
        print(f"    english: {e_color}{english}{Style.RESET_ALL}")

        # Delete symbol from list (won't see twice) and increment counter
        del symbols[index]
        count += 1


def load_symbols(csv_filename):
    """
    Load and validate Chinese symbols from file using three column format:
    chinese,pinyin,english
    """

    with open(csv_filename, encoding="utf=8") as handle:
        csv_reader = csv.reader(handle)
        symbols = [row for row in csv_reader if not row[0].startswith("#")]

    # Iterate over list of symbols (rows from CSV)
    c_list = []
    c_set = set()
    for symbol in symbols:

        # Ensure exactly 3 columns exist
        assert len(symbol) == 3

        # Ensure chinese symbols are within proper unicode range or
        # are explicitly permitted as exceptions
        for c_sym in symbol[0]:
            c_sym_ord = ord(c_sym)
            assert (0x4E00 <= c_sym_ord <= 0x9FFF) or c_sym in C_SYM_EXCEPTIONS

        # Ensure pinyin only contains valid characters
        assert all(pinyin_char in VALID_PINYIN for pinyin_char in symbol[1])

        # Valid chinese/pinyin; add entire chinese phrase to a list and a set
        c_list.append(symbol[0])
        c_set.add(symbol[0])

    # Ensure chinese list and set are same length, else we have duplicates
    assert len(c_list) == len(c_set)

    # All tests passed; return the symbols list
    return symbols


def run_attempt(args, chinese, count, total):
    """
    Produce a single test question, collect input, and return it.
    """

    # If mask mode is enabled, mask chinese symbols. Can highlight to reveal
    c_color = Fore.BLACK + Back.BLACK if args.mask else ""

    # While attempt is blank, keep looping
    attempt = ""
    while not attempt:
        print(f"\n{count}/{total}:   {c_color}{chinese}{Style.RESET_ALL}")

        # Run the "say" command if quiet mode is disabled
        if not args.quiet:
            say_cmd = f"say --voice=Ting-Ting --rate={args.rate} {chinese}"
            subprocess.run(say_cmd.split(" "), check=True)

        # Prompt for input and string extra whitespace
        attempt = input("Type the pinyin,english: ").strip()

        # If user entered a period (.) then quit gracefully (rc=0)
        if attempt == ".":
            sys.exit(0)

        # Try to split the input on comma. If no comma exists, catch
        # ValueError and set attempt to empty string, causing re-loop
        try:
            in1, in2 = attempt.split(",")
        except ValueError:
            attempt = ""

    # Return 2-tuple (parenthesis optional) of pinyin,english inputs
    return in1, in2


def process_args():
    """
    Process command line arguments according to README.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--mask",
        help="disable easy reading of chinese symbols (MacOS only)",
        action="store_true",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="disable audio narration of chinese symbols (MacOS only)",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--rate",
        help="adjust rate of speech in words per minute (90 to 300)",
        type=int,
        default=180,
    )
    parser.add_argument(
        "-i",
        "--infile",
        help="input file in CSV format (chinese,pinyin,english)",
        type=str,
        default="inputs/all.csv",
    )
    args = parser.parse_args()

    # Using mask and quiet together is meaningless, fail with rc=2
    if args.mask and args.quiet:
        print("ERROR: --mask and --quiet cannot be enabled together")
        sys.exit(2)

    # Quiet mode is enabled if system is not MacOS or -q set
    args.quiet = (sys.platform != "darwin") or args.quiet

    # Blind mode is enabled if system is MacOS and -m set
    args.mask = (sys.platform == "darwin") and args.mask

    return args


if __name__ == "__main__":
    main(process_args())
