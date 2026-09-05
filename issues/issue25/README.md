_Created: 07-07-2026 · Last updated: 05-09-2026_

# Issue 25 — Wrap bare semicolon-digit refs after `<ls>` tags

## Problem

After a citation like `<ls>Man. 8, 51</ls>`, additional verse references sometimes appear as bare digits separated by semicolons or ending a list with a period, e.g.:

```
<ls>Man. 8, 51</ls>; 60; 332.
```

Both `60` and `332` after `</ls>;` should be wrapped to make the references explicit and trackable.

## Pattern

Input:
```
<ls>SOURCE DIGIT, DIGIT</ls>; DIGIT;  ...  ; DIGIT.
```

Output:
```
<ls>SOURCE DIGIT, DIGIT</ls>; <ls n="SOURCE DIGIT,">DIGIT</ls>;  ...  ; <ls n="SOURCE DIGIT,">DIGIT</ls>.
```

The `n=` source is derived from the preceding `<ls>` content with the last ref token removed (preserving the trailing comma as book/chapter context).

Two terminator patterns are handled:
- `; DIGIT;` — digit followed by semicolon (middle of list)
- `; DIGIT.` — digit followed by period (end of list)

### `<ab>` in source context

Some `<ls>` content contains `<ab>` tags, e.g. `<ls>Vikr. <ab>d.</ab> 42</ls>`. If left in, the `n` attribute would contain raw XML (`n="Vikr. <ab>d.</ab>"`), which is invalid — an XML parser rejects `<` in attribute values.

`get_source()` strips `<ab>` and `</ab>` tags from the source string before inserting it into `n=`, keeping only the display text:

| Input `<ls>` content | `n=` value |
|---|---|
| `Vikr. <ab>d.</ab> 42` | `Vikr. d.` |
| `Pañc. iii. <ab>d.</ab> 10` | `Pañc. iii. d.` |
| `Lass. <ab>2. ed.</ab> 9, 11` | `Lass. 2. ed. 9,` |

## Solution

`convert_bare_semicolon_refs.py`:

1. **Split by `<ls>` tags**: iterates through line segments separated by `<ls>…</ls>` tags.
2. **Track current source**: for each `<ls>` tag (without `n=`), store its inner content as the source context for the next non-tag segment.
3. **Extract source for `n=`**: `get_source()` strips `<ab>`/`</ab>` tags, then removes the last token (the ref number) from the `<ls>` content; e.g. `<ls>Vikr. <ab>d.</ab> 42</ls>` → `Vikr. d.`.
4. **Replace bare digits**: regex `(?<=;)\s*(\d+)(?=;)` matches digits between semicolons without consuming the semicolons (supports consecutive refs like `; 43; 46;`).

### Consecutive bare refs

The lookahead/lookbehind approach allows shared semicolons — `; 43; 46;` becomes `; <ls n="…">43</ls>; <ls n="…">46</ls>;` rather than `; <ls n="…">43</ls>;; <ls n="…">46</ls>;`.

## Files

| File | Purpose |
|---|---|
| `temp_d1d0a18.txt` | Input base file (47,524 `<ls>` tags, 1,546 `<ls n=…>` tags) |
| `temp_ben_1.txt` | Script output — bare semicolon/period-digit refs wrapped (275 new `<ls n=…>`) |
| `temp_ben_2.txt` | Manually corrected — additional bare refs, merged split `<ls>` tags, inline source+ref wrapping |
| `diff2.txt` | Diff between script output (1) and manual correction (2) — 462 lines |
| `convert_bare_semicolon_refs.py` | Conversion script |

## Verification

```
Input  <ls> tags:              47,524
Output <ls> tags:              47,524 (unchanged)
Input  <ls n=…> tags:           1,546
Output <ls n=…> tags:           1,821 (+275)
Unwrapped '; DIGIT;' after </ls>:   51 → 0
Unwrapped '; DIGIT.' after </ls>:  170 → 0
'<' in n= attribute values:           0
Diff script vs manual correction:  610 lines
```

_Dr. Mārcis Gasūns_
