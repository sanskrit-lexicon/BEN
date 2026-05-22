### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `ben.txt`.

I ran the same two-job recipe over `csl-orig/v02/ben/ben.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `issues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — please review the findings listed below.

## Markup fixer + audit for `ben.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>X</ab> Y</ab>` | `<ab>X Y</ab>` |
| `<ab> word </ab>` | `<ab>word</ab>` |
| `<ls> word </ls>` | `<ls>word</ls>` |
| `<lang> word </lang>` | `<lang>word</lang>` |

Whitespace trimming applies to all 3 paired tag(s) in `ben.txt`: `<ab>`, `<ls>`, `<lang>`. The original file is never modified — output goes to `ben_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format). 1 line(s) changed.

### Closing-tag inventory in current `ben.txt`

| Tag | Count |
|---|---:|
| `</ab>` | 65 |
| `</514)>` | ? |
| `</ls>` | 48 |
| `</603)>` | ? |
| `</lang>` | 1 |
| `</243)>` | ? |

### What it found in current `ben.txt`

- 1 whitespace trim applied: trailing space in one `<lang>` tag.
- 2,059 within-line adjacent `</ab> <ab>` pairs — listed for verification.
- 0 `<ab n="…">` attributes — no abbreviation tooltips in ben.txt.
- 0 correction records.

### Usage

```
cd issues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/ben/ben.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `ben_fixed.txt`, `markup_fix_changes.txt`, `markup_audit.txt`.

### Summary

No unusual n= values.

### Severity

`minor`
