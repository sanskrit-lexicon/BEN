#!/usr/bin/env python3
"""
Revert BEN <ls> conversion back to original format.

Input : temp_ben_1.txt  (converted: <ls>SRC REF</ls>)
Output: temp_ben_2.txt  (reverted:   <ls>SRC</ls> REF)
"""

import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_ben_1.txt")
OUTPUT = os.path.join(SCRIPT_DIR, "temp_ben_2.txt")

ROMAN_NUMS = {
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii",
    "ix", "x", "xi", "xii", "xiii", "xiv", "xv", "xvi",
    "xvii", "xviii", "xix", "xx", "xxi", "xxii", "xxiii", "xxiv", "xxv",
    "xxx", "xl", "l", "lx", "lxx", "lxxx", "xc", "c",
    "ci", "cv", "cx", "cl", "cc", "ccc", "cd", "d",
}
ROMAN_SET = set(ROMAN_NUMS)


def is_roman(word):
    return word.rstrip('.,;').lower() in ROMAN_SET


def token_is_ref_start(tok):
    """Check if a token looks like the start of a reference number."""
    if tok.startswith('<ab>'):
        return False
    if '[' in tok or ']' in tok:
        return False
    clean = tok.rstrip(',.;')
    digit_clean = clean.replace(',', '')
    if digit_clean.isdigit():
        return True
    # Single uppercase chars (D. for 500, C. for 100, etc.) are too ambiguous
    if len(clean) == 1 and clean.isupper():
        return False
    # Single lowercase d/c/l/m are too ambiguous (German abbreviations like "d." = "der")
    if len(clean) == 1 and clean in 'dclm':
        return False
    if is_roman(tok):
        return True
    return False


def find_ref_start(content):
    """
    Find where the reference starts in converted content.
    Returns (idx_before_ref, ref_kind) or (None, None).
    Skips <ab> tags.
    """
    tokens = []
    token_starts = []
    pos = 0
    while pos < len(content):
        if content[pos] in ' \t':
            pos += 1
            continue
        if content[pos:pos+4] == '<ab>':
            end = content.find('</ab>', pos+4)
            if end >= 0:
                tokens.append(content[pos:end+5])
                token_starts.append(pos)
                pos = end + 5
                continue
            else:
                pos += 1
                continue
        start = pos
        while pos < len(content) and content[pos] not in ' \t':
            pos += 1
        tokens.append(content[start:pos])
        token_starts.append(start)

    for i, tok in enumerate(tokens):
        if token_is_ref_start(tok):
            clean = tok.rstrip(',.;')
            kind = 'arabic' if clean.isdigit() else 'roman'
            return token_starts[i], kind

    return None, None


def split_source_ref(text):
    """
    Split text into (source_abbreviation, ref_text).
    Source is everything before the first ref token (with <ab> tags preserved in ref).
    Returns None if no ref token found.
    """
    ref_start, _ = find_ref_start(text)
    if ref_start is None:
        return None

    pre = text[:ref_start]
    ref = text[ref_start:]

    # Walk through pre — <ab> tags belong to ref, everything else is source
    src_parts = []
    ref_insert = ''
    pos = 0
    while pos < len(pre):
        if pre[pos:pos+4] == '<ab>':
            end = pre.find('</ab>', pos+4)
            if end >= 0:
                extracted = pre[pos:end+5]
                pos = end + 5
                # Include following space in ref (separator between <ab> tags or <ab> and ref number)
                if pos < len(pre) and pre[pos] == ' ':
                    extracted += ' '
                    pos += 1
                ref_insert += extracted
                continue
        src_parts.append(pre[pos])
        pos += 1

    src = ''.join(src_parts).strip()
    if ref_insert:
        ref = ref_insert.rstrip() + ' ' + ref.lstrip()
    ref = ref.strip()

    if not src:
        return None

    return src, ref


def revert_content(content):
    """
    Revert a single <ls> content string.
    Returns (new_tags, after_ref) or None if no conversion to revert.
    
    new_tags: list of source abbreviations (for <ls> tags)
    after_ref: text to place after </ls> (ref content with <ab> tags)
    """
    # Handle "in" pattern (with optional period after "in")
    in_match = re.search(r'\sin\.?\s', content)
    if in_match:
        before_in = content[:in_match.start()]
        sep = content[in_match.start():in_match.end()].strip()
        after_in = content[in_match.end():]
        result = split_source_ref(after_in)
        if result is not None:
            src2, ref = result
            return [before_in.strip(), f'{sep} {src2}'], ref

    # Regular case: find ref start
    result = split_source_ref(content)
    if result is not None:
        src, ref = result
        return [src], ref

    return None


def revert_text(text):
    out = []
    i = 0
    reverted_count = 0

    while i < len(text):
        m = re.search(r'<ls>[^<]*(?:<ab>[^<]*</ab>[^<]*)*</ls>', text[i:])
        if not m:
            m = re.search(r'<ls>([^<]*)</ls>', text[i:])
            if not m:
                out.append(text[i:])
                break

        out.append(text[i:i + m.start()])
        tag_start = i + m.start()
        tag_end = i + m.end()

        # Get content between <ls> and </ls>
        content = text[tag_start + 4:tag_end - 5]

        result = revert_content(content)
        if result is not None:
            parts, ref = result
            reverted_count += 1
            if len(parts) == 1:
                out.append(f'<ls>{parts[0]}</ls> {ref}')
            elif len(parts) == 2 and (parts[1].startswith('in ') or parts[1].startswith('in. ')):
                idx = 4 if parts[1].startswith('in. ') else 3
                sep = parts[1][:idx].rstrip()
                src2 = parts[1][idx:]
                out.append(f'<ls>{parts[0]}</ls> {sep} <ls>{src2}</ls> {ref}')
            i = tag_end
        else:
            out.append(text[tag_start:tag_end])
            i = tag_end

    return ''.join(out), reverted_count


def main():
    with open(INPUT, encoding='utf-8') as f:
        data = f.read()

    result, reverted = revert_text(data)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(result)

    total_tags = data.count('<ls>')
    print(f'Input  <ls> tags:  {total_tags}')
    print(f'Output <ls> tags:  {result.count("<ls>")}')
    print(f'Reverted:          {reverted}')
    print(f'Written to:        {OUTPUT}')


if __name__ == '__main__':
    main()
