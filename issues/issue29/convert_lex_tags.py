#!/usr/bin/env python3
"""
Convert selected <ab>...</ab> tags to <lex>...</lex> in ben.txt,
and apply minor formatting fixes.

Changes:
  1. <ab>i.e.</ab> → <ab>i. e.</ab>   (insert space)
     <ab>s.v.</ab> → <ab>s. v.</ab>
     <ab>v.r.</ab> → <ab>v. r.</ab>
  2. <ab>Adj.</ab> → <lex>Adj.</lex>
     <ab>adj.</ab> → <lex>adj.</lex>
     <ab>adv.</ab> → <lex>adv.</lex>
     <ab>f.</ab>   → <lex>f.</lex>
     <ab>fem.</ab> → <lex>fem.</lex>
     <ab>ind.</ab> → <lex>ind.</lex>
     <ab>indecl.</ab> → <lex>indecl.</lex>
     <ab>m.</ab>   → <lex>m.</lex>
     <ab>msc.</ab> → <lex>msc.</lex>
     <ab>ntr.</ab> → <lex>ntr.</lex>
  3. <ab>n.</ab>   → <lex>n.</lex>
     EXCEPT where <ab>n.</ab> appears inside <ls>…</ls>
     (there ~23 such cases where n. means 'note', not 'neuter')
  4. <ls>Hit. <ab>Pr.</ab> → <ls>Hit. Pr.
     (remove <ab> wrapper around Pr. following <ls>Hit.)
"""

import re

INPUT  = '/Users/Shared/sanskrit-lexicon/csl-orig/v02/ben/ben.txt'
OUTPUT = '/Users/Shared/other-sanskrit-lexicon-repos/BEN/issues/issue29/temp_ben_1.txt'

with open(INPUT, encoding='utf-8') as f:
    text = f.read()

# ---- 1. Space insertions inside <ab> tags ----
for old, new in [
    ('<ab>i.e.</ab>', '<ab>i. e.</ab>'),
    ('<ab>s.v.</ab>', '<ab>s. v.</ab>'),
    ('<ab>v.r.</ab>', '<ab>v. r.</ab>'),
]:
    text = text.replace(old, new)

# ---- 2. Simple <ab> → <lex> conversions (all except n.) ----
for tag in ['Adj.', 'adj.', 'adv.', 'f.', 'fem.',
            'ind.', 'indecl.', 'm.', 'msc.', 'ntr.']:
    old = f'<ab>{tag}</ab>'
    new = f'<lex>{tag}</lex>'
    text = text.replace(old, new)

# ---- 3. <ab>n.</ab> → <lex>n.</lex> (skip instances inside <ls>) ----
# Collect all <ls>…</ls> span positions first.
LS_RE = re.compile(r'<ls[^>]*>.*?</ls>', re.DOTALL)
ls_spans = [(m.start(), m.end()) for m in LS_RE.finditer(text)]

def inside_ls(pos):
    return any(s < pos < e for s, e in ls_spans)

chunks = []
pos = 0
for m in re.finditer(r'<ab>n\.</ab>', text):
    chunks.append(text[pos:m.start()])
    if inside_ls(m.start()):
        chunks.append(m.group())          # keep as <ab>n.</ab>
    else:
        chunks.append('<lex>n.</lex>')    # convert to <lex>
    pos = m.end()
chunks.append(text[pos:])
text = ''.join(chunks)

# ---- 4. Remove <ab> wrapper around Pr. after <ls>Hit. ----
text = text.replace('<ls>Hit. <ab>Pr.</ab>', '<ls>Hit. Pr.')

# ---- Write output ----
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(text)

# ---- Summary ----
counts = {}
for old_tag, new_tag in [
    ('<ab>Adj.</ab>',  '<lex>Adj.</lex>'),
    ('<ab>adj.</ab>',  '<lex>adj.</lex>'),
    ('<ab>adv.</ab>',  '<lex>adv.</lex>'),
    ('<ab>f.</ab>',    '<lex>f.</lex>'),
    ('<ab>fem.</ab>',  '<lex>fem.</lex>'),
    ('<ab>ind.</ab>',  '<lex>ind.</lex>'),
    ('<ab>indecl.</ab>','<lex>indecl.</lex>'),
    ('<ab>m.</ab>',    '<lex>m.</lex>'),
    ('<ab>msc.</ab>',  '<lex>msc.</lex>'),
    ('<ab>n.</ab>',    '<lex>n.</lex>'),
    ('<ab>ntr.</ab>',  '<lex>ntr.</lex>'),
    ('<ab>i.e.</ab>',  '<ab>i. e.</ab>'),
    ('<ab>s.v.</ab>',  '<ab>s. v.</ab>'),
    ('<ab>v.r.</ab>',  '<ab>v. r.</ab>'),
]:
    with open(OUTPUT, encoding='utf-8') as f:
        out_text = f.read()
    old_count = out_text.count(old_tag)
    new_count = out_text.count(new_tag)
    print(f'{new_count:>6}  {new_tag}')
    if old_count:
        print(f'        (remaining {old_tag}: {old_count})')

hit_pr_count = out_text.count('<ls>Hit. Pr.')
print(f'{hit_pr_count:>6}  <ls>Hit. Pr.')
