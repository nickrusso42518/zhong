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
# The : symbol represents a non-written tone transition via special rule.
# The space is used for cleanliness to separate pinyin words.
VALID_PINYIN = string.ascii_lowercase + " :1234"

# String used to test a system for MacOS
MACOS_PLATFORM = "darwin"


def main(args):
    """
    Main game code.
    """

    # Load symbols and initialize counters to track progress
    rows = load_symbols(args.infile)
    i = 1
    total = len(rows)

    # Print gameplay instructions before asking translation questions
    print("HOW TO PLAY:")
    print("  Provide the english meaning for the chinese/pinyin phrase shown.")
    print("  Press ENTER by itself (no input) to reprint/restate the phrase.")
    print("  Enter a comma (,) character to skip/forfeit a question.")
    print("  Enter a period (.) character to quit gracefully.")

    # Keep looping while more rows exist
    while rows:

        # Select a random symbol by index
        index = random.randint(0, len(rows) - 1)
        row = rows[index]

        # Extract chinese, pinyin, and english from the symbol entry
        chinese, pinyin, english = [r.lower().strip() for r in row]

        # Attempt to collect input from user interactively
        attempt = run_attempt(args, chinese, pinyin, i, total)

        # Test for proper english input, colorize it, and print result
        e_color = Fore.GREEN if attempt in english else Fore.RED
        print(f"correct english: {e_color}{english}{Style.RESET_ALL}")

        # Delete symbol from list (won't see twice) and increment counter
        del rows[index]
        i += 1


def load_symbols(csv_filename):
    """
    Load and validate Chinese symbols from file using three column format:
    chinese,pinyin,english
    """

    # Try to open the file
    try:
        # If the file exists, include rows that don't begin with # (comment)
        with open(csv_filename, encoding="utf=8") as handle:
            csv_reader = csv.reader(handle)
            rows = [row for row in csv_reader if not row[0].startswith("#")]

    # File does not exist; print Python-generated error and quit with rc=3
    except FileNotFoundError as fnf_error:
        print(f"ERROR: {fnf_error}")
        sys.exit(3)

    # Iterate over list of symbols (rows from CSV)
    seen_chin = set()
    dup_chin = []
    for row in rows:

        # Ensure exactly 3 columns exist in each row
        assert len(row) == 3, f"len({row}) = {len(row)}"

        # Ensure chinese symbols are within proper unicode range or
        # are explicitly permitted as exceptions
        for c_sym in row[0]:
            c_sym_ord = ord(c_sym)
            assert (
                0x4E00 <= c_sym_ord <= 0x9FFF
            ) or c_sym in C_SYM_EXCEPTIONS, f"ord({c_sym}) = {c_sym_ord}"

        # Ensure pinyin only contains valid characters
        assert all(
            pinyin_char in VALID_PINYIN for pinyin_char in row[1]
        ), f"{row[1]} not in {VALID_PINYIN}"

        # Capture duplicates; if symbol in set already, it's a duplicate
        if row[0] in seen_chin:
            dup_chin.append(row[0])
        else:
            seen_chin.add(row[0])

    # Ensure chinese list and set are same length, else we have duplicates
    assert not dup_chin, f"dup_chin: {','.join(dup_chin)}"

    # All tests passed; return the list of rows
    return rows


def run_attempt(args, chinese, pinyin, i, total):
    """
    Produce a single test question, collect input, and return it.
    """

    # If -c/-p is set, mask the chinese/pinyin. Highlight with mouse to reveal
    c_color = Fore.BLACK + Back.BLACK if args.nochin else ""
    p_color = Fore.BLACK + Back.BLACK if args.nopin else ""

    # While attempt is blank, keep looping
    attempt = ""
    while not attempt:

        # Print chinese and pinyin together using the proper color
        print(f"\n{i}/{total}:    {c_color}{chinese}{Style.RESET_ALL}", end="")
        print(f"    ({p_color}{pinyin}{Style.RESET_ALL})")

        # Run the "say" command if -s is not set (default)
        # Example: say --voice=Ting-Ting --rate=150 电话号码
        if not args.nosound:
            say_cmd = f"say --voice=Ting-Ting --rate={args.rate} {chinese}"
            subprocess.run(say_cmd.split(" "), check=True, shell=False)

        # Prompt for input and string extra whitespace
        attempt = input("english meaning: ").lower().strip()

        # If user entered a period (.) then quit gracefully (rc=0)
        if attempt == ".":
            print("\n\n")
            sys.exit(0)

    # Return the user input
    return attempt


def process_args():
    """
    Process command line arguments according to README.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--nochin",
        help="disable (mask) presentation of chinese symbols",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--nopin",
        help="disable (mask) presentation of pinyin symbols",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--nosound",
        help="disable sound; no audio narration of phrases",
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
        default="inputs/default.csv",
    )
    args = parser.parse_args()

    # If -c and -p are set, system must be MacOS and -s must be unset
    if args.nochin and args.nopin:

        # Disabling all visual and audible cues is meaningless, fail with rc=2
        if args.nosound:
            print("ERROR: -c/-p/-s can never be enabled together")
            sys.exit(2)

        # Only MacOS has sounds; non-MacOS must display chinese, pinyin, or both
        elif sys.platform != MACOS_PLATFORM:
            print("ERROR: -c/-p cannot be enabled together on non-MacOS")
            sys.exit(2)

    # Sounds are disabled if system is not MacOS or -s set
    args.nosound = (sys.platform != MACOS_PLATFORM) or args.nosound

    # CLI arguments valid; return the object containing them
    return args


if __name__ == "__main__":
    main(process_args())
