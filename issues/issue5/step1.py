#!/usr/bin/env python3
"""step1.py - Apply mechanical transformations to bring CDSL closer to AB.

Transformations:
  T7: Collapse newlines within entries (-\n → '', \n → ' ')
  T5: Normalize -- separator spacing (-- + → --)
  T4: Unwrap {@ @} around -- <ab>Comp.</ab>
  T2: Move punctuation (, . ;) from inside {%...%} to outside
  T3: Move † (dagger) from inside {#...#} to before it
  T8: Split Comp sub-entries onto separate lines with ¦
  T9: Remove trailing space before <LEND>
  T10: Merge adjacent {%...%} blocks (%} {% → '')
  T6: Ensure blank line after each <LEND>

Output:
  derivatives/temp_cdsl_ben1.txt  — CDSL with corrections applied
  derivatives/temp_ab_ben1.txt    — AB source (copied as-is for comparison)

Diff measurement:
  git diff --word-diff-regex=. --no-index derivatives/temp_cdsl_ben1.txt derivatives/temp_ab_ben1.txt | wc -c
"""

import re
import os

CDSL_FILE = "temp_base_ben.txt"
AB_FILE = "ben_Main_L2.txt"
DERIV_DIR = "derivatives"


def t7_collapse_newlines(text):
    """T7: Collapse newlines within entries.

    Within each entry (between <L> and <LEND>):
      - '-\n' → ''  (join hyphenated words)
      -  '\n' → ' ' (replace other newlines with space)
    Preserves the <L> header line on its own line and
    keeps <LEND> on its own line.
    """
    parts = re.split(r'(<LEND>\n?)', text)
    for i, part in enumerate(parts):
        if part.startswith('<L>') and not part.startswith('<LEND'):
            lines = part.split('\n')
            header = lines[0]
            body = '\n'.join(lines[1:])
            body = re.sub(r'-\n', '', body)
            body = re.sub(r'\n', ' ', body)
            body = re.sub(r' +', ' ', body)
            parts[i] = header + '\n' + body
    return ''.join(parts)


def t5_dash_space(text):
    """T5: Remove space(s) after -- section separators.

    Handles single space (-- text) and double space ({@ --  @}).
    """
    return re.sub(r'-- +', '--', text)


def t4_comp_unwrap(text):
    """T4: Remove {@ @} wrapping around -- <ab>Comp.</ab>."""
    return re.sub(r'\s*\{@\s*--\s*<ab>Comp\.</ab>@\}', ' --<ab>Comp.</ab>', text)


def t2_punctuation_outside(text):
    """T2: Move trailing punctuation from inside {%...%} to outside.

    Handles single punctuation ({%a,%} -> {%a%},) and multiple
    consecutive punctuation ({%a,,%} -> {%a%},,).
    """
    text = re.sub(r'\{%([^}]*?)([,.;]+)%\}', r'{%\1%}\2', text)
    return text


def t3_dagger_outside(text):
    """T3: Move † from inside {#...#} to before it."""
    return re.sub(r'\{#†\s*', '† {#', text)


def t8_comp_subentries(text):
    """T8: Split Comp sub-entries onto separate lines with '¦' prefix.

    After '<ab>Comp.</ab>', each {%...%} sub-entry heading that starts
    with a capital letter gets its own line: \n¦ {%Heading%}.
    """
    parts = re.split(r'(<LEND>\n?)', text)
    for i, part in enumerate(parts):
        if part.startswith('<L>') and not part.startswith('<LEND'):
            comp_idx = part.find('<ab>Comp.</ab>')
            if comp_idx != -1:
                before = part[:comp_idx + len('<ab>Comp.</ab>')]
                after = part[comp_idx + len('<ab>Comp.</ab>'):]
                after = re.sub(r'\{%([A-Z])', r'\n¦ {%\1', after)
                # Ensure leading newline before first sub-entry
                after = re.sub(r'^ ', '', after)
                parts[i] = before + after
    return ''.join(parts)


def t9_trail_space(text):
    """T9: Remove trailing space(s) before <LEND>."""
    return re.sub(r' +<LEND>', '<LEND>', text)


