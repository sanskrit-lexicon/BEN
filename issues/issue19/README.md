# issue19: Convert BEN `<ls>` References to PWG-Style Format

Converts BEN's `<ls>` markup from the CDSL standard style
(`<ls>MBh.</ls> 14, 34.`) to the PWG style
(`<ls>MBh. 14, 34</ls>.`), where the reference numbers are moved
*inside* the `<ls>` tag.

## Motivation

PWG already uses the inline style.  Making BEN consistent with PWG
allows the existing PWG LS-link scripts to process BEN with minimal
adaptation.

## Source Data

The working copy was taken from
`/Users/Shared/sanskrit-lexicon/csl-orig/v02/ben/ben.txt` at commit
**c726170** of the csl-orig repository.

Copied as:
- `temp_c72617.txt` (input, 5,809,746 bytes, 49,234 `<ls>` tags)
- `temp_c72617_pwg.txt` (output after conversion)

## Conversion Script

`convert_ls.py` — a Python 3 script that:

1. Finds every `<ls>SOURCE</ls>` in the text.
2. Examines the text that follows `</ls>`.
3. If the next token is a **digit** or a **valid Roman numeral**
   (`i`–`d` from the standard Roman set), it scans forward to the
   reference boundary (`.`, `;`, `=`, `<`, `)`, or `[`) and moves
   that reference text inside the `<ls>` tag.
4. References whose first token is **not** numeric/Roman (e.g. `in`,
   `p.`, `vol.`, `also`, `title`, `ed.`) are left unchanged.

### Iteration

| Pass | Converted | Notes |
|------|-----------|-------|
| 1    | 41,644    | Arabic-only refs |
| 2    | 45,528    | Added Roman-numeral handling; fixed false positives from words like `in` starting with `i` |

### Verification

The output was verified against the 47,002 `<ls>` reference analysis
from `issues/issue16/roman_analysis.txt`:

| Category | roman_analysis count | Converter result |
|---|---|---|
| Arabic first token  | 41,644 | 41,644 converted |
| Roman first token   |  3,884 |  3,884 converted |
| Other first token   |  1,474 |      0 converted (correct — not references) |
| Total analyzed      | 47,002 | 45,528 converted, 1,474 intentionally skipped |
| Unanalyzed (no token) | 2,232 | 0 converted (correct — no reference follows) |

All 45,528 references with numeric or Roman first tokens are correctly
converted.  The 3,706 unconverted tags are either cross-references
(`<ls>Daśak.</ls> in <ls>Chr.</ls>`), page citations
(`<ls>Chr.</ls> p. 234`), drama references
(`<ls>Śāk.</ls> <ab>d.</ab> 5`), or tags with no following content.

## Usage

```sh
python3 issues/issue19/convert_ls.py
```

Output is written to `issues/issue19/temp_c72617_pwg.txt`.
