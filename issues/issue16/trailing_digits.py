#!/usr/bin/env python3
"""
Analyze trailing digit blocks after <ls> tags.

For each source, count how many digit blocks follow the </ls>
(e.g., '<ls>Man.</ls> 9, 47.' → 2 digit blocks: 9, 47).

For sources with a dominant pattern (>=95%), report all
non-conforming references with their full lines.
"""

import os
import re
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_ben_2.txt")
OUTPUT = os.path.join(SCRIPT_DIR, "trailing_digits.txt")

# Pattern: <ls>SOURCE</ls> followed by one or more digit blocks separated by
# commas/spaces.  Stops at the first character that isn't a digit, comma, or
# space (no terminating [.;] required, which captures cross-refs like
# "289, 2 = <ls>Rigv.</ls>" where the digit blocks are followed by space+equals).
PATTERN = re.compile(r"<ls>([^<]+)</ls>\s*(\d+(?:[\s,]*\d+)*)")
DIGIT_BLOCK = re.compile(r"\d+")


def main():
    # src -> [(num_blocks, trailing_text, full_line, line_no)]
    records = defaultdict(list)

    with open(INPUT, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line_stripped = line.rstrip("\n")
            for m in PATTERN.finditer(line_stripped):
                src = m.group(1)
                trailing = m.group(2).strip()
                blocks = DIGIT_BLOCK.findall(trailing)
                records[src].append((len(blocks), trailing, line_stripped, lineno))

    order = sorted(records, key=lambda k: len(records[k]), reverse=True)

    out_lines = []
    out_lines.append("Trailing Digit Block Analysis for <ls> tags")
    out_lines.append("=" * 70)
    total = sum(len(v) for v in records.values())
    out_lines.append(f"Total matches: {total}")
    out_lines.append(f"Total sources: {len(records)}")
    out_lines.append("")
    out_lines.append(
        f"{'Source':<35} {'Total':>6} {'1-blk':>6} {'2-blk':>6} {'3-blk':>6} {'4+blk':>6} {'Consistent?':>12}"
    )
    out_lines.append(f"{'─'*80}")

    # Per-source stats
    stats = {}
    for src in order:
        recs = records[src]
        total_src = len(recs)
        c = Counter(r[0] for r in recs)
        n1 = c.get(1, 0)
        n2 = c.get(2, 0)
        n3 = c.get(3, 0)
        n_plus = sum(v for k, v in c.items() if k >= 4)

        top_n, top_count = c.most_common(1)[0]
        top_frac = top_count / total_src if total_src > 0 else 0
        if top_frac >= 0.95:
            cons = "\u2713"
        elif top_frac >= 0.80:
            cons = "~"
        else:
            cons = "\u2717"

        stats[src] = {
            "total": total_src,
            "n1": n1,
            "n2": n2,
            "n3": n3,
            "n_plus": n_plus,
            "top_n": top_n,
            "top_frac": top_frac,
            "cons": cons,
            "c": c,
        }

        out_lines.append(
            f"{src:<35} {total_src:>6} {n1:>6} {n2:>6} {n3:>6} {n_plus:>6} {cons:>12}"
        )
    out_lines.append("")
    out_lines.append(
        "Note: \u2713 = >=95% of refs have same block count, ~ = 80-94%, \u2717 = <80%"
    )

    # ─── NON-CONFORMING REFERENCES ───
    out_lines.append("")
    out_lines.append("=" * 70)
    out_lines.append("NON-CONFORMING REFERENCES (all sources)")
    out_lines.append("=" * 70)
    out_lines.append("")

    wrote_any = False
    for src in order:
        s = stats[src]
        recs = records[src]
        non_conf = [(nb, tr, ln, no) for (nb, tr, ln, no) in recs if nb != s["top_n"]]
        if not non_conf:
            continue

        wrote_any = True
        pct = s["top_frac"] * 100
        out_lines.append(
            f"Source: {src} ({len(non_conf)} non-conforming out of {s['total']}, "
            f"{pct:.1f}% {s['top_n']}-blk)"
        )
        out_lines.append(f"{'─'*60}")

        for nb, tr, ln, no in non_conf:
            plural = "s" if nb != 1 else ""
            out_lines.append(f"  L{no:>6}  {nb} blk{plural}: <ls>{src}</ls> {tr}")
            out_lines.append(f"         LINE: {ln}")
            out_lines.append("")

    if not wrote_any:
        out_lines.append("  (none)")

    # ─── DETAILED BREAKDOWN ───
    out_lines.append("=" * 70)
    out_lines.append("DETAILED BREAKDOWN")
    out_lines.append("=" * 70)

    for src in order:
        s = stats[src]
        recs = records[src]
        total_src = s["total"]
        c = s["c"]

        out_lines.append("")
        out_lines.append(f"{'─'*60}")
        out_lines.append(f"{src} ({total_src} total)")
        out_lines.append(f"{'─'*60}")

        for n in sorted(c.keys()):
            pct = c[n] / total_src * 100
            label = f"{n} digit block{'s' if n != 1 else ''}"
            out_lines.append(f"  {label:<20} {c[n]:>5} ({pct:>5.1f}%)")

        # Show up to 2 examples of each variant
        if len(c) > 1:
            out_lines.append(f"  Pattern variants:")
            ex_seen = {}
            for nb, tr, ln, _ in recs:
                if all(ex_seen.get(n, 0) >= 2 for n in c.keys()):
                    break
                if nb in c and ex_seen.get(nb, 0) < 2:
                    ex_seen[nb] = ex_seen.get(nb, 0) + 1
                    out_lines.append(f"    {nb} blk: <ls>{src}</ls> {tr}")

    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out_lines))

    print(f"Written to {OUTPUT}")


if __name__ == "__main__":
    main()
