#!/usr/bin/env python3
"""
Wrap bare single-digit refs after semicolons following <ls> tags.

Pattern: <ls>SOURCE DIGIT, DIGIT</ls>; DIGIT;
  → <ls>SOURCE DIGIT, DIGIT</ls>; <ls n="SOURCE DIGIT,">DIGIT</ls>;

Bare DIGIT after </ls>; uses source from preceding <ls> content
with the last ref number removed (retaining the trailing comma).
"""

import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_d1d0a18.txt")
OUTPUT = os.path.join(SCRIPT_DIR, "temp_ben_1.txt")

TAG_RE = re.compile(r'(<ls[^>]*>.*?</ls>)')
BARE_DIGIT_RE = re.compile(r'(?<=;)\s*(\d+)(?=;)')


def get_source(ls_content):
    """Derive n= source by removing the last token from ls_content."""
    tokens = ls_content.split()
    if len(tokens) >= 2:
        return ' '.join(tokens[:-1])
    return ls_content


def wrap_bare_digits(segment, source):
    """Wrap bare digits after semicolons in segment with <ls n="source">."""
    out = []
    last_end = 0
    count = 0
    for m in BARE_DIGIT_RE.finditer(segment):
        digit = m.group(1)
        pre = segment[last_end:m.start()]
        out.append(pre)
        out.append(' <ls n="%s">%s</ls>' % (source, digit))
        last_end = m.end()
        count += 1
    out.append(segment[last_end:])
    return ''.join(out), count


def process(text):
    lines = text.split('\n')
    out_lines = []
    total_wrapped = 0

    for line in lines:
        parts = TAG_RE.split(line)
        new_parts = []
        current_ls = None

        for part in parts:
            m = TAG_RE.fullmatch(part)
            if m:
                if 'n=' not in part:
                    inner = re.match(r'<ls[^>]*>(.*?)</ls>', part)
                    if inner:
                        current_ls = inner.group(1)
                new_parts.append(part)
            else:
                if current_ls and part:
                    source = get_source(current_ls)
                    wrapped, cnt = wrap_bare_digits(part, source)
                    new_parts.append(wrapped)
                    total_wrapped += cnt
                else:
                    new_parts.append(part)

        out_lines.append(''.join(new_parts))

    return '\n'.join(out_lines), total_wrapped


def main():
    with open(INPUT, encoding='utf-8') as f:
        data = f.read()

    print(f"Input <ls> tags: {data.count('<ls>')}")

    result, wrapped = process(data)

    # Count pattern occurrences in input vs output
    pat = re.compile(r'<ls>[^<]+</ls>;\s*\d+;')
    before = len(pat.findall(data))
    after = len(pat.findall(result))

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Unwrapped '; DIGIT;' patterns: {before} → {after}")
    print(f"Bare refs wrapped: {wrapped}")
    print(f"Output <ls n=...> tags: {result.count('<ls n=')}")
    print(f"Written to: {OUTPUT}")


if __name__ == '__main__':
    main()
