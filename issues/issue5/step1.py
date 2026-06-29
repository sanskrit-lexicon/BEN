#!/usr/bin/env python3
"""step1.py - Apply mechanical transformations to bring CDSL closer to AB.

Transformations:
  T_join_pct: Merge hyphenated {%...%} blocks across line break (-%}\n{% → '')
  T0: Join hyphenated line breaks globally (-\n → '')
  T7: Collapse newlines within entries (\n → ' ')
  T5: Normalize -- separator spacing (-- + → --)
  T4: Unwrap {@ @} around -- <ab>Comp.</ab>
  T4b: Unwrap split {@ @} blocks ({@ --@} {@<ab>Comp.</ab>@} → --<ab>Comp.</ab>)
  T_plus_spacing: Normalize spacing around + signs (a+b → a + b)
  T_roman_comma: Change comma to period after roman numerals before digits (i, 1 → i. 1)
  T2: Move punctuation (, . ; :) from inside {%...%} to outside
  T3: Move † (dagger) from inside {#...#} to before it
  T8: Split Comp sub-entries onto separate lines with ¦
  T_section_nl: Put ' --' section separators on their own line ( -- → \n --)
  T_with_nl: Put ' -With ' on its own line with double dash ( -With → \n --With)
  T_pipe_missing: Add missing '¦' to lines starting with '{%' or ' {%' (^{% → ¦ {%)
  T9: Remove trailing space before <LEND> or newline+¦
  T_merge_m: Merge %} + {%m%}[.] into previous block ({%x%} + {%m%}. → {%xm%})
  T10: Merge adjacent {%...%} blocks (%} {% → '')
  T6: Ensure blank line after each <LEND>
  #63-1: Change single-dash <ab> to double-dash
  #63-2: Put {% block after digit+period on own line with ¦
  #63-3: Tag 'etc.' with <ab>...</ab>
  #63-4: Tag 'VP.' with <ls>...</ls>
  #63-5: Move + from inside {%...+%} to before {%
  #63-6: Tag 'Man, N' with <ls>Man.</ls> N
  #63-7: Tag 'Vedāntas.' with <ls>...</ls>
  #63-8: Split {%x = y%} into {%x%} + {%y%}
  #63-9: Move * from inside {%*...%} to before {%
  #63-10: Join Sanskrit blocks by removing -#} {#

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


def t_join_pct(text):
    """T_join_pct: Merge hyphenated {%...%} blocks across line break.

    Handles the case where a hyphenated line break falls exactly
    at the boundary between two {%...%} blocks.
    {%abc-%}\n{%def%} → {%abcdef%}
    """
    return re.sub(r'-%}\n{%', '', text)


def t0_join_hyphens(text):
    """T0: Join hyphenated line breaks globally before any other transform."""
    return re.sub(r'-\n', '', text)


def t7_collapse_newlines(text):
    """T7: Collapse newlines within entries.

    Within each entry (between <L> and <LEND>):
        '\n' → ' ' (replace other newlines with space)
    Preserves the <L> header line on its own line and
    keeps <LEND> on its own line.
    """
    parts = re.split(r'(<LEND>\n?)', text)
    for i, part in enumerate(parts):
        if part.startswith('<L>') and not part.startswith('<LEND'):
            lines = part.split('\n')
            header = lines[0]
            body = '\n'.join(lines[1:])
            body = re.sub(r'\n', ' ', body)
            body = re.sub(r' +', ' ', body)
            parts[i] = header + '\n' + body + '\n'
    return ''.join(parts)


def t5_dash_space(text):
    """T5: Remove space(s) after -- section separators.

    Handles single space (-- text) and double space ({@ --  @}).
    """
    return re.sub(r'-- +', '--', text)


def t4_comp_unwrap(text):
    """T4: Remove {@ @} wrapping around -- <ab>Comp.</ab>."""
    return re.sub(r'\s*\{@\s*--\s*<ab>Comp\.</ab>@\}', ' --<ab>Comp.</ab>', text)


def t4b_comp_unwrap_split(text):
    """T4b: Handle {@ --@} {@<ab>Comp.</ab>@} pattern (split across two {@ @} blocks)."""
    return re.sub(r'\{@\s*--@\}\s*\{@<ab>Comp\.</ab>@\}', ' --<ab>Comp.</ab>', text)


def t_plus_spacing(text):
    """Normalize spacing around + signs: ensures surrounding spaces."""
    text = re.sub(r'([^ ])[+]', r'\1 +', text)
    text = re.sub(r'[+]([^ ])', r'+ \1', text)
    return text


def t_roman_comma_to_period(text):
    """Change comma to period after roman numerals before digits (e.g. 'i, 1' → 'i. 1')."""
    return re.sub(r', ([ivx]+), ([0-9])', r', \1. \2', text)


def t_merge_m(text):
    """Merge %} + {%m%}[.] into the previous block, removing the +."""
    return re.sub(r'%} \+ \{%m%\}\.?', 'm%}', text)


def t2_punctuation_outside(text):
    """T2: Move trailing punctuation from inside {%...%} to outside.

    Handles single punctuation ({%a,%} -> {%a%},) and multiple
    consecutive punctuation ({%a,,%} -> {%a%},,).
    """
    text = re.sub(r'\{%([^}]*?)([,.;:]+)%\}', r'{%\1%}\2', text)
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


def t_section_nl(text):
    """T_section_nl: Put ' --' section separators on their own line.
    Skip '{@...@}' blocks (e.g. ' -- {@2.@}') — they should stay inline.
    """
    return re.sub(r' --(?!\s*\{@)', '\n --', text)


def t_with_nl(text):
    """Normalize ' -With ' to '\n --With ' (put -With sections on own line with double dash)."""
    return re.sub(r' -With ', '\n --With ', text)


def t_pipe_missing(text):
    """Prepend '¦' to lines starting with '{%' (missing pipe separator)."""
    text = re.sub(r'^ \{', '¦ {', text, flags=re.MULTILINE)
    text = re.sub(r'^\{', '¦ {', text, flags=re.MULTILINE)
    # Undo incorrect additions to {# lines (entry body starts with {#...})
    text = re.sub(r'^¦ \{#', '{#', text, flags=re.MULTILINE)
    text = re.sub(r'^¦  \{#', '{#', text, flags=re.MULTILINE)
    return text


def t9_trail_space(text):
    """T9: Remove trailing whitespace from all lines, especially before <LEND> and ¦."""
    text = re.sub(r' +\n<LEND>', '\n<LEND>', text)
    text = re.sub(r' +\n¦', '\n¦', text)
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
    return text


def t10_merge_pct_blocks(text):
    """T10: Merge adjacent {%...%} blocks by removing '%} {%' separator."""
    return re.sub(r'%} {%', '', text)


def t6_blank_lines(text):
    """T6: Ensure exactly one blank line after each <LEND>."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'<LEND>\n(?!\n)', '<LEND>\n\n', text)
    return text


