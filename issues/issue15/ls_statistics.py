#!/usr/bin/env python3
"""Analyze <ls>...</ls> tag occurrences in ben.txt.

Usage: python ls_statistics.py
"""

import os
import re
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_ben_0.txt")
LS_PATTERN = re.compile(r"<ls>([^<]+)</ls>")

def main():
    counter = Counter()
    with open(INPUT, encoding="utf-8") as fh:
        for line in fh:
            counter.update(LS_PATTERN.findall(line))

    total = sum(counter.values())
    items = counter.most_common()

    print(f"{'Value':<30} {'Count':>7} {'Pct':>7} {'Cum':>7}")
    print("-" * 53)

    cum = 0.0
    for value, count in items:
        pct = count / total * 100
        cum += pct
        print(f"{value:<30} {count:>7} {pct:>6.2f}% {cum:>6.2f}%")

    print()
    print(f"Total occurrences: {total}")
    print(f"Unique values: {len(items)}")

if __name__ == "__main__":
    main()
