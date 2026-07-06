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
ROMAN_ANALYSIS = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "issue16", "roman_analysis.txt"))

# Valid Roman numerals
ROMAN_NUMS = {
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii",
    "ix", "x", "xi", "xii", "xiii", "xiv", "xv", "xvi",
    "xvii", "xviii", "xix", "xx", "xxi", "xxii", "xxiii", "xxiv", "xxv",
    "xxx", "xl", "l", "lx", "lxx", "lxxx", "xc", "c",
    "ci", "cv", "cx", "cl", "cc", "ccc", "cd", "d",
}
ROMAN_SET = set(ROMAN_NUMS)


def build_roman_sources(data):
    """Scan raw data for source abbreviations that use Roman numeral refs."""
    roman_sources = set()
    for m in re.finditer(r'<ls>([^<]+)</ls>', data):
        source = m.group(1)
        pos = m.end()
        scan = pos
        while scan < len(data) and data[scan] in ' \t\r\n':
            scan += 1
        if scan >= len(data):
            continue
        if data[scan:scan+4] == '<ab>':
            end = data.find('</ab>', scan + 4)
            if end >= 0:
                scan = end + 5
        while scan < len(data) and data[scan] in ' \t\r\n':
            scan += 1
        if scan >= len(data):
            continue
        ch = data[scan]
        if ch in 'ivxlcdm':
            rm = re.match(r'^([a-z]+)', data[scan:])
            if rm and rm.group(1) in ROMAN_SET:
                roman_sources.add(source)
    return roman_sources


def skip_ab_tag(text, pos):
    """If text at pos starts with <ab>, return position after </ab>, else pos."""
    if text[pos:pos+4] == '<ab>':
        end = text.find('</ab>', pos + 4)
        if end >= 0:
            return end + 5
    return pos


def has_ref_token(text, pos):
    """Check if text at pos starts with a digit or Roman numeral.
    Returns ('arabic', n) or ('roman', n) or (None, 0)."""
    if pos >= len(text):
        return None, 0
    ch = text[pos]
    if ch.isdigit():
        return 'arabic', 1
    if ch in 'ivxlcdm':
        m = re.match(r'^([a-z]+)', text[pos:])
        if m and m.group(1) in ROMAN_SET:
            return 'roman', len(m.group(1))
    return None, 0


def extract_ref(text, pos, roman_sources, source=None):
    """
    Extract reference text after </ls>, including any intervening <ab> tags.

    Returns (ref_text, end_pos, kind) or (None, None, None).
    """
    uses_roman = source and source in roman_sources
    ref_start = pos  # may be adjusted forward past whitespace
    scan = pos

    # ---- find first reference token, consuming <ab> tags along the way ----
    kind = None
    while True:
        while scan < len(text) and text[scan] in ' \t\r\n':
            scan += 1
        if scan >= len(text):
            return None, None, None

        # Try to consume <ab> tag
        new_scan = skip_ab_tag(text, scan)
        if new_scan > scan:
            scan = new_scan
            continue

        # Check for reference token
        k, _ = has_ref_token(text, scan)
        if k == 'roman' and not uses_roman:
            k = None
        if k is not None:
            kind = k
            break

        return None, None, None

    # ref_start was at `pos`; move it to the first non-whitespace position
    # (before we found the token) so that any <ab> tags are included.
    # Walk back from `scan` to include preceding whitespace + <ab> tags.
    # Actually, simpler: set ref_start to the first non-ws position after </ls>
    # that begins the reference material. That's the position we skipped to
    # initially (before the <ab> scanning). But we need to track it properly.
    # 
    # Let me just recalculate ref_start:
    ref_start = pos
    while ref_start < len(text) and text[ref_start] in ' \t\r\n':
        ref_start += 1
    # ref_start now at first non-ws (could be <ab> or digit/Roman)

    # ---- scan forward through the reference material ----
    while scan < len(text):
        ch = text[scan]

        if ch == '.':
            if scan + 1 < len(text) and text[scan + 1] in ' \t\r\n':
                nxt = scan + 1
                has_newline = False
                while nxt < len(text) and text[nxt] in ' \t\r\n':
                    if text[nxt] == '\n':
                        has_newline = True
                    nxt += 1
                if not has_newline and nxt < len(text):
                    k, _ = has_ref_token(text, nxt)
                    if k == 'roman' and not uses_roman:
                        k = None
                    if k is not None:
                        if not (k == 'arabic' and kind != 'roman'):
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

            # Try to consume <ab> tag after whitespace
            ab_consumed = skip_ab_tag(text, nxt)
            if ab_consumed > nxt:
                # <ab> tag found — skip whitespace + tag, continue
                scan = ab_consumed
                continue

            k, _ = has_ref_token(text, nxt)
            if k == 'roman' and not uses_roman:
                k = None
            if k is not None:
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

        # <ab> tag in the middle of the reference
        new_scan = skip_ab_tag(text, scan)
        if new_scan > scan:
            scan = new_scan
            continue

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
LS_TAG_RE = re.compile(r"<ls>([^<]+)</ls>")


def convert_text(text, roman_sources):
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

        ref, ref_end, kind = extract_ref(text, tag_end, roman_sources, source)

        if ref is not None:
            out.append(f'<ls>{source} {ref}</ls>')
            i = ref_end
            if kind == 'arabic':
                arabic_handled += 1
            else:
                roman_handled += 1
        else:
            # Try "X in Y" cross-reference pattern
            after = text[tag_end:]
            fm = FIRST_TOKEN_RE.match(after)
            if fm and fm.group(1) == 'in':
                word_end = tag_end + len(fm.group(0))
                sep_period = ''
                scan_pos = word_end
                if scan_pos < len(text) and text[scan_pos] == '.':
                    sep_period = '.'
                    scan_pos += 1
                while scan_pos < len(text) and text[scan_pos] in ' \t\r\n':
                    scan_pos += 1
                if scan_pos < len(text) and text[scan_pos:scan_pos+4] == '<ls>':
                    inner_m = re.match(r'<ls>([^<]+)</ls>', text[scan_pos:])
                    if inner_m:
                        y_source = inner_m.group(1)
                        inner_tag_end = scan_pos + inner_m.end()
                        ref2, ref_end2, kind2 = extract_ref(text, inner_tag_end, roman_sources, y_source)
                        if ref2 is not None:
                            out.append(f'<ls>{source} in{sep_period} {y_source} {ref2}</ls>')
                            i = ref_end2
                            if kind2 == 'arabic':
                                arabic_handled += 1
                            else:
                                roman_handled += 1
                        else:
                            out.append(f'<ls>{source}</ls>')
                            i = tag_end
                            other_not_handled += 1
                        continue

            out.append(f'<ls>{source}</ls>')
            i = tag_end
            # Classify unconverted: "other" (has a letter token) or unanalyzed
            if fm and not fm.group(1).isdigit():
                other_not_handled += 1
            else:
                unanalyzed_not_handled += 1

    return ''.join(out), arabic_handled, roman_handled, other_not_handled, unanalyzed_not_handled


def main():
    with open(INPUT, encoding='utf-8') as f:
        data = f.read()

    roman_sources = build_roman_sources(data)

    result, arabic_handled, roman_handled, other_not_handled, unanalyzed_not_handled = convert_text(data, roman_sources)

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
