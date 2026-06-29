#!/usr/bin/env python3
"""step3.py - Transfer page line numbers from CDSL to AB.

CDSL has [PageNNNN-x + NN] references (with line numbers on the page),
while AB has [PageNNNN-x] (without line numbers). This script inserts
the line numbers into the AB version.

Output:
  derivatives/temp_cdsl_ben3.txt — CDSL (copied as-is)
  derivatives/temp_ab_ben3.txt   — AB with line numbers inserted
"""

import re
import os

CDSL_FILE = "derivatives/temp_cdsl_ben2.txt"
AB_FILE = "derivatives/temp_ab_ben2.txt"
DERIV_DIR = "derivatives"


def main():
    os.makedirs(DERIV_DIR, exist_ok=True)

    with open(CDSL_FILE, 'r') as f:
        cdsl = f.read()
    with open(AB_FILE, 'r') as f:
        ab = f.read()

    # Extract all CDSL page references with line numbers
    cdsl_refs = re.findall(r'\[Page(\d+-[a-z]) \+ (\d+)\]', cdsl)
    print(f"CDSL page+line references: {len(cdsl_refs)}")

    # Extract all AB page references (without line numbers)
    ab_refs = re.findall(r'\[Page(\d+-[a-z])\]', ab)
    print(f"AB page references:        {len(ab_refs)}")

    if len(cdsl_refs) != len(ab_refs):
        print(f"  Warning: count mismatch ({len(cdsl_refs)} vs {len(ab_refs)})")

    # Build a mapping: page key -> line number
    # Use list for sequential matching based on order
    ab_new = ab
    insertions = 0
    for (page_letter, line_num) in cdsl_refs:
        old = f'[Page{page_letter}]'
        new = f'[Page{page_letter} + {line_num}]'
        if old in ab_new:
            ab_new = ab_new.replace(old, new, 1)
            insertions += 1
        else:
            print(f"  Warning: {old} not found in AB")

    print(f"Line numbers inserted:    {insertions}")

    cdsl_out = os.path.join(DERIV_DIR, 'temp_cdsl_ben3.txt')
    with open(cdsl_out, 'w') as f:
        f.write(cdsl)

    ab_out = os.path.join(DERIV_DIR, 'temp_ab_ben3.txt')
    with open(ab_out, 'w') as f:
        f.write(ab_new)

    cdsl_size = os.path.getsize(CDSL_FILE)
    ab_orig_size = os.path.getsize(AB_FILE)
    print()
    print(f"=== step3.py completed ===")
    print(f"  Output CDSL: {cdsl_out} ({cdsl_size} bytes)")
    print(f"  Output AB:   {ab_out}")
    print()
    print("To measure diff:")
    print("  git diff --word-diff-regex=. --no-index derivatives/temp_cdsl_ben3.txt derivatives/temp_ab_ben3.txt | wc -c")


if __name__ == '__main__':
    main()
