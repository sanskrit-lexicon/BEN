#!/usr/bin/env python3
"""
Analyze Roman numeral usage in literary source (<ls>) references.

Classifies each <ls> reference by whether the first number after the
tag is a Roman numeral (i, ii, iii, iv, v, vi, vii, viii, ix, x,
xi, xii, xiii, xiv, xv, xvi, xvii, xviii, xix, xx, etc.) or
an Arabic digit.

Reports per-source statistics on Roman numeral usage patterns.
"""

import os
import re
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_ben_2.txt")
OUTPUT = os.path.join(SCRIPT_DIR, "roman_analysis.txt")

# Pattern to capture <ls> tag content AND trailing reference numbers
# Matches: <ls>Source</ls> followed by the first number token
LS_PATTERN = re.compile(r"<ls>([^<]+)</ls>\s*")

# Roman numeral pattern (lowercase only — no uppercase found in BEN)
ROMAN_RE = re.compile(
    r"^(m{0,3}(?:cm|cd|d?c{0,3})(?:xc|xl|l?x{0,3})(?:ix|iv|v?i{0,3}))$"
)

# Valid Roman numerals to match
ROMAN_NUMS = {
    "i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7, "viii": 8,
    "ix": 9, "x": 10, "xi": 11, "xii": 12, "xiii": 13, "xiv": 14, "xv": 15,
    "xvi": 16, "xvii": 17, "xviii": 18, "xix": 19, "xx": 20,
    "xxi": 21, "xxii": 22, "xxiii": 23, "xxiv": 24, "xxv": 25,
    "xxx": 30, "xl": 40, "l": 50, "lx": 60, "lxx": 70, "lxxx": 80,
    "xc": 90, "c": 100, "ci": 101, "cv": 105, "cx": 110,
    "cl": 150, "cc": 200, "ccc": 300, "cd": 400, "d": 500,
}

ROMAN_SET = set(ROMAN_NUMS.keys())

# Regex to extract the first token after <ls> tag
FIRST_TOKEN = re.compile(r"^\s*([a-z]+|[0-9]+)")


def is_roman(s):
    return s in ROMAN_SET


def is_arabic(s):
    return s.isdigit()


def classify_ref(src, after_tag):
    """
    Classify a single <ls> reference.
    Returns (first_token, type) where type is 'roman', 'arabic', 'other', or None.
    """
    m = FIRST_TOKEN.search(after_tag)
    if not m:
        return None, None
    token = m.group(1)
    if is_roman(token):
        return token, "roman"
    elif is_arabic(token):
        return token, "arabic"
    else:
        return token, "other"


