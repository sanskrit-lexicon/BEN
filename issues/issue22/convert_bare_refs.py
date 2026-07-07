#!/usr/bin/env python3
"""
Wrap bare digit references in BEN text with <ls n="SOURCE">REF</ls>.

Bare refs like "13, 4880." or "6, 36, 117." that appear after a </ls>
tag without their own source abbreviation need source inferred from the
most recent <ls> tag. Source is all non-ref tokens from the merged
content (e.g. "Vedāntas. in Chr." for "Vedāntas. in Chr. 218, 1").

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
    content = re.sub(r'<[^>]+>[^<]*</[^>]+>', '', content)
    content = re.sub(r'<[^>]+>', '', content)
    tokens = content.split()
    parts = []
    for t in tokens:
        if is_ref_start(t):
            break
        parts.append(t)
    return ' '.join(parts) if parts else content


MERGE_PAGE_INTERRUPT_RE = re.compile(
    r'(<ls>([^<]+)</ls>)\.\s*(\[Page[^\]]*\])\s*<ls n="([^"]*)">([^<]+)</ls>'
)


def merge_page_ref_interrupts(text, counter):
    """Merge Roman refs split by [Page...] blocks back into a single <ls> tag.
    
    Pattern: <ls>S_PARTIAL</ls>. [Page...] <ls n="S">REF</ls>
    → <ls>S_PARTIAL. REF</ls> [Page...]
    Only applies to period (ref continuations), not semicolons (list separators).
    """
    def replacer(m):
        tag_content = m.group(2)
        page = m.group(3)
        source_attr = m.group(4)
        ref = m.group(5)
        if not tag_content.startswith(source_attr):
            return m.group(0)
        counter[0] += 1
        return '<ls>%s. %s</ls> %s' % (tag_content, ref, page)
    return MERGE_PAGE_INTERRUPT_RE.sub(replacer, text)


AB_REF_RE = re.compile(
    r'(<ls>([^<]+)</ls>)\.\s*(<ab>([a-z]+)\.</ab>)\s*(\d+)'
)


def merge_ab_refs(text, ab_counts):
    """Merge <ab>-qualified refs split by issue19 into single <ls> tags.
    
    Pattern: <ls>Pañc. iv</ls>. <ab>d.</ab> 79
    → <ls>Pañc. iv. <ab>d.</ab> 79</ls>
    """
    def replacer(m):
        tag_content = m.group(2)
        ab_tag = m.group(3)
        ab_type = m.group(4)
        digits = m.group(5)
        ab_counts[ab_type] = ab_counts.get(ab_type, 0) + 1
        return '<ls>%s. %s %s</ls>' % (tag_content, ab_tag, digits)
    return AB_REF_RE.sub(replacer, text)


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
    page_counter = [0]
    result = merge_page_ref_interrupts(result, page_counter)
    ab_counts = {}
    result = merge_ab_refs(result, ab_counts)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(result)

    input_plain = data.count('<ls>')
    input_n = data.count('<ls n=')
    output_plain = result.count('<ls>')
    output_n = result.count('<ls n=')
    print('=== Statistics ===')
    print(f'1. Bare ref wrapping:         {output_n} new <ls n="..."> tags')
    print(f'   (input had {input_n}, output has {output_n})')
    print(f'2. Page-interrupt refs merged: {page_counter[0]}')
    print(f'3. <ab>-qualified refs merged: {sum(ab_counts.values())}')
    for ab_type in sorted(ab_counts):
        print(f'   <ab>{ab_type}.</ab>{" " * (8 - len(ab_type))} {ab_counts[ab_type]}')
    print(f'')
    print(f'Input  <ls> tags:  {input_plain}')
    print(f'Output <ls> tags:  {output_plain}')
    print(f'Lines modified:    ~{wrapped_count}')
    print(f'Written to:        {OUTPUT}')


if __name__ == '__main__':
    main()
