"""step4.py — Copy Greek tags from CDSL into AB version.

Reads CDSL (temp_cdsl_ben3.txt) and AB (temp_ab_ben3.txt), matches
entries by <L> number, and replaces each <lang n="greek">...</lang>
in AB with the corresponding tag from CDSL (which has more accurate
Greek text).  Entries where the tag count differs are left unchanged.
Output: derivatives/temp_ab_ben4.txt
"""

import os
import re
import sys

SRC_CDSL = "derivatives/temp_cdsl_ben3.txt"
SRC_AB = "derivatives/temp_ab_ben3.txt"
OUT_AB = "derivatives/temp_ab_ben4.txt"
DIR = os.path.dirname(os.path.abspath(__file__))

GREEK_RE = re.compile(r'<lang n="greek">.*?</lang>', re.DOTALL)
ENTRY_SPLIT_RE = re.compile(r'(?=<L>\d+<pc>)')


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_entries(text):
    """Split file text into entry strings at every '<L>N<pc>'."""
    parts = ENTRY_SPLIT_RE.split(text)
    return [p for p in parts if p.strip()]


def entry_number(entry):
    m = re.match(r'<L>(\d+)', entry)
    return int(m.group(1)) if m else None


def extract_greek(text):
    return GREEK_RE.findall(text)


def replace_greek(text, new_tags):
    """Replace every <lang n="greek">...</lang> in text with new_tags in order."""
    it = iter(new_tags)

    def sub(m):
        try:
            return next(it)
        except StopIteration:
            return m.group(0)

    return GREEK_RE.sub(sub, text)


def main():
    cdsl_raw = read_file(os.path.join(DIR, SRC_CDSL))
    ab_raw = read_file(os.path.join(DIR, SRC_AB))

    cdsl_entries = split_entries(cdsl_raw)
    ab_entries = split_entries(ab_raw)

    cdsl_by_num = {}
    for e in cdsl_entries:
        n = entry_number(e)
        if n is not None:
            cdsl_by_num[n] = e

    stats = {"matched": 0, "updated": 0, "count_mismatch": 0, "no_match": 0}
    out_parts = []

    for entry in ab_entries:
        num = entry_number(entry)
        if num is not None and num in cdsl_by_num:
            stats["matched"] += 1
            cdsl_entry = cdsl_by_num[num]
            cdsl_tags = extract_greek(cdsl_entry)
            ab_tags = extract_greek(entry)
            if cdsl_tags:
                if len(cdsl_tags) == len(ab_tags):
                    updated = replace_greek(entry, cdsl_tags)
                    if updated != entry:
                        stats["updated"] += 1
                    out_parts.append(updated)
                else:
                    stats["count_mismatch"] += 1
                    out_parts.append(entry)
            else:
                out_parts.append(entry)
        else:
            if num is not None:
                stats["no_match"] += 1
            out_parts.append(entry)

    out_text = "".join(out_parts)
    out_path = os.path.join(DIR, OUT_AB)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out_text)

    ab_orig_size = os.path.getsize(os.path.join(DIR, SRC_AB))
    ab_new_size = os.path.getsize(out_path)

    print("=== step4.py completed ===")
    print(f"  Output AB: {OUT_AB}")
    print(f"  Matched entries:         {stats['matched']}")
    print(f"  Greek tags updated:      {stats['updated']}")
    print(f"  Count mismatches (kept): {stats['count_mismatch']}")
    print(f"  Unmatched AB entries:    {stats['no_match']}")
    print(f"  Original AB:  {ab_orig_size} bytes")
    print(f"  Updated AB:   {ab_new_size} bytes")


if __name__ == "__main__":
    main()
