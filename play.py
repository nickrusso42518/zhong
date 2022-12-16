#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Description: Chinese language trainer. See README.md for details.
"""

import random
import subprocess
import time

from colorama import Fore, Back, Style

from utils.cliargs import process_args
from utils.dictdb import lookup
from utils.fileio import load_csv_data

# Seconds to sleep after each item when auto is enabled
AUTO_SLEEP = 5


def main(args):
    """
    Main game code.
    """

    # Load symbols and initialize empty list to track failures
    rows = load_csv_data(args.infile)
    fail_list = []

    # Print gameplay instructions before asking translation questions
    print("HOW TO PLAY:")
    print("  Provide the english meaning for the chinese/pinyin phrase shown.")
    print("  Press ENTER by itself (no input) to reprint/restate the phrase.")
    print("  Enter a comma (,) character to skip/forfeit a question.")
    print("  Enter a question mark (?) character to consult the dictionary.")
    print("  Enter a period (.) character to quit gracefully.")

    # Randomize (shuffle) the list of row entries, then iterate over them
    random.shuffle(rows)
    for i, row in enumerate(rows, start=1):

        # Extract chinese, pinyin, and english from the row entry
        chinese, pinyin, english = [r.lower().strip() for r in row]

        # Attempt to collect input from user interactively
        attempt = run_attempt(args, chinese, pinyin, i, len(rows))

        # If attempt is None, user wants to quit. Break out of the loop
        if attempt is None:
            break

        # Test for proper english input, colorize it, and track failures
        if attempt in english:
            e_color = Fore.GREEN
        else:
            e_color = Fore.RED
            fail_list.append(",".join(row))

        # Print colorized solutions, then current success count and percent
        succ_c = i - len(fail_list)
        succ_p = round(succ_c / i * 100, 2)
        print(f"correct english: {e_color}{english}{Style.RESET_ALL}")
        print(f"[success# = {succ_c}, success% = {succ_p}]")

    # If attempt is None, user wants to quit. Print failed items
    # and exit with rc=0 to signal success (occurs by default)
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
        print(f"\n{i}/{total}:  {c_color}{chinese}{Style.RESET_ALL}", end="")
        print(f"  ({p_color}{pinyin}{Style.RESET_ALL})")

        # Spawn new process to run the "say" command if -s is not set (default)
        # Example: say --voice=tingting --rate=150 电话号码
        if not args.nosound:
            say_cmd = f"say --voice=tingting --rate={args.rate} {chinese}"
            say_sp = subprocess.Popen(say_cmd.split(" "))

        # Prompt for input and strip extra whitespace
        if not args.auto:
            attempt = input("english meaning: ").lower().strip()

        # If "say" command ran, ensure the process terminates
        if say_sp:
            say_sp.communicate()

        # If in auto (hands-free) mode, wait a period of time, and
        # hardcode a comma response
        if args.auto:
            time.sleep(AUTO_SLEEP)
            attempt = ","

        # If user entered a question mark (?) then lookup symbols in dictionary
        # Overwrite attempt to a comma, which is guaranteed not to be correct
        if attempt == "?":
            lookup(chinese)
            attempt = ","

        # If user entered a period (.) then return None (breaks loop)
        elif attempt == ".":
            return None

    # Return the user input
    return attempt


if __name__ == "__main__":
    main(process_args())
