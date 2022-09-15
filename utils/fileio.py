#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Description: Module for file I/O functions.
"""

import csv
import string
import sys


# Rare cases of chinese symbols not in the correct unicode range
C_SYM_EXCEPTIONS = ["〇", "，", "。"]

# Identify valid pinyin characters. Numbers 1-4 map to the chinese tones.
# The : symbol represents a non-written tone transition via special rule.
# The space is used for cleanliness to separate pinyin words.
VALID_PINYIN = string.ascii_lowercase + " :1234"


def load_csv_data(csv_filename):
    """
    Load and validate row data from CSV file using three column format:
    chinese,pinyin,english
    """

    # Try to open the file
    try:
        # If the file exists, include rows that don't begin with # (comment)
        with open(csv_filename, encoding="utf-8") as handle:
            csv_reader = csv.reader(handle)
            rows = [row for row in csv_reader if not row[0].startswith("#")]

    # File does not exist; print Python-generated error and quit with rc=3
    except FileNotFoundError as fnf_error:
        print(f"ERROR: {fnf_error}")
        sys.exit(3)

    # Iterate over list of rows from CSV
    chin_unique, chin_dup = set(), []
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

        # Ensure number of chinese and pinyin elements are the same
        # Ignore this test if pinyin contains "::" for multi-tone characters
        if not "::" in row[1]:
            assert len(row[0]) == row[1].count(" ") + 1, f"{row[0]}: {row[1]}"

        # Capture duplicates; if symbol in set already, it's a duplicate
        if not row[0] in chin_unique:
            chin_unique.add(row[0])
        else:
            chin_dup.append(row[0])

    # Ensure duplicate list has zero length, else we have duplicates
    assert not chin_dup, f"duplicate entries: {','.join(chin_dup)}"

    # All tests passed; return the list of rows
    return rows


def print_report(argv):
    """
    Count Chinese phrases by length and display the results. This helps
    determine how much of a given CSV file has individual characters/words
    versus longer phrases.
    """

    # Loop over CLI arguments
    for arg in argv[1:]:

        # Perform regular data loading and validation process
        rows = load_csv_data(arg)
        counters = {}

        # Loop over rows, creating a new dict key upon first seeing a new
        # length word, then increment that counter afterwards
        for row in rows:
            key = len(row[0])
            counters[key] = (counters[key] + 1) if (key in counters) else 1

        # Print the report for a given file, including the word length
        # and number of words having that length
        print(f"Report for {arg}")
        for key, val in counters.items():
            if val:
                print(f"  - {key}: {val}")
        print()


if __name__ == "__main__":
    print_report(sys.argv)
