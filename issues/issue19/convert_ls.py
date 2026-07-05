#!/usr/bin/env python3
"""
Convert BEN <ls> references to PWG-style format.

BEN format : <ls>MBh.</ls> 14, 34.
PWG format : <ls>MBh. 14, 34</ls>.

Moves trailing reference numbers from after </ls> to inside the <ls> tag.
"""

import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_c72617.txt")
OUTPUT = os.path.join(SCRIPT_DIR, "temp_ben_1.txt")

# Valid Roman numerals
ROMAN_NUMS = {
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii",
    "ix", "x", "xi", "xii", "xiii", "xiv", "xv", "xvi",
    "xvii", "xviii", "xix", "xx", "xxi", "xxii", "xxiii", "xxiv", "xxv",
    "xxx", "xl", "l", "lx", "lxx", "lxxx", "xc", "c",
    "ci", "cv", "cx", "cl", "cc", "ccc", "cd", "d",
}
ROMAN_SET = set(ROMAN_NUMS)


def extract_ref(text, pos):
    """
    Extract the reference text starting at position pos (which is right after </ls>).
    
    A reference starts with a digit or a valid Roman numeral and continues
    until a sentence terminator (. or ;), a cross-ref delimiter (=),
    another opening tag (<), or a closing parenthesis.
    
    Returns (ref_text, end_pos, kind) where kind is 'arabic' or 'roman',
    or (None, None, None) if no reference follows.
    """
    start = pos
    while start < len(text) and text[start] in ' \t\r\n':
        start += 1

    if start >= len(text):
        return None, None, None

    ch = text[start]

    kind = None
    if ch.isdigit():
        kind = 'arabic'
        ref_start = start
        scan = start
    elif ch in 'ivxlcdm':
        word_match = re.match(r'^([a-z]+)', text[start:])
        if not word_match or word_match.group(1) not in ROMAN_SET:
            return None, None, None
        kind = 'roman'
        ref_start = start
        scan = start
    else:
        return None, None, None

    while scan < len(text):
        ch = text[scan]

        if ch == '.':
            if scan + 1 < len(text) and text[scan + 1] in ' \t\r\n':
                nxt = scan + 1
                while nxt < len(text) and text[nxt] in ' \t\r\n':
                    nxt += 1
                if nxt < len(text) and (text[nxt].isdigit() or text[nxt] in 'ivxlcdm'):
                    scan += 1
                    continue
            return text[ref_start:scan], scan, kind

        if ch == ';':
            return text[ref_start:scan], scan, kind

        if ch.isdigit():
            scan += 1
            continue

        if ch == ',':
            scan += 1
            continue

        if ch in ' \t\r\n':
            nxt = scan + 1
            while nxt < len(text) and text[nxt] in ' \t\r\n':
                nxt += 1
            if nxt >= len(text):
                return text[ref_start:scan].rstrip(), scan, kind
            nc = text[nxt]
            if nc.isdigit() or nc in 'ivxlcdm':
                scan = nxt
                continue
            elif nc == '=':
                return text[ref_start:scan].rstrip(), scan, kind
            elif nc == '<' or nc == ')' or nc == '[':
                return text[ref_start:scan].rstrip(), scan, kind
            elif nc == '.':
                return text[ref_start:scan].rstrip(), scan, kind
            else:
                return text[ref_start:scan].rstrip(), scan, kind

        if ch == '=' and scan + 1 < len(text) and text[scan + 1] == ' ' and scan > ref_start and text[scan - 1] == ' ':
            return text[ref_start:scan].rstrip(), scan, kind

        if ch == '<' or ch == ')':
            ref = text[ref_start:scan].rstrip()
            if ref:
                return ref, scan, kind
            return None, scan, None

        if ch in '[':
            return text[ref_start:scan].rstrip(), scan, kind

        if ch in 'ivxlcdm':
            scan += 1
            continue

        ref = text[ref_start:scan].rstrip()
        if ref:
            return ref, scan, kind
        return None, scan, None

    ref = text[ref_start:scan].rstrip()
    if ref:
        return ref, scan, kind
    return None, scan, None


FIRST_TOKEN_RE = re.compile(r"\s*([a-z]+|[0-9]+)")


def convert_text(text):
    """Convert all LS references in the full text.
    Returns (output_text, arabic_handled, roman_handled,
             other_not_handled, unanalyzed_not_handled)."""
    out = []
    i = 0
    arabic_handled = 0
    roman_handled = 0
    other_not_handled = 0
    unanalyzed_not_handled = 0

    while i < len(text):
        m = re.search(r'<ls>([^<]+)</ls>', text[i:])
        if not m:
            out.append(text[i:])
            break

        out.append(text[i:i + m.start()])
        tag_end = i + m.end()
        source = m.group(1)

        ref, ref_end, kind = extract_ref(text, tag_end)

        if ref is not None:
            out.append(f'<ls>{source} {ref}</ls>')
            i = ref_end
            if kind == 'arabic':
                arabic_handled += 1
            else:
                roman_handled += 1
        else:
            out.append(f'<ls>{source}</ls>')
            i = tag_end
            # Classify unconverted: "other" (has a letter token) or unanalyzed
            after = text[tag_end:]
            fm = FIRST_TOKEN_RE.match(after)
            if fm and not fm.group(1).isdigit():
                other_not_handled += 1
            else:
                unanalyzed_not_handled += 1

    return ''.join(out), arabic_handled, roman_handled, other_not_handled, unanalyzed_not_handled


def main():
    with open(INPUT, encoding='utf-8') as f:
        data = f.read()

    result, arabic_handled, roman_handled, other_not_handled, unanalyzed_not_handled = convert_text(data)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(result)

    total_input = data.count('<ls>')
    total_output = result.count('<ls>')
    total = arabic_handled + roman_handled + other_not_handled + unanalyzed_not_handled
    print(f'Input  <ls> tags : {total_input}')
    print(f'Output <ls> tags : {total_output}')
    print()
    print(f'{"Category":<25} {"Handled":>8} {"Not handled":>12} {"Total":>8}')
    print(f'{"─"*53}')
    print(f'{"Arabic first token":<25} {arabic_handled:>8} {0:>12} {arabic_handled:>8}')
    print(f'{"Roman first token":<25} {roman_handled:>8} {0:>12} {roman_handled:>8}')
    print(f'{"Other (letter token)":<25} {0:>8} {other_not_handled:>12} {other_not_handled:>8}')
    print(f'{"Unanalyzed (no token)":<25} {0:>8} {unanalyzed_not_handled:>12} {unanalyzed_not_handled:>8}')
    print(f'{"─"*53}')
    print(f'{"Total":<25} {arabic_handled + roman_handled:>8} {other_not_handled + unanalyzed_not_handled:>12} {total:>8}')
    print()
    print(f'Written to  {OUTPUT}')


if __name__ == '__main__':
    main()