def main():
    # Data structures: src -> list of (token, type, trailing, line_no, line)
    records = defaultdict(list)

    with open(INPUT, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line_stripped = line.rstrip("\n")
            # Find all <ls> tags in this line
            for m in LS_PATTERN.finditer(line_stripped):
                src = m.group(1)
                after = line_stripped[m.end():]
                token, typ = classify_ref(src, after)
                if token is not None:
                    records[src].append((token, typ, after[:60], lineno, line_stripped))

    order = sorted(records, key=lambda k: len(records[k]), reverse=True)

    out_lines = []
    out_lines.append("Roman Numeral Usage in <ls> References")
    out_lines.append("=" * 70)
    out_lines.append("")

    total_refs = sum(len(v) for v in records.values())
    total_src = len(records)
    total_roman = sum(
        sum(1 for r in recs if r[1] == "roman") for recs in records.values()
    )
    total_arabic = sum(
        sum(1 for r in recs if r[1] == "arabic") for recs in records.values()
    )
    total_other = total_refs - total_roman - total_arabic

    out_lines.append(f"Total <ls> references with first-token analysis: {total_refs}")
    out_lines.append(f"Total sources: {total_src}")
    out_lines.append(f"Roman numeral first tokens: {total_roman} ({total_roman/total_refs*100:.1f}%)")
    out_lines.append(f"Arabic digit first tokens:  {total_arabic} ({total_arabic/total_refs*100:.1f}%)")
    out_lines.append(f"Other:                     {total_other} ({total_other/total_refs*100:.1f}%)")
    out_lines.append("")

    # Per-source summary table
    out_lines.append(f"{'Source':<40} {'Total':>7} {'Roman':>7} {'Arabic':>7} {'Other':>7} {'% Roman':>9}")
    out_lines.append(f"{'─'*80}")
    for src in order:
        recs = records[src]
        total = len(recs)
        n_roman = sum(1 for r in recs if r[1] == "roman")
        n_arabic = sum(1 for r in recs if r[1] == "arabic")
        n_other = total - n_roman - n_arabic
        pct_roman = n_roman / total * 100 if total else 0
        out_lines.append(
            f"{src:<40} {total:>7} {n_roman:>7} {n_arabic:>7} {n_other:>7} {pct_roman:>8.1f}%"
        )
    out_lines.append("")

    # ─── SOURCES THAT USE ROMAN NUMERALS ───
    out_lines.append("=" * 70)
    out_lines.append("SOURCES USING ROMAN NUMERALS")
    out_lines.append("=" * 70)
    out_lines.append("")

    roman_users = [(src, recs) for src, recs in records.items()
                   if any(r[1] == "roman" for r in recs)]
    roman_users.sort(key=lambda x: -sum(1 for r in x[1] if r[1] == "roman"))

    for src, recs in roman_users:
        total = len(recs)
        n_roman = sum(1 for r in recs if r[1] == "roman")
        n_arabic = sum(1 for r in recs if r[1] == "arabic")
        pct = n_roman / total * 100

        # Collect unique Roman numerals used
        romans_used = sorted(set(r[0] for r in recs if r[1] == "roman"),
                             key=lambda x: ROMAN_NUMS.get(x, 999))

        # Count occurrences per Roman numeral
        rom_count = defaultdict(int)
        for r in recs:
            if r[1] == "roman":
                rom_count[r[0]] += 1

        rom_summary = ", ".join(f"{rn}={rom_count[rn]}" for rn in romans_used)

        out_lines.append(
            f"{src:<40} {total:>5} refs, {n_roman:>5} Roman ({pct:>5.1f}%), "
            f"{n_arabic:>5} Arabic"
        )
        out_lines.append(f"  Roman numerals: {rom_summary}")
        out_lines.append("")

    # ─── MIXED USAGE ───
    out_lines.append("=" * 70)
    out_lines.append("SOURCES WITH MIXED ROMAN + ARABIC USAGE")
    out_lines.append("=" * 70)
    out_lines.append("")

    mixed_users = [(src, recs) for src, recs in records.items()
                   if any(r[1] == "roman" for r in recs)
                   and any(r[1] == "arabic" for r in recs)]
    mixed_users.sort(key=lambda x: -len(x[1]))

    wrote_any = False
    for src, recs in mixed_users:
        wrote_any = True
        total = len(recs)
        n_roman = sum(1 for r in recs if r[1] == "roman")
        n_arabic = sum(1 for r in recs if r[1] == "arabic")
        out_lines.append(
            f"{src:<40} {total:>5} refs — {n_roman:>4} Roman, {n_arabic:>4} Arabic"
        )

        # Show up to 5 examples of Roman usage
        roman_examples = [r for r in recs if r[1] == "roman"][:5]
        for token, typ, after, lineno, ln in roman_examples:
            short = after[:80]
            out_lines.append(f"  L{lineno:>6} Roman [{token}]: <ls>{src}</ls> {short}")

        # Show up to 5 examples of Arabic usage (first tokens)
        arabic_examples = [r for r in recs if r[1] == "arabic"][:5]
        for token, typ, after, lineno, ln in arabic_examples:
            short = after[:80]
            out_lines.append(f"  L{lineno:>6} Arabic [{token}]: <ls>{src}</ls> {short}")

        out_lines.append("")

    if not wrote_any:
        out_lines.append("  (none)")

    # ─── REFS WHERE FIRST TOKEN IS NEITHER ROMAN NOR ARABIC ───
    out_lines.append("=" * 70)
    out_lines.append("REFS WITH NON-ROMAN/NON-ARABIC FIRST TOKENS")
    out_lines.append("=" * 70)
    out_lines.append("")

    other_refs = []
    for src, recs in records.items():
        for r in recs:
            if r[1] == "other":
                other_refs.append((src, r[0], r[3], r[4]))

    if other_refs:
        for src, token, lineno, ln in other_refs[:30]:
            short = ln[:120]
            out_lines.append(f"  L{lineno:>6} [{src}] first token '{token}': {short}")
        if len(other_refs) > 30:
            out_lines.append(f"  ... and {len(other_refs) - 30} more")
    else:
        out_lines.append("  (none)")

    # ─── DETAIL PER SOURCE THAT USES ROMAN ───
    out_lines.append("")
    out_lines.append("=" * 70)
    out_lines.append("DETAILED ROMAN USAGE PER SOURCE")
    out_lines.append("=" * 70)
    out_lines.append("")

    for src, recs in roman_users:
        n_roman = sum(1 for r in recs if r[1] == "roman")
        # Count by specific Roman numeral
        rom_count = defaultdict(int)
        rom_examples = defaultdict(list)
        for r in recs:
            if r[1] == "roman":
                rom_count[r[0]] += 1
                if len(rom_examples[r[0]]) < 2:
                    rom_examples[r[0]].append(r[3])  # line_no

        out_lines.append(f"{src} ({n_roman} Roman refs)")
        for rn in sorted(rom_count, key=lambda x: ROMAN_NUMS.get(x, 999)):
            ex_lines = ", ".join(f"L{no}" for no in rom_examples[rn])
            out_lines.append(f"  {rn:<6} ×{rom_count[rn]:>4}  e.g. {ex_lines}")
        out_lines.append("")

    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out_lines))

    print(f"Written to {OUTPUT}")


if __name__ == "__main__":
    main()