def t10_merge_pct_blocks(text):
    """T10: Merge adjacent {%...%} blocks by removing '%} {%' separator."""
    return re.sub(r'%} {%', '', text)


def t6_blank_lines(text):
    """T6: Ensure exactly one blank line after each <LEND>."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'<LEND>\n(?!\n)', '<LEND>\n\n', text)
    return text


def main():
    os.makedirs(DERIV_DIR, exist_ok=True)

    with open(CDSL_FILE, 'r') as f:
        cdsl = f.read()

    stats = {}

    # T7: collapse newlines within entries
    c7a = len(re.findall(r'-\n[a-z]', cdsl))
    c7b = len(re.findall(r'(?<!<LEND>)\n(?!<L>)', cdsl))
    cdsl = t7_collapse_newlines(cdsl)
    stats['T7: hyphenated words joined'] = c7a
    stats['T7: newlines collapsed'] = c7b

    # T5: normalize -- spacing
    c5 = len(re.findall(r'-- +', cdsl))
    cdsl = t5_dash_space(cdsl)
    stats['T5: -- spacing normalized'] = c5

    # T4: unwrap Comp blocks
    c4 = len(re.findall(r'\{@\s*--\s*<ab>Comp\.</ab>@\}', cdsl))
    cdsl = t4_comp_unwrap(cdsl)
    stats['T4: Comp blocks unwrapped'] = c4

    # T2: move punctuation outside {%...%}
    c2 = len(re.findall(r'\{%[^}]*?[,.;]+%\}', cdsl))
    cdsl = t2_punctuation_outside(cdsl)
    stats['T2: punctuation moved out'] = c2

    # T3: move dagger
    c3 = len(re.findall(r'\{#†', cdsl))
    cdsl = t3_dagger_outside(cdsl)
    stats['T3: daggers moved out'] = c3

    # T8: split Comp sub-entries
    c8 = len(re.findall(r'<ab>Comp\.</ab>[^<]*?\{%.*?[A-Z]', cdsl))
    cdsl = t8_comp_subentries(cdsl)
    stats['T8: Comp sub-entries split'] = c8

    # T9: remove trailing space before <LEND>
    c9 = len(re.findall(r' +<LEND>', cdsl))
    cdsl = t9_trail_space(cdsl)
    stats['T9: trailing space before LEND'] = c9

    # T10: merge adjacent {%...%} blocks
    c10 = len(re.findall(r'%} {%', cdsl))
    cdsl = t10_merge_pct_blocks(cdsl)
    stats['T10: merged adjacent {% blocks'] = c10

    # T6: ensure blank lines after LEND
    c6 = len(re.findall(r'<LEND>\n(?!\n)', cdsl))
    cdsl = t6_blank_lines(cdsl)
    stats['T6: blank lines ensured'] = c6

    # Write CDSL output
    cdsl_out = os.path.join(DERIV_DIR, 'temp_cdsl_ben1.txt')
    with open(cdsl_out, 'w') as f:
        f.write(cdsl)

    # Copy AB output (as-is for comparison)
    with open(AB_FILE, 'r') as f:
        ab = f.read()
    ab_out = os.path.join(DERIV_DIR, 'temp_ab_ben1.txt')
    with open(ab_out, 'w') as f:
        f.write(ab)

    print("=== step1.py completed ===")
    print(f"  CDSL output: {cdsl_out}")
    print(f"  AB   output: {ab_out}")
    print()
    print("Transformations applied:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print()
    cdsl_size = os.path.getsize(CDSL_FILE)
    mod_size = os.path.getsize(cdsl_out)
    ab_size = os.path.getsize(AB_FILE)
    print(f"  Original CDSL: {cdsl_size:>8} bytes ({cdsl_size // 1000} KB)")
    print(f"  Modified CDSL: {mod_size:>8} bytes ({mod_size // 1000} KB)")
    print(f"  AB version:    {ab_size:>8} bytes ({ab_size // 1000} KB)")
    print()
    print("To measure diff reduction:")
    print("  git diff --word-diff-regex=. --no-index derivatives/temp_cdsl_ben1.txt derivatives/temp_ab_ben1.txt | wc -c")


if __name__ == '__main__':
    main()
