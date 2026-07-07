#!/usr/bin/env python3
"""
Convert '</ls> <ls>Gorr.</ls>' to ' <ab>Gorr.</ab></ls>' in BEN text.

Gorr. (Gorresio's edition of Rāmāyaṇa) is not an independent source
citation but a qualifier on the preceding <ls> ref, so it should be
marked as <ab> (annotation) inside the preceding <ls> tag.
"""

import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "temp_0dd4ede.txt")
OUTPUT = os.path.join(SCRIPT_DIR, "temp_ben_1.txt")

PATTERN = '</ls> <ls>Gorr.</ls>'
REPLACEMENT = ' <ab>Gorr.</ab></ls>'


def process(text):
    return text.replace(PATTERN, REPLACEMENT)


def main():
    with open(INPUT, encoding='utf-8') as f:
        data = f.read()

    count = data.count(PATTERN)
    print(f"Matches: {count}")

    result = process(data)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(result)

    after = result.count('<ab>Gorr.</ab>')
    remaining = result.count('</ls> <ls>Gorr.</ls>')
    print(f"<ab>Gorr.</ab> tags created: {after}")
    print(f"Remaining unconverted: {remaining}")
    print(f"Input  <ls> tags: {data.count('<ls>')}")
    print(f"Output <ls> tags: {result.count('<ls>')}")
    print(f"Written to: {OUTPUT}")


if __name__ == '__main__':
    main()
