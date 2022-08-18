#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Description: Ensure all Chinese characters don't crash the lookup process.
"""

import sys

from utils.dictdb import lookup
from utils.fileio import load_csv_data


def main(argv):
    """
    Execution starts here.
    """

    # Loop over CLI arguments representing input files
    for infile in argv[1:]:
        rows = load_csv_data(infile)

        # For each row, lookup the Chinese characters
        for row in rows:
            lookup(row[0])


if __name__ == "__main__":
    main(sys.argv)
