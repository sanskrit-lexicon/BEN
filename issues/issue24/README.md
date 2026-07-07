# Issue 24 — Wrap bare source+ref patterns outside `<ls>` tags

## Problem

Some source abbreviations followed by digit references appear as plain text outside any `<ls>` tag, e.g.:

```
<ab>adj.</ab>, <ab>f.</ab> {%śā%}, Near, Kumāras. 6, 2. {@II.@}
```

`Kumāras. 6, 2` should be `<ls>Kumāras. 6, 2</ls>`, just like all other `Kumāras.` references in the file.

## Analysis

1. Build a set of known source abbreviations from all existing `<ls>` tags (1,711 unique sources).
2. Search each line outside `<ls>` spans for patterns matching `KNOWN_SOURCE + DIGIT_REF`.
3. 21 bare source+ref patterns were found. One (`Ragh. 11` in a `;`-comment line) is a false positive.

**Genuine cases:** 20 across 10 unique tag values:

| Source | Count | Ref |
|---|---|---|
| `Kumāras.` | 15 | `6, 2`, `3, 31`, `5, 12`, `4, 5` (×2), `2, 58`, `7, 14`, `5, 25`, `5, 86`, `3, 54`, `3, 40`, `5, 83`, `5, 65`, `3, 70`, `3, 24` |
| `Matsyop.` | 4 | `22` (×2), `14`, `35` |
| `Brāhmaṇ.` | 1 | `2, 17` |

## Solution

`convert_bare_sources.py`:

1. **Build sources**: scan all `<ls>content</ls>` tags, extract the source abbreviation (text before the first ref token).
2. **Combined regex**: compile a single alternation regex with all 1,711 sources (longest-first to prefer `Brāhmaṇ.` over `Br.`).
3. **Per-line processing**: for each line, find `<ls>` spans, then find source+ref matches outside those spans. Wrap in `<ls>SOURCE REF</ls>`.

## Files

| File | Purpose |
|---|---|
| `temp_be2edf5.txt` | Input base file (47,821 `<ls>` tags) |
| `temp_ben_1.txt` | Output with 20 bare source+ref patterns wrapped |
| `convert_bare_sources.py` | Conversion script |
| `analyze_bare_sources.py` | Analysis script (scan for bare source+ref patterns) |

## Verification

```
Input  <ls> tags:  47,821
Output <ls> tags:  47,841 (+20)
Bare Kumāras./Matsyop./Brāhmaṇ. + digit remaining: 0
Lines changed: 20 (of 86,989)
<ls n="..."> tags (issue22): unchanged (1,546)
Original <ls> tags preserved: 100%
```
