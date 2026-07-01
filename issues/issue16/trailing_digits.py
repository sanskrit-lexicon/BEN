#!/usr/bin/env python3
"""
Analyze trailing digit blocks after <ls> tags.

For each source, count how many digit blocks follow the </ls>
(e.g., '<ls>Man.</ls> 9, 47.' → 2 digit blocks: 9, 47).
"""

import os
import re
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_ben_0.txt")
OUTPUT = os.path.join(SCRIPT_DIR, "trailing_digits.txt")

# Pattern: <ls>SOURCE</ls> followed by digits, commas, spaces, ending with period or semicolon
PATTERN = re.compile(r"<ls>([^<]+)</ls>\s*([0-9,\s]+?)[.;]")
DIGIT_BLOCK = re.compile(r"\d+")

def main():
    src_blocks = defaultdict(list)  # src -> [num_blocks]

    with open(INPUT, encoding="utf-8") as fh:
        for line in fh:
            for m in PATTERN.finditer(line):
                src = m.group(1)
                trailing = m.group(2)
                blocks = DIGIT_BLOCK.findall(trailing)
                src_blocks[src].append(len(blocks))

    order = sorted(src_blocks, key=lambda k: len(src_blocks[k]), reverse=True)

    lines = []
    lines.append("Trailing Digit Block Analysis for <ls> tags")
    lines.append("=" * 70)
    total = sum(len(v) for v in src_blocks.values())
    lines.append(f"Total matches: {total}")
    lines.append(f"Total sources: {len(src_blocks)}")
    lines.append("")
    lines.append(f"{'Source':<35} {'Total':>6} {'1-blk':>6} {'2-blk':>6} {'3-blk':>6} {'4+blk':>6} {'Consistent?':>12}")
    lines.append(f"{'─'*80}")

    for src in order:
        counts = src_blocks[src]
        total_src = len(counts)
        c = Counter(counts)
        n1 = c.get(1, 0)
        n2 = c.get(2, 0)
        n3 = c.get(3, 0)
        n_plus = sum(v for k, v in c.items() if k >= 4)

        top_frac = max(n1, n2, n3, n_plus) / total_src if total_src > 0 else 0
        if top_frac >= 0.95:
            cons = "\u2713"
        elif top_frac >= 0.80:
            cons = "~"
        else:
            cons = "\u2717"

        lines.append(f"{src:<35} {total_src:>6} {n1:>6} {n2:>6} {n3:>6} {n_plus:>6} {cons:>12}")
    lines.append("")
    lines.append("Note: \u2713 = >=95% of refs have same block count, ~ = 80-94%, \u2717 = <80%")

    # Detailed per source
    lines.append("")
    lines.append("=" * 70)
    lines.append("DETAILED BREAKDOWN")
    lines.append("=" * 70)

    for src in order:
        counts = src_blocks[src]
        total_src = len(counts)
        c = Counter(counts)

        lines.append("")
        lines.append(f"{'─'*60}")
        lines.append(f"{src} ({total_src} total)")
        lines.append(f"{'─'*60}")

        for n in sorted(c.keys()):
            pct = c[n] / total_src * 100
            label = f"{n} digit block{'s' if n != 1 else ''}"
            lines.append(f"  {label:<20} {c[n]:>5} ({pct:>5.1f}%)")

        # If multiple patterns found, show examples of each
        if len(c) > 1:
            lines.append(f"  Pattern variants:")
            ex_seen = {}
            with open(INPUT, encoding="utf-8") as fh:
                for line in fh:
                    all_done = all(ex_seen.get(n, 0) >= 2 for n in c.keys())
                    if all_done:
                        break
                    for m in PATTERN.finditer(line):
                        if m.group(1) == src:
                            trailing = m.group(2)
                            blocks = DIGIT_BLOCK.findall(trailing)
                            n = len(blocks)
                            if n in c and ex_seen.get(n, 0) < 2:
                                ex_seen[n] = ex_seen.get(n, 0) + 1
                                lines.append(f"    {n} blk: <ls>{src}</ls> {trailing}")

    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"Written to {OUTPUT}")

if __name__ == "__main__":
    main()
