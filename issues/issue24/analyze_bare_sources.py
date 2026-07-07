import re, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_be2edf5.txt")

print(f"Reading {INPUT} ...", flush=True)
with open(INPUT, encoding='utf-8') as f:
    data = f.read()

ROMAN_NUMS = {'i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii','xiv','xv','xvi','xvii','xviii','xix','xx','xxi','xxii','xxiii','xxiv','xxv','xxx','xl','l','lx','lxx','lxxx','xc','c','ci','cv','cx','cl','cc','ccc','cd','d'}

def is_ref_start(tok):
    clean = tok.rstrip(',.;:')
    return clean.isdigit() or clean.lower() in ROMAN_NUMS

def extract_source(content):
    content = re.sub(r'<[^>]+>', '', content)
    tokens = content.split()
    parts = []
    for t in tokens:
        if is_ref_start(t):
            break
        parts.append(t)
    return ' '.join(parts) if parts else content

# Build known sources
print("Building known sources ...", flush=True)
sources = set()
for m in re.finditer(r'<ls[^>]*>([^<]+)</ls>', data):
    s = extract_source(m.group(1))
    if s:
        sources.add(s)

sources_sorted = sorted(sources, key=len, reverse=True)
print(f"Known sources: {len(sources_sorted)}", flush=True)

# Build a single combined regex (longest-first alternation)
# Escape each source for regex safety
escaped = [re.escape(s) for s in sources_sorted]
# Only use first 50 sources that commonly have digit refs to keep regex fast
# Actually, try all, but sort by length desc
combined_pat = re.compile(
    r'\b(?:' + '|'.join(escaped) + r')\s+(\d{1,6}(?:,\s*\d{1,6})*)'
)
print(f"Combined regex compiled ({len(escaped)} alternatives)", flush=True)

# Scan each line
lines = data.split('\n')
genuine = []
total = len(lines)

# Also build a set of the source strings for quick lookup of which source matched
source_set = set(sources_sorted)

for lineno, line in enumerate(lines, 1):
    if lineno % 5000 == 0:
        print(f"  line {lineno}/{total}", flush=True)

    ls_spans = [(m.start(), m.end()) for m in re.finditer(r'<ls\b[^>]*>.*?</ls>', line)]
    if not ls_spans:
        # No <ls> tags — check whole line
        for m in combined_pat.finditer(line):
            ctx = line[max(0,m.start()-50):min(len(line),m.end()+50)].strip()
            genuine.append((lineno, m.group(), ctx))
    else:
        for m in combined_pat.finditer(line):
            start = m.start()
            in_ls = any(ls_start <= start < ls_end for ls_start, ls_end in ls_spans)
            if not in_ls:
                ctx = line[max(0,start-50):min(len(line),m.end()+50)].strip()
                genuine.append((lineno, m.group(), ctx))

print(f"\nTotal genuine bare source+ref: {len(genuine)}", flush=True)
# Deduplicate by line+match
seen = set()
for ln, match, ctx in genuine:
    key = (ln, match)
    if key not in seen:
        seen.add(key)
        print(f"  L{ln:>5}: \"{match}\"  |  ...{ctx}...")
