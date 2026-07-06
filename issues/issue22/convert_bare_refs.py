#!/usr/bin/env python3
"""
Wrap bare digit references in BEN text with <ls n="SOURCE">REF</ls>.

Bare refs like "13, 4880." or "6, 36, 117." that appear after a </ls>
tag without their own source abbreviation need source inferred from the
most recent <ls> tag. The "in" pattern (e.g. "Daśak. in Chr. 184, 12")
uses the inner source ("Chr.") as the implied source for subsequent bare refs.

Input : temp_7c2fdca.txt  (issue19 merged format with page-ref fixes)
Output: temp_ben_1.txt    (bare refs wrapped with inferred source)
"""

import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_7c2fdca.txt")
OUTPUT = os.path.join(SCRIPT_DIR, "temp_ben_1.txt")

ROMAN_NUMS = {
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii",
    "ix", "x", "xi", "xii", "xiii", "xiv", "xv", "xvi",
    "xvii", "xviii", "xix", "xx", "xxi", "xxii", "xxiii", "xxiv", "xxv",
    "xxx", "xl", "l", "lx", "lxx", "lxxx", "xc", "c",
    "ci", "cv", "cx", "cl", "cc", "ccc", "cd", "d",
}

BARE_REF_RE = re.compile(r'(?<!\d)(\d{1,4},\s*\d{1,4}(?:,\s*\d{1,4})?)(?!\d)')

TAG_RE = re.compile(r'(<ls[^>]*>.*?</ls>)')


def is_ref_start(tok):
    clean = tok.rstrip(',.;:')
    if clean.isdigit():
        return True
    if clean.lower() in ROMAN_NUMS:
        return True
    return False


def extract_source(content):
    """Extract the source abbreviation from merged <ls> content."""
    m = re.search(r'\sin\.?\s', content)
    if m:
        content = content[m.end():]
    content = re.sub(r'<[^>]+>[^<]*</[^>]+>', '', content)
    content = re.sub(r'<[^>]+>', '', content)
    tokens = content.split()
    parts = []
    for t in tokens:
        if is_ref_start(t):
            break
        parts.append(t)
    return ' '.join(parts) if parts else content


def is_false_positive_match(text, match_end):
    """Check if a bare ref match is a false positive (has source word before it)."""
    before = text[max(0, match_end - 60):match_end].rstrip()
    if re.search(r'\b[A-Z][a-zA-Zāīūṛṝḷḹēōṣṭḍñṅ]*\.\s*$', before):
        return True
    return False


def wrap_bare_refs(segment, source):
    """Wrap bare ref patterns in segment with source tags."""
    if not source:
        return segment
    out = []
    last_end = 0
    for m in BARE_REF_RE.finditer(segment):
        if not is_false_positive_match(segment, m.start()):
            ref = m.group(1)
            out.append(segment[last_end:m.start()])
            out.append('<ls n="%s">%s</ls>' % (source, ref))
            last_end = m.end()
        else:
            out.append(segment[last_end:m.end()])
            last_end = m.end()
    out.append(segment[last_end:])
    return ''.join(out)


def process(text):
    lines = text.split('\n')
    out_lines = list(lines)
    current_source = None
    entry_start = True
    total_wrapped = 0

    for row_idx, line in enumerate(lines):
        if line.startswith('<L>'):
            entry_start = True

        parts = TAG_RE.split(line)
        new_parts = []
        for i, part in enumerate(parts):
            if TAG_RE.fullmatch(part):
                m = re.match(r'<ls[^>]*>(.*?)</ls>', part)
                if m and 'n=' not in part:
                    content = m.group(1)
                    current_source = extract_source(content)
                    entry_start = False
                new_parts.append(part)
            else:
                src = current_source if not entry_start else None
                wrapped = wrap_bare_refs(part, src)
                new_parts.append(wrapped)
                if wrapped != part:
                    total_wrapped += 1

        out_lines[row_idx] = ''.join(new_parts)

    return '\n'.join(out_lines), total_wrapped


def main():
    with open(INPUT, encoding='utf-8') as f:
        data = f.read()

    result, wrapped_count = process(data)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(result)

    input_tags = data.count('<ls>')
    output_tags = result.count('<ls>')
    print(f'Input  <ls> tags: {input_tags}')
    print(f'Output <ls> tags: {output_tags}')
    print(f'New tags added:  {output_tags - input_tags}')
    print(f'Lines modified:  ~{wrapped_count}')
    print(f'Written to:      {OUTPUT}')


if __name__ == '__main__':
    main()
