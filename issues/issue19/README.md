_Created: 05-07-2026 · Last updated: 05-09-2026_

# issue19: Convert BEN `<ls>` References to PWG-Style Format (Round-Trip)

Converts BEN's `<ls>` markup from the CDSL standard style
(`<ls>MBh.</ls> 14, 34.`) to the PWG style
(`<ls>MBh. 14, 34</ls>.`), where reference numbers are moved
*inside* the `<ls>` tag. The reverse script (`revert_ls.py`)
restores the original format, verified by `diff` against the
source file.

## Motivation

PWG already uses the inline style. Making BEN consistent with PWG
allows the existing PWG LS-link scripts to process BEN with minimal
adaptation.

## Source Data

The working copy was taken from
`/Users/Shared/sanskrit-lexicon/csl-orig/v02/ben/ben.txt` at commit
**c726170** of the csl-orig repository.

| File | Role |
|---|---|
| `temp_c72617.txt` | Original input (5,809,746 bytes, 49,234 `<ls>` tags) |
| `temp_ben_1.txt` | Forward output from `convert_ls.py` |
| `temp_ben_2.txt` | Reverse output from `revert_ls.py` |

## Scripts

### `convert_ls.py` (forward)

Finds every `<ls>SOURCE</ls>` and moves following reference text
inside the tag. Three strategies:

1. **Standard ref extraction**: If the text after `</ls>` starts with
   a digit or valid Roman numeral, it is scanned forward to the
   reference boundary (`.`, `;`, `=`, `<`, `)`, `[`, `]`) and moved
   inside the `<ls>` tag.

   **Period continuation**: For Roman-kind refs, `.` allows continuation
   when the next token is a ref token (e.g. `i. 88. 3` is a single
   reference). For Arabic-kind refs, `.` is always a hard barrier —
   `6, 12. 2` stops at `6, 12` (the `2` is a definition marker, not
   a ref continuation). This prevents ~695 false-positive merges.

   **Roman-source filtering**: `build_roman_sources()` scans the raw
   data to build a set of source abbreviations that actually use Roman
   numeral first tokens. Roman detection is suppressed for sources
   (e.g. `Chr.`, `Ragh.`) with 0% Roman usage, preventing false
   positives for any future entries with Roman-looking tokens.

2. **"X in Y" cross-reference pattern**: When text after `</ls>`
   starts with `in` (optionally followed by `.`) and the next
   `<ls>` tag immediately follows (with only whitespace and optional
   period between), the two tags are merged into
   `<ls>X in. Y REF</ls>`. A `<ls>` that is not immediately adjacent
   (e.g. `in Weber, <ls>Ind. St.</ls>`) is NOT merged.

3. **`<ab>` tag handling**: `<ab>…</ab>` tags between `</ls>` and
   the reference digits are included inside the merged `<ls>` tag.

### `revert_ls.py` (reverse)

Splits merged `<ls>` tags back into the two-tag original format:

1. **Standard split**: Finds the ref-start token and separates
   source abbreviation from reference text.

2. **"in" pattern split**: Detects ` in ` or ` in. ` within the
   content and reconstructs `<ls>X</ls> in. <ls>Y</ls> REF`.

3. **`<ab>` restoration**: `<ab>` tags before the ref are moved
   back outside the `<ls>` tag.

## Verification

Round-trip: `diff temp_c72617.txt temp_ben_2.txt` shows **0 semantic
differences** — 2 cosmetic spacing lines remain (original
`<ls>Bhāg. P.</ls>6, 17` vs reverse `<ls>Bhāg. P.</ls> 6, 17`;
original `<ls>R.</ls>11. 61` vs reverse `<ls>R.</ls> 11. 61`).
`rg '</ls>\w' temp_ben_1.txt` returns 0 matches.

### Tag counts

| Metric | Count |
|---|---|
| Original `<ls>` tags (`c72617.txt`) | 49,234 |
| Forward output `<ls>` tags (`ben_1.txt`) | 47,821 |
| Reverse output `<ls>` tags (`ben_2.txt`) | 49,234 |
| Reverted (successfully split) | 47,165 |

### Forward converter coverage

| Category | Handled | Not handled |
|---|---|---|
| Arabic first token | 43,269 | 0 |
| Roman first token | 3,896 | 0 |
| Other (letter token) | 0 | 61 |
| Unanalyzed (no token) | 0 | 595 |

Unhandled tags (656 total) include cross-references without
trailing refs (`<ls>Chr.</ls> p. 234`), drama references
(`<ls>Śāk.</ls> <ab>d.</ab> 5`), and tags with no following
reference content. These are passed through unchanged and
correctly left unmodified by the reverse script.

## Usage

```sh
python3 issues/issue19/convert_ls.py
python3 issues/issue19/revert_ls.py
```

Outputs written to `temp_ben_1.txt` and `temp_ben_2.txt`.

_Dr. Mārcis Gasūns_
