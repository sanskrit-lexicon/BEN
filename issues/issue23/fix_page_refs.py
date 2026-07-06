#!/usr/bin/env python3
"""Fix <ls>SOURCE</ls> p. N -> <ls>SOURCE p. N</ls> page references."""

import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_ben_1.txt")
OUTPUT = os.path.join(SCRIPT_DIR, "temp_ben_1.txt")

P_REF_RE = re.compile(r'\s*p\.\s+(\d+(?:\s*,\s*\d+)*)')

with open(INPUT, encoding='utf-8') as f:
    text = f.read()

out = []
i = 0
fixed = 0

while i < len(text):
    m = re.search(r'<ls>([^<]+)</ls>', text[i:])
    if not m:
        out.append(text[i:])
        break
    out.append(text[i:i + m.start()])
    tag_end = i + m.end()
    source = m.group(1)
    after = text[tag_end:]
    pm = P_REF_RE.match(after)
    if pm:
        out.append('<ls>%s p. %s</ls>' % (source, pm.group(1)))
        i = tag_end + len(pm.group(0))
        fixed += 1
        continue
    out.append('<ls>%s</ls>' % source)
    i = tag_end

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(''.join(out))

print('Fixed: %d page references' % fixed)
