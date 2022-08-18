#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Description: Module for dictionary lookup functions.
"""

from chinese import ChineseAnalyzer, errors

ANALYZER = ChineseAnalyzer()
MAX_DEFS = 4


def lookup(chinese):
    """
    Consult the CC-CEDICT database (dictionary) for a Chinese phrase.
    Prints the matching results, including pinyin and English definitions.
    """

    # Perform the dictionary lookup
    result = ANALYZER.parse(chinese)

    # Loop over returned tokens, which are symbols or small phrases
    for token in result.tokens():
        try:

            # Rely on __getitem__ defined in the result object
            for sym in result[token]:

                # Print the matched symbol and pinyin (latter may not exist)
                pinyin = " ".join(sym.pinyin) if sym.pinyin else "N/A"
                print(f"\n{sym.match}   ({pinyin})")

                # Print the first MAX_DEFS definitions, if any exist
                definitions = sym.definitions if sym.definitions else []
                for i, definition in enumerate(definitions[:MAX_DEFS]):

                    # Ignore contextual CL definitions
                    if not definition.startswith("CL"):
                        print(f"  {i+1}. {definition}")

        except errors.InvalidKeyError:
            # This error should be impossible, but handle it anyway
            print(f"\nSanity check failed; valid token not found: {token}")

        finally:
            # Print a clean-up newline no matter what
            print("\n")


def main():
    """
    Consult the CC-CEDICT database (dictionary) for a Chinese phrase.
    Works interactively for a quick, non-gameplay lookup.
    """
    while True:
        chinese = input("enter symbols (use . to quit): ").strip()
        if chinese == ".":
            break
        result = ANALYZER.parse(chinese)
        result.pprint()


if __name__ == "__main__":
    main()
