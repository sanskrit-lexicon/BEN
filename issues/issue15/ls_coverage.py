#!/usr/bin/env python3
"""Compare <ls> tags from ben.txt against tooltip expansions.

Shows how many unique <ls> values have an expansion and how many do not.

Usage: python ls_coverage.py
"""

import os
import re
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LS_INPUT = os.path.join(SCRIPT_DIR, "temp_ben_0.txt")
LS_EXPANSIONS = os.path.join(SCRIPT_DIR, "ls_input.txt")
LS_PATTERN = re.compile(r"<ls>([^<]+)</ls>")

def main():
    counter = Counter()
    with open(LS_INPUT, encoding="utf-8") as fh:
        for line in fh:
            counter.update(LS_PATTERN.findall(line))

    ben_ls_values = set(counter.keys())

    expansions = {}
    with open(LS_EXPANSIONS, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or "\t" not in line:
                continue
            ls_val = line.split("\t", 1)[0]
            expansions[ls_val] = line

    expansion_ls_values = set(expansions.keys())

    have_expansion = ben_ls_values & expansion_ls_values
    no_expansion = ben_ls_values - expansion_ls_values
    expansions_only = expansion_ls_values - ben_ls_values

    print("=== <ls> tag expansion coverage ===")
    print()
    print(f"Unique <ls> values in ben.txt:     {len(ben_ls_values)}")
    print(f"Entries in ls_input.txt:             {len(expansion_ls_values)}")
    print()
    print(f"Have expansion:     {len(have_expansion):>3}  ({len(have_expansion)/len(ben_ls_values)*100:>5.1f}%)")
    print(f"No expansion:       {len(no_expansion):>3}  ({len(no_expansion)/len(ben_ls_values)*100:>5.1f}%)")
    if expansions_only:
        print(f"In expansions file but not in ben.txt: {len(expansions_only)}")
    print()

    if no_expansion:
        print(f"{'Value':<30} {'Count':>7}")
        print("-" * 38)
        for val, cnt in sorted(((v, counter[v]) for v in no_expansion), key=lambda x: (-x[1], x[0])):
            print(f"{val:<30} {cnt:>7}")

if __name__ == "__main__":
    main()
