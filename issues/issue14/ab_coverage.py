#!/usr/bin/env python3
"""Compare <ab> tags from ben.txt against benab expansions.

Shows how many unique <ab> values have an expansion and how many do not.

Usage: python ab_coverage.py
"""

import os
import re
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AB_INPUT = os.path.join(SCRIPT_DIR, "temp_ben_0.txt")
AB_EXPANSIONS = os.path.join(SCRIPT_DIR, "benab_input.txt")
AB_PATTERN = re.compile(r"<ab>([^<]+)</ab>")

def main():
    # Extract all unique <ab> values from ben.txt
    counter = Counter()
    with open(AB_INPUT, encoding="utf-8") as fh:
        for line in fh:
            counter.update(AB_PATTERN.findall(line))

    ben_ab_values = set(counter.keys())

    # Read expansions from benab_input.txt
    expansions = {}
    with open(AB_EXPANSIONS, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or "\t" not in line:
                continue
            ab_val = line.split("\t", 1)[0]
            expansions[ab_val] = line

    expansion_ab_values = set(expansions.keys())

    # Compare
    have_expansion = ben_ab_values & expansion_ab_values
    no_expansion = ben_ab_values - expansion_ab_values

    # Extra: in expansions but not in ben.txt
    expansions_only = expansion_ab_values - ben_ab_values

    print("=== <ab> tag expansion coverage ===")
    print()
    print(f"Unique <ab> values in ben.txt:     {len(ben_ab_values)}")
    print(f"Entries in benab_input.txt:         {len(expansion_ab_values)}")
    print()
    print(f"Have expansion:     {len(have_expansion):>3}  ({len(have_expansion)/len(ben_ab_values)*100:>5.1f}%)")
    print(f"No expansion:       {len(no_expansion):>3}  ({len(no_expansion)/len(ben_ab_values)*100:>5.1f}%)")
    if expansions_only:
        print(f"In expansions file but not in ben.txt: {len(expansions_only)}")
    print()

    # List tags without expansion, in descending order of occurrence
    if no_expansion:
        print(f"{'Value':<24} {'Count':>7}")
        print("-" * 31)
        for val, cnt in sorted(((v, counter[v]) for v in no_expansion), key=lambda x: (-x[1], x[0])):
            print(f"{val:<24} {cnt:>7}")

if __name__ == "__main__":
    main()