# ── New transformations (issue #63) ──────────────────────────────────────────


def t_dash_ab(text):
    """Change single-dash + <ab> to double-dash (matching AB)."""
    return re.sub(r' -<ab>', ' --<ab>', text)


def t_num_pipe_pct(text):
    """Put {% block after digit+period on its own line with ¦."""
    return re.sub(r'(\d\.) \{%', r'\1\n¦ {%', text)


def t_etc_tag(text):
    """Tag 'etc.' with <ab>...</ab>."""
    return re.sub(r' etc\.', ' <ab>etc.</ab>', text)


def t_vp_tag(text):
    """Tag 'VP.' with <ls>...</ls>."""
    return re.sub(r' VP\. ', ' <ls>VP.</ls> ', text)


def t_plus_out(text):
    """Move + from inside {%...+%} to before {%."""
    return re.sub(r'\{% \+ ', '+ {%', text)


def t_man_tag(text):
    """Tag 'Man,' reference with <ls>...</ls>."""
    return re.sub(r' Man, (\d)', ' <ls>Man.</ls> \\1', text)


def t_vedantas_tag(text):
    """Tag 'Vedāntas.' with <ls>...</ls>."""
    return re.sub(r'Vedāntas\. ', '<ls>Vedāntas.</ls> ', text)


