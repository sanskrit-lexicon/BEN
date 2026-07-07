#!/usr/bin/env python3
"""
Wrap bare source+ref patterns (source outside <ls> tags) in BEN text.

Pattern: "Kumāras. 6, 2" where "Kumāras." is a known source abbreviation
and "6, 2" is a digit reference. Both appear in text outside any <ls> tag.

Input : temp_be2edf5.txt  (base file)
Output: temp_ben_1.txt    (bare source+ref wrapped in <ls> tags)
"""

import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_be2edf5.txt")
OUTPUT = os.path.join(SCRIPT_DIR, "temp_ben_1.txt")

ROMAN_NUMS = {
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii",
    "ix", "x", "xi", "xii", "xiii", "xiv", "xv", "xvi",
    "xvii", "xviii", "xix", "xx", "xxi", "xxii", "xxiii", "xxiv", "xxv",
    "xxx", "xl", "l", "lx", "lxx", "lxxx", "xc", "c",
    "ci", "cv", "cx", "cl", "cc", "ccc", "cd", "d",
}

LS_TAG_RE = re.compile(r'<ls\b[^>]*>.*?</ls>')

def is_ref_start(tok):
    clean = tok.rstrip(',.;:')
    if clean.isdigit():
        return True
    if clean.lower() in ROMAN_NUMS:
        return True
    return False

def extract_source(content):
    content = re.sub(r'<[^>]+>[^<]*</[^>]+>', '', content)
    content = re.sub(r'<[^>]+>', '', content)
    tokens = content.split()
    parts = []
    for t in tokens:
        if is_ref_start(t):
            break
        parts.append(t)
    return ' '.join(parts) if parts else content


def build_known_sources(text):
    """Build set of known source abbreviations from existing <ls> tags."""
    sources = set()
    for m in re.finditer(r'<ls[^>]*>([^<]+)</ls>', text):
        s = extract_source(m.group(1))
        if s:
            sources.add(s)
    return sorted(sources, key=len, reverse=True)


def find_bare_source_refs(line, sources_re):
    """Find (source, ref, start, end) tuples for bare source+ref in line."""
    results = []
    # Collect <ls> spans
    ls_spans = [(m.start(), m.end()) for m in LS_TAG_RE.finditer(line)]

    for m in sources_re.finditer(line):
        start = m.start()
        # Skip if inside <ls> tag
        in_ls = any(ls_start <= start < ls_end for ls_start, ls_end in ls_spans)
        if not in_ls:
            full = m.group(0)
            ref = m.group(1)
            source = full[:-(len(ref))].strip()
            results.append((source, ref, start, m.end()))

    return results


def process(text):
    """Process text, wrapping bare source+ref in <ls> tags."""
    sources_sorted = build_known_sources(text)
    print(f"Known sources: {len(sources_sorted)}")

    # Build combined regex (longest-first alternation)
    escaped = [re.escape(s) for s in sources_sorted]
    sources_re = re.compile(
        r'\b(?:' + '|'.join(escaped) + r')\s+(\d{1,8}(?:,\s*\d{1,8})*)'
    )
    print("Combined regex compiled")

    lines = text.split('\n')
    out_lines = []
    total_wrapped = 0
    total_lines = len(lines)

    for lineno, line in enumerate(lines, 1):
        if lineno % 10000 == 0:
            print(f"  processing line {lineno}/{total_lines}...")

        # Comment line — pass through unchanged
        if line.startswith(';'):
            out_lines.append(line)
            continue

        # Find matches in this line
        matches = find_bare_source_refs(line, sources_re)

        if not matches:
            out_lines.append(line)
            continue

        # Process from right to left to preserve offsets
        result = line
        for source, ref, start, end in reversed(matches):
            # Reconstruct the full match text
            replacement = '<ls>%s %s</ls>' % (source, ref)
            # Find the match in the current result (should be at known position
            # but offsets may have shifted from previous replacements)
            # Instead, search for the source+ref text
            match_text = source + ' ' + ref
            pos = result.find(match_text)
            if pos >= 0:
                result = result[:pos] + replacement + result[pos + len(match_text):]
                total_wrapped += 1

        out_lines.append(result)

    return '\n'.join(out_lines), total_wrapped


def main():
    with open(INPUT, encoding='utf-8') as f:
        data = f.read()

    print(f"Input: {INPUT}")
    print(f"Input <ls> tags: {data.count('<ls>')}")

    result, wrapped = process(data)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(result)

    print()
    print(f"=== Statistics ===")
    print(f"Bare source+ref wrapped: {wrapped}")
    print(f"Input  <ls> tags:  {data.count('<ls>')}")
    print(f"Output <ls> tags:  {result.count('<ls>')}")
    print(f"Written to: {OUTPUT}")


if __name__ == '__main__':
    main()
