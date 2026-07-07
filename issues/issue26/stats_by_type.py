#!/usr/bin/env python3
import re, collections

with open('issues/issue25/temp_ben_2.txt', encoding='utf-8') as f:
    data = f.read()

def normalize_source(s):
    """Reduce a source string to its core abbreviation.
    Removes trailing chapter/verse ref tokens (digits, Roman numerals)."""
    tokens = s.strip().split()
    # Keep removing trailing tokens that look like refs
    while tokens:
        t = tokens[-1]
        # Pure digit, possibly with comma/period suffix
        if re.match(r'^\d+[.,]?$', t):
            tokens.pop()
        # Roman numeral, possibly with period
        elif re.match(r'^[ivxlcdmIVXLCDM]+[.,]?$', t):
            tokens.pop()
        else:
            break
    return ' '.join(tokens) if tokens else s.strip()

plain_counts = collections.Counter()
named_counts = collections.Counter()

# --- Plain tags ---
for m in re.finditer(r'<ls>(.*?)</ls>', data):
    content = m.group(1)
    # Strip <ab> tags
    clean = re.sub(r'</?ab[^>]*>', '', content)
    src = normalize_source(clean)
    if src:
        plain_counts[src] += 1

# --- Named tags ---
for m in re.finditer(r'<ls n="([^"]+)">(.*?)</ls>', data):
    n_val = m.group(1).strip()
    if n_val:
        src = normalize_source(n_val)
        if src:
            named_counts[src] += 1

all_srcs = sorted(
    set(list(plain_counts.keys()) + list(named_counts.keys())),
    key=lambda a: plain_counts.get(a, 0) + named_counts.get(a, 0),
    reverse=True,
)

print(f'{"Source":<38} {"Plain":>6} {"Named":>6} {"Total":>6}')
print('-' * 58)
for s in all_srcs:
    p = plain_counts.get(s, 0)
    n = named_counts.get(s, 0)
    print(f'{s:<38} {p:>6} {n:>6} {p + n:>6}')