def t_split_eq(text):
    """Split {%x = y%} into {%x%} + {%y%}."""
    return re.sub(r'\{%([^=]+) =([^%]+)%\}', r'\1%} + {%\2%}', text)


def t_asterisk_out(text):
    """Move * from inside {%*...%} to before {%."""
    return re.sub(r'\{%\*', '*{%', text)


def t_join_sanskrit(text):
    """Join Sanskrit blocks by removing -#} {# boundary."""
    return re.sub(r'-#} *{#', '', text)


def main():
    os.makedirs(DERIV_DIR, exist_ok=True)

    with open(CDSL_FILE, 'r') as f:
        cdsl = f.read()

    stats = {}

    # T_join_pct: merge hyphenated {%...%} blocks across line break
    cjp = len(re.findall(r'-%}\n{%', cdsl))
    cdsl = t_join_pct(cdsl)
    stats['T_join_pct: merged hyphenated {% blocks'] = cjp

    # T0: join hyphenated line breaks globally (before any other transform)
    c0 = len(re.findall(r'-\n[a-z]', cdsl))
    cdsl = t0_join_hyphens(cdsl)
    stats['T0: hyphenated words joined'] = c0

    # T7: collapse newlines within entries
    c7 = len(re.findall(r'(?<!<LEND>)\n(?!<L>)', cdsl))
    cdsl = t7_collapse_newlines(cdsl)
    stats['T7: newlines collapsed'] = c7

    # T5: normalize -- spacing
    c5 = len(re.findall(r'-- +', cdsl))
    cdsl = t5_dash_space(cdsl)
    stats['T5: -- spacing normalized'] = c5

    # T4: unwrap Comp blocks
    c4 = len(re.findall(r'\{@\s*--\s*<ab>Comp\.</ab>@\}', cdsl))
    cdsl = t4_comp_unwrap(cdsl)
    stats['T4: Comp blocks unwrapped'] = c4

    # T4b: unwrap split Comp blocks ({@ --@} {@<ab>Comp.</ab>@})
    c4b = len(re.findall(r'\{@\s*--@\}\s*\{@<ab>Comp\.</ab>@\}', cdsl))
    cdsl = t4b_comp_unwrap_split(cdsl)
    stats['T4b: split Comp blocks unwrapped'] = c4b

    # T_plus_spacing: normalize spacing around + signs
    c_plus_before = len(re.findall(r'[^ ]\+', cdsl)) + len(re.findall(r'\+[^ ]', cdsl))
    cdsl = t_plus_spacing(cdsl)
    c_plus_after = len(re.findall(r'[^ ]\+', cdsl)) + len(re.findall(r'\+[^ ]', cdsl))
    stats['T_plus_spacing: + spacing'] = c_plus_before - c_plus_after

    # T2: move punctuation outside {%...%}
    c2 = len(re.findall(r'\{%[^}]*?[,.;:]+%\}', cdsl))
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

    # T_section_nl: put ' --' on its own line
    c_sn = len(re.findall(r' --', cdsl))
    cdsl = t_section_nl(cdsl)
    stats['T_section_nl: -- on own line'] = c_sn

    # T_with_nl: normalize ' -With ' to '\n --With '
    c_wn = len(re.findall(r' -With ', cdsl))
    cdsl = t_with_nl(cdsl)
    stats['T_with_nl: -With to --With'] = c_wn

    # T_pipe_missing: prepend '¦' to lines starting with '{%' or ' {%'
    c_pm = len(re.findall(r'^ \{', cdsl, flags=re.MULTILINE)) + len(re.findall(r'^\{', cdsl, flags=re.MULTILINE)) - len(re.findall(r'^\{#', cdsl, flags=re.MULTILINE))
    cdsl = t_pipe_missing(cdsl)
    stats['T_pipe_missing: added missing ¦'] = c_pm

    # T9: remove trailing whitespace from all lines (before <LEND>, \n¦, and general)
    c9a = len(re.findall(r' +\n<LEND>', cdsl))
    c9b = len(re.findall(r' +\n¦', cdsl))
    c9c = len(re.findall(r'[ \t]+$', cdsl, flags=re.MULTILINE))
    cdsl = t9_trail_space(cdsl)
    stats['T9: trailing space before LEND'] = c9a
    stats['T9: trailing space before ¦'] = c9b
    stats['T9: trailing whitespace on lines'] = c9c

    # T_merge_m: merge %} + {%m%}[.] into previous block
    c_m = len(re.findall(r'%} \+ \{%m%\}.?', cdsl))
    cdsl = t_merge_m(cdsl)
    stats['T_merge_m: merged m into prev block'] = c_m

    # T_roman_comma_to_period: unify roman numeral notation (', i, 1' → ', i. 1')
    c_roman = len(re.findall(r', ([ivx]+), ([0-9])', cdsl))
    cdsl = t_roman_comma_to_period(cdsl)
    stats['T_roman_comma: roman comma to period'] = c_roman

    # T10: merge adjacent {%...%} blocks
    c10 = len(re.findall(r'%} {%', cdsl))
    cdsl = t10_merge_pct_blocks(cdsl)
    stats['T10: merged adjacent {% blocks'] = c10

    # T6: ensure blank lines after LEND
    c6 = len(re.findall(r'<LEND>\n(?!\n)', cdsl))
    cdsl = t6_blank_lines(cdsl)
    stats['T6: blank lines ensured'] = c6

    # ── New transforms (issue #63) ─────────────────────────────────────
    # 1: change single-dash <ab> to double-dash (matching AB)
    c_dab = len(re.findall(r' -<ab>', cdsl))
    cdsl = t_dash_ab(cdsl)
    stats['1: -<ab> → --<ab>'] = c_dab

    # 2: put {% block after digit+period on own line
    c_np = len(re.findall(r'\d\. \{%', cdsl))
    cdsl = t_num_pipe_pct(cdsl)
    stats['2: \\d. {% → own line with ¦'] = c_np

    # 3: tag 'etc.' with <ab>...</ab>
    c_etc = len(re.findall(r' etc\.', cdsl))
    cdsl = t_etc_tag(cdsl)
    stats['3: etc. tagged'] = c_etc

    # 4: tag 'VP.' with <ls>...</ls>
    c_vp = len(re.findall(r' VP\. ', cdsl))
    cdsl = t_vp_tag(cdsl)
    stats['4: VP. tagged'] = c_vp

    # 5: move + out of {%...+%} to before {%
    c_po = len(re.findall(r'\{% \+ ', cdsl))
    cdsl = t_plus_out(cdsl)
    stats['5: + moved out of {%...%}'] = c_po

    # 6: tag 'Man,' reference with <ls>...</ls>
    c_man = len(re.findall(r' Man, \d', cdsl))
    cdsl = t_man_tag(cdsl)
    stats['6: Man, tagged'] = c_man

    # 7: tag 'Vedāntas.' with <ls>...</ls>
    c_ved = len(re.findall(r'Vedāntas\. ', cdsl))
    cdsl = t_vedantas_tag(cdsl)
    stats['7: Vedāntas. tagged'] = c_ved

    # 8: split {%x = y%} into {%x%} + {%y%}
    c_eq = len(re.findall(r'\{%[^=]+ =[^%]+%\}', cdsl))
    cdsl = t_split_eq(cdsl)
    stats['8: {%...=...%} split'] = c_eq

    # 9: move * out of {%*...%} to before {%
    c_ast = len(re.findall(r'\{%\*', cdsl))
    cdsl = t_asterisk_out(cdsl)
    stats['9: * moved out of {%...%}'] = c_ast

    # 10: join Sanskrit blocks by removing -#} {#
    c_js = len(re.findall(r'-#} *{#', cdsl))
    cdsl = t_join_sanskrit(cdsl)
    stats['10: -#} {# removed'] = c_js

    # ── New transforms (user 2025-12-20) ──────────────────────────────
    # 11-12: standardize Cf. and Caus. sections (skip if already on own line)
    c11 = len(re.findall(r'-*<ab>Cf\.</ab>', cdsl))
    cdsl = re.sub(
        r'(\n --)?-*<ab>Cf\.</ab>',
        lambda m: '\n --<ab>Cf.</ab>' if m.group(1) is None else m.group(0),
        cdsl,
    )
    stats['11: standardize <ab>Cf.</ab>'] = c11

    c12 = len(re.findall(r'-*<ab>Caus\.</ab>', cdsl))
    cdsl = re.sub(
        r'(\n --)?-*<ab>Caus\.</ab>',
        lambda m: '\n --<ab>Caus.</ab>' if m.group(1) is None else m.group(0),
        cdsl,
    )
    stats['12: standardize <ab>Caus.</ab>'] = c12

    # 13: put † roman.page on its own line (skip if already on own line)
    c13 = len(re.findall(r'† ([ivx]+)\. (\d)', cdsl))
    cdsl = re.sub(
        r'(\n --)?† ([ivx]+)\. (\d)',
        lambda m: '\n --† ' + m.group(2) + '. ' + m.group(3) if m.group(1) is None else m.group(0),
        cdsl,
    )
    stats['13: † roman.page on own line'] = c13

    # Write CDSL output
    cdsl_out = os.path.join(DERIV_DIR, 'temp_cdsl_ben1.txt')
    with open(cdsl_out, 'w') as f:
        f.write(cdsl)

    # Read and normalize AB output
    with open(AB_FILE, 'r') as f:
        ab = f.read()

    ab_orig = ab  # snapshot for stats

    # Normalize AB: remove leading space before ¦ at line start
    ab = re.sub(r'^ [¦]', '¦', ab, flags=re.MULTILINE)
    ab_norm_pipe = ab_orig.count(' ¦') - ab.count(' ¦')
    # Normalize AB: fix Kriṣṇa → Kṛṣṇa (4 instances in AB, 0 in CDSL)
    ab_kri_count = ab.count('Kriṣ')
    ab = ab.replace('Kriṣ', 'Kṛṣ')
    # Normalize AB: use ˚ (ring above) instead of ° (degree sign) to match CDSL
    ab_deg_count = ab.count('°')
    ab = ab.replace('°', '˚')
    ab_out = os.path.join(DERIV_DIR, 'temp_ab_ben1.txt')
    with open(ab_out, 'w') as f:
        f.write(ab)

    print("=== step1.py completed ===")
    print(f"  CDSL output: {cdsl_out}")
    print(f"  AB   output: {ab_out}")
    print()
    print("CDSL transformations:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print()
    print(f"AB normalizations:")
    print(f"  Pipe at line start:  {ab_norm_pipe}")
    print(f"  Kriṣ→Kṛṣ:            {ab_kri_count}")
    print(f"  °→˚:                 {ab_deg_count}")
    print()
    cdsl_size = os.path.getsize(CDSL_FILE)
    mod_size = os.path.getsize(cdsl_out)
    ab_size = os.path.getsize(AB_FILE)
    print(f"  Original CDSL: {cdsl_size:>8} bytes ({cdsl_size // 1000} KB)")
    print(f"  Modified CDSL: {mod_size:>8} bytes ({mod_size // 1000} KB)")
    print(f"  Original AB:   {ab_size:>8} bytes ({ab_size // 1000} KB)")
    print()
    print("To measure diff reduction:")
    print("  git diff --word-diff-regex=. --no-index derivatives/temp_cdsl_ben1.txt derivatives/temp_ab_ben1.txt | wc -c")


if __name__ == '__main__':
    main()
