#!/usr/bin/env python3
"""step2.py - Tag abbreviations using re.sub with negative lookbehind.
Skips already-tagged abbreviations and ambiguous ones.
"""
import re
import os

CDSL_FILE = "derivatives/temp_cdsl_ben1.txt"
AB_FILE = "derivatives/temp_ab_ben1.txt"
DERIV_DIR = "derivatives"


def get_abbr_counts(text):
    counts = {}
    for m in re.finditer(r'<ab>([^<]+)</ab>', text):
        tag = m.group(1)
        counts[tag] = counts.get(tag, 0) + 1
    return counts


def find_untagged_abbrs(cdsl, ab):
    cdsl_tags = get_abbr_counts(cdsl)
    ab_tags = get_abbr_counts(ab)
    result = []
    for abbr, ab_cnt in ab_tags.items():
        cdsl_cnt = cdsl_tags.get(abbr, 0)
        if ab_cnt > cdsl_cnt:
            result.append((ab_cnt - cdsl_cnt, ab_cnt, cdsl_cnt, abbr))
    result.sort(key=lambda x: (-len(x[3]), -x[0]))
    return result


EXCLUDE = {
    'v.', 'pr.', 's.', 'German', 'Ptcple', 'Hariv.', 'Vedāntas.',
    'Böhtl.', 'Gorr.', 'Nalod.', 'dual', 'act.', 'ord.',
    'Ptcple', 'Gr.', 'Lenz.', 'Ball.', 'Bhvr.',
}


def needs_tagging(abbr, need):
    if abbr in EXCLUDE:
        return False
    if need < 1:
        return False
    if len(abbr) <= 2 and need < 5:
        return False
    return True


def tag_one(text, abbr, patterns):
    """Tag one abbreviation using given patterns, skipping already-tagged."""
    for pat_fmt in patterns:
        pat = pat_fmt.format(re.escape(abbr))
        if re.search(pat, text):
            text = re.sub(pat, lambda m: m.group(0).replace(abbr, f'<ab>{abbr}</ab>'), text)
    return text


def main():
    os.makedirs(DERIV_DIR, exist_ok=True)

    with open(CDSL_FILE, 'r') as f:
        cdsl = f.read()
    with open(AB_FILE, 'r') as f:
        ab = f.read()

    abbreviations = find_untagged_abbrs(cdsl, ab)
    total_need = sum(n for n, _, _, _ in abbreviations)
    significant = [(n, a, c, abbr) for n, a, c, abbr in abbreviations if needs_tagging(abbr, n)]
    print(f"Abbreviations needing tagging: {len(abbreviations)}")
    print(f"After exclusions: {len(significant)}")
    print(f"Total instances needed: {total_need}")

    patterns = [
        r'(?<!<ab>) {0},(?= )',
        r'(?<!<ab>) {0} ',
    ]

    total_tagged = 0
    stats = {}
    for need, ab_cnt, cdsl_cnt, abbr in significant:
        esc = re.escape(abbr)
        esc = re.escape(abbr)
        count = 0
        for pat_fmt in patterns:
            pat = pat_fmt.format(esc)
            before = len(re.findall(pat, cdsl))
            if before > 0:
                cdsl = re.sub(pat, lambda m, a=abbr: m.group(0).replace(a, f'<ab>{a}</ab>'), cdsl)
                count += before
        if count > 0:
            stats[abbr] = count
            total_tagged += count

    print(f"Abbreviations tagged: {total_tagged}")
    print()

    # Merge adjacent <ab> tags that should be a single tag per AB
    merge_map = {
        '<ab>comp.</ab> <ab>adj.</ab>': '<ab>comp. adj.</ab>',
    }
    for old, new in merge_map.items():
        n = cdsl.count(old)
        if n:
            cdsl = cdsl.replace(old, new)
            print(f"  Merged {n} instances of {old!r} -> {new!r}")

    mismatches = []
    for abbr, count in sorted(stats.items(), key=lambda x: -x[1]):
        need = 0
        for n, _, _, a in significant:
            if a == abbr:
                need = n
                break
        diff = count - need
        sym = '+' if diff > 0 else ''
        note = f" ({sym}{diff})" if diff else ""
        print(f"  {abbr:25s} need={need:>4} found={count:>4}{note}")
        if diff:
            mismatches.append((abs(diff), abbr, need, count))

    if mismatches:
        print()
        for d, a, n, c in sorted(mismatches, key=lambda x: -x[0])[:10]:
            sym = '+' if c > n else ''
            print(f"  {a:25s} need={n:>4} found={c:>4} ({sym}{c-n})")
    print()

    cdsl_out = os.path.join(DERIV_DIR, 'temp_cdsl_ben2.txt')
    with open(cdsl_out, 'w') as f:
        f.write(cdsl)

    ab_out = os.path.join(DERIV_DIR, 'temp_ab_ben2.txt')
    with open(ab_out, 'w') as f:
        f.write(ab)

    cdsl_size = os.path.getsize(CDSL_FILE)
    mod_size = os.path.getsize(cdsl_out)
    print(f"=== step2.py completed ===")
    print(f"  Output CDSL: {cdsl_out}")
    print(f"  Input CDSL:  {cdsl_size:>8} bytes")
    print(f"  Output CDSL: {mod_size:>8} bytes")
    print()
    print("To measure diff:")
    print("  git diff --word-diff-regex=. --no-index derivatives/temp_cdsl_ben2.txt derivatives/temp_ab_ben2.txt | wc -c")


if __name__ == '__main__':
    main()
