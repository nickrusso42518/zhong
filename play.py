#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Description: Chinese language trainer. See README.md for details.
"""

import random
import subprocess

from colorama import Fore, Back, Style

from utils.cliargs import process_args
from utils.dictdb import lookup
from utils.fileio import load_csv_data


def main(args):
    """
    Main game code.
    """

    # Load symbols and initialize counters to track progress
    rows = load_csv_data(args.infile)
    fail_list = []
    succ_c = 0
    i = 1
    total = len(rows)

    # Print gameplay instructions before asking translation questions
    print("HOW TO PLAY:")
    print("  Provide the english meaning for the chinese/pinyin phrase shown.")
    print("  Press ENTER by itself (no input) to reprint/restate the phrase.")
    print("  Enter a comma (,) character to skip/forfeit a question.")
    print("  Enter a question mark (?) character to consult the dictionary.")
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

        # If attempt is None, user wants to quit. Break out of the loop
        if attempt is None:
            break

        # Test for proper english input, colorize it, and track successes
        if attempt in english:
            e_color = Fore.GREEN
            succ_c += 1
        else:
            e_color = Fore.RED
            fail_list.append(",".join(row))

        # Print colorized output, then current success count and percent
        print(f"correct english: {e_color}{english}{Style.RESET_ALL}")
        print(f"[success# = {succ_c}   success% = {int(succ_c / i * 100)}]")

        # Delete row from list (won't see twice) and increment counter
        del rows[index]
        i += 1

    # If attempt is None, user wants to quit. Print failed items
    # and exit with rc=0 to signal success (no error)
    fail_list_str = "\n".join(fail_list)
    print(f"\nINCORRECTLY ANSWERED:\n{fail_list_str}\n")


def run_attempt(args, chinese, pinyin, i, total):
    """
    Produce a single test question, collect input, and return it.
    """

    # If -c/-p is set, mask the chinese/pinyin. Highlight with mouse to reveal
    c_color = Fore.BLACK + Back.BLACK if args.nochin else ""
    p_color = Fore.BLACK + Back.BLACK if args.nopin else ""

    # While attempt is blank, keep looping
    attempt, say_sp = None, None
    while not attempt:

        # Print chinese and pinyin together using the proper color
        print(f"\n{i}/{total}:    {c_color}{chinese}{Style.RESET_ALL}", end="")
        print(f"    ({p_color}{pinyin}{Style.RESET_ALL})")

        # Spawn new process to run the "say" command if -s is not set (default)
        # Example: say --voice=Ting-Ting --rate=150 电话号码
        if not args.nosound:
            say_cmd = f"say --voice=Ting-Ting --rate={args.rate} {chinese}"
            say_sp = subprocess.Popen(say_cmd.split(" "))

        # Prompt for input and string extra whitespace
        attempt = input("english meaning: ").lower().strip()

        # If "say" command ran, ensure the process terminates
        if say_sp:
            say_sp.communicate()

        # If user entered a question mark (?) then lookup symbols in dictionary
        if attempt == "?":
            lookup(chinese)

        # If user entered a period (.) then return None
        elif attempt == ".":
            return None

    # Return the user input
    return attempt


if __name__ == "__main__":
    main(process_args())
