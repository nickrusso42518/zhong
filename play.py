#!/usr/bin/env python

import csv
import random
import subprocess
import string

from colorama import Fore
from colorama import Style
import sys

# Try to read Chinese characters, but only works on MacOS
SPEAK_TOGGLE = True and sys.platform == "darwin"

# Rate of speech in words per minute. 90 is slowest and 180 is default
SPEAK_RATE = 90

def load_symbols(csv_filename):
    with open(csv_filename, encoding="utf=8") as handle:
        csv_reader = csv.reader(handle)
        symbols = [row for row in csv_reader if not row[0].startswith("#")]

    # Identify valid pinyin characters (a-z, 1-4, -, >, and space)
    valid_pinyin = string.ascii_lowercase + "->1234 "

    for symbol in symbols:
        # Ensure exactly 3 columns exist
        assert len(symbol) == 3

        # Ensure Chinese symbols are within proper unicode range
        for chinese_char in symbol[0]:
            assert 0x4e00 <= ord(chinese_char) <= 0x9fff

        # Ensure pinyin only contains valid characters
        assert all(pinyin_char in valid_pinyin for pinyin_char in symbol[1])

    return symbols

def main(csv_filename):

    # Initialize counters and load symbols
    symbols = load_symbols(csv_filename)
    count = 1
    total = len(symbols)

    print("HOW TO PLAY:")
    print("  Provide the pinyin and english for the chinese phrase shown.")
    print("  Unicode values for chinese characters are shown in parenthesis.")
    print("  Mac users can enable narration of the chinese symbols.")
    print("  Press ENTER by itself (no input) to reprint/restate the phrase.")
    print("  Enter a comma (,) character to skip/forfeit a question.")
    print("  Enter a period (.) character to quit; it's invalid input.")

    # Keep looping while more symbols exist
    while symbols:

        # Select a random symbol by index
        index = random.randint(0, len(symbols) - 1)
        sym = symbols[index]

        # Extract chinese, pinyin, and english from the symbol entry
        chinese = sym[0].lower().strip()
        pinyin = sym[1].lower().strip()
        english = sym[2].lower().strip()

        # Build a string of unicode chars for debugging
        unicode_str = " ".join([hex(ord(c)) for c in chinese])

        # While attempt is blank, keep looping
        attempt = ""
        while not attempt.strip():
            print(f"\n{count}/{total}: {chinese}   ({unicode_str})")

            # If SPEAK_TOGGLE is true, use the "say" command. Mac only!
            if SPEAK_TOGGLE:
                say_cmd = f"say --voice=Ting-Ting --rate={SPEAK_RATE} {chinese}"
                subprocess.run(say_cmd.split(" "))

            # Prompt for input
            attempt = input(f"Type the pinyin,english: ")

        # Unpack inputs and test for proper pinyin and english
        in1, in2 = attempt.split(",")
        p_color = Fore.GREEN if in1.lower().strip() == pinyin else Fore.RED

        in2 = in2.lower().strip()
        e_color = Fore.GREEN if len(in2) > 0 and in2 in english else Fore.RED

        # Print results using proper colors
        print(f"pinyin: {p_color}{pinyin}{Style.RESET_ALL}", end="")
        print(f"    english: {e_color}{english}{Style.RESET_ALL}")

        # Delete symbol and increment counter
        del symbols[index]
        count += 1

if __name__ == "__main__":
    main("symbols.csv")
