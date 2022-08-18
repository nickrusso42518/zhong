#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Description: Module for CLI argument functions
"""

import argparse
import sys

# String used to test a system for MacOS
MACOS_PLATFORM = "darwin"


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
