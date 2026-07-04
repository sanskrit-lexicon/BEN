# issue16: `<ls>` Reference Analysis

Analyses the consistency of literary source (`<ls>`) references across
the BEN dictionary text, from two complementary angles.

## Input

`temp_ben_0.txt` — a correction-stage copy of the BEN dictionary
(derived from `csl-orig/v02/ben/ben.txt` with issue-15 corrections
applied).  Contains ~17,000 entries with CDSL-standard markup.

## Scripts

### `trailing_digits.py` — Digit-Block Consistency

Classifies each `<ls>` reference by the number of *digit blocks* after
`</ls>` (the period- or semicolon-terminated sequence of numbers,
commas, and spaces that follows the tag).

**Example:**

    <ls>Man.</ls> 9, 47.  →  2 digit blocks (9, 47)
    <ls>MBh.</ls> 1, 3, 25.  →  3 digit blocks (1, 3, 25)

Sources like MBh. use **book, chapter, verse** (3 blocks), while
others use **chapter, verse** (2 blocks).  The script finds each
source's dominant block count and reports:

- A summary table (total matches by source, with block-count
  distributions and a consistency flag).
- All **non-conforming** references — entries whose block count
  differs from the source's majority pattern — with line numbers.
- A detailed per-source breakdown with example lines.

Run:

    python3 issues/issue16/trailing_digits.py

Output: `trailing_digits.txt`

### `analyze_roman.py` — Roman Numeral First-Token Analysis

Examines the *first token* after every `<ls>` tag and classifies it
as a **Roman numeral**, an **Arabic digit**, or **other** (text or
punctuation).

This reveals each source's citation convention:

| Source | Pattern | Example |
|---|---|---|
| Rigv. | Roman book, Arabic verse | `<ls>Rigv.</ls> i. 50, 7. |
| Hit. | Roman section, Arabic page/line | `<ls>Hit.</ls> ii. 117. |
| Pañc. | Roman section, Arabic story/line | `<ls>Pañc.</ls> iii. 144. |
| MBh., Man., Rām. | All-Arabic book, chapter, verse | `<ls>MBh.</ls> 1, 3, 25. |

The script reports:

- Overall statistics (total refs, % Roman, % Arabic, % other).
- A per-source table.
- Sources that use Roman numerals, with the specific numerals found.
- Sources with **mixed** Roman + Arabic usage (with line-numbered
  examples of each).
- References where the first token is neither Roman nor Arabic
  (e.g. `Daśak. in Chr.`, `Chr. p. 234`, `MBh. vol.`).
- Detailed Roman-usage breakdown per source.

Run:

    python3 issues/issue16/analyze_roman.py

Output: `roman_analysis.txt`

## Workflow

1. Run `trailing_digits.py` to find digit-block outliers (e.g. a
   1-block MBh. ref where 3 is expected — likely a typo).
2. Run `analyze_roman.py` to confirm each source's citation
   convention and flag anomalous mixing of Roman and Arabic.
3. Inspect flagged lines in the source and decide whether they
   need correction.

## Key Findings

- **No source mixes Arabic and Roman numerals within a single
  citation path.**  Roman numerals always occupy the first
  positional token (book / canto number); the rest are Arabic.
- The `vi` token is often a false positive for Roman numeral 6;
  in context it is the Sanskrit prefix `vi-`.
- ~1,474 references have a non-numeric first token — mostly
  nested citations (`Daśak. in Chr.`) and page references
  (`Chr. p. 234`).
