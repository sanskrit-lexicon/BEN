#!/usr/bin/env python3
"""
Move [Page...] references that sit between digit blocks in <ls> citations
to after the terminator.

Before:  <ls>MBh.</ls> 12, [Page0139-a + 38] 12724;
After:   <ls>MBh.</ls> 12, 12724; [Page0139-a + 38]
"""

import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_ben_1.txt")
OUTPUT = os.path.join(SCRIPT_DIR, "temp_ben_2.txt")

# Pattern matches <ls>SRC</ls> followed by:
#   \1 = the <ls> tag plus trailing whitespace
#   \2 = one or more digit blocks (prefix before [Page])
#   separator = comma/space between digit blocks and [Page]
#   \3 = the bracket reference (typically [PageNNNN-a + NN])
#   separator = comma/space between [Page] and following digits
#   \4 = one or more digit blocks (suffix after [Page])
#   \5 = the terminator (. or ;)
PATTERN = re.compile(
    r"(<ls>[^<]+</ls>\s*)"
    r"(\d+(?:[\s,]*\d+)*)"
    r"(?:[\s,]*)"
    r"(\[[^\]]*\])"
    r"(?:[\s,]*)"
    r"(\d+(?:[\s,]*\d+)*)"
    r"([.;])"
)

FIX_RE = re.compile(
    r"(<ls>[^<]+</ls>\s*)"
    r"(\d+(?:[\s,]*\d+)*)"
    r"(?:[\s,]*)"
    r"(\[[^\]]*\])"
    r"(?:[\s,]*)"
    r"(\d+(?:[\s,]*\d+)*)"
    r"([.;])"
)

def fix(m):
    """Rejoin as: tag  prefix_digits, suffix_digits terminator  [Page...]"""
    return f"{m.group(1)}{m.group(2)}, {m.group(4)}{m.group(5)} {m.group(3)}"

def main():
    with open(INPUT, encoding="utf-8") as f:
        text = f.read()

    result, count = FIX_RE.subn(fix, text)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Processed {INPUT}")
    print(f"Fixed {count} references.")
    print(f"Written to {OUTPUT}")

if __name__ == "__main__":
    main()
