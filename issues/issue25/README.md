# Issue 25 — Wrap bare semicolon-digit refs after `<ls>` tags

## Problem

After a citation like `<ls>Man. 8, 51</ls>`, additional verse references sometimes appear as bare digits separated by semicolons, e.g.:

```
<ls>Man. 8, 51</ls>; 60; 332.
```

The `60` after `</ls>;` should be wrapped as `<ls n="Man. 8,">60</ls>` to make the reference explicit and trackable.

## Pattern

Input:
```
<ls>SOURCE DIGIT, DIGIT</ls>; DIGIT;
```

Output:
```
<ls>SOURCE DIGIT, DIGIT</ls>; <ls n="SOURCE DIGIT,">DIGIT</ls>;
```

The `n=` source is derived from the preceding `<ls>` content with the last ref token removed (preserving the trailing comma as book/chapter context).

## Solution

`convert_bare_semicolon_refs.py`:

1. **Split by `<ls>` tags**: iterates through line segments separated by `<ls>…</ls>` tags.
2. **Track current source**: for each `<ls>` tag (without `n=`), store its inner content as the source context for the next non-tag segment.
3. **Extract source for `n=`**: `get_source()` removes the last token (the ref number) from the `<ls>` content; e.g. `Man. 8, 51` → `Man. 8,`.
4. **Replace bare digits**: regex `(?<=;)\s*(\d+)(?=;)` matches digits between semicolons without consuming the semicolons (supports consecutive refs like `; 43; 46;`).

### Consecutive bare refs

The lookahead/lookbehind approach allows shared semicolons — `; 43; 46;` becomes `; <ls n="…">43</ls>; <ls n="…">46</ls>;` rather than `; <ls n="…">43</ls>;; <ls n="…">46</ls>;`.

## Files

| File | Purpose |
|---|---|
| `temp_d1d0a18.txt` | Input base file (47,524 `<ls>` tags, 1,546 `<ls n=…>` tags) |
| `temp_ben_1.txt` | Output with 70 bare semicolon-digit refs wrapped |
| `convert_bare_semicolon_refs.py` | Conversion script |

## Verification

```
Input  <ls> tags:        47,524
Output <ls> tags:        47,524 (unchanged)
Input  <ls n=…> tags:     1,546
Output <ls n=…> tags:     1,616 (+70)
Unwrapped '; DIGIT;' after </ls>: 51 → 0
Remaining bare `; DIGIT;` outside <ls> context: 1 (inline `ii. 3; 5; 9` not after a citation — correct)
```
