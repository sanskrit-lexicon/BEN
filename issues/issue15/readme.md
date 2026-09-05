_Created: 30-06-2026 · Last updated: 05-09-2026_

# issue15 — Study of `<ls>` tags in BEN

Study of `<ls>…</ls>` tag occurrences in the Benfey Sanskrit-English Dictionary, and mapping them to expanded forms (text/author references).

## Source commits

| Source | Commit |
|---|---|
| `csl-orig` `v02/ben/ben.txt` | [`d050e48`](https://github.com/sanskrit-lexicon/csl-orig/commit/d050e48) |
| `csl-pywork` `benauth/tooltip.txt` | [`cda2ed1`](https://github.com/sanskrit-lexicon/csl-pywork/commit/cda2ed1) |

## Files

| File | Purpose |
|---|---|
| `temp_ben_0.txt` | Copy of the canonical `ben.txt` (86,989 lines, 17,036 entries) |
| `temp_ls_input.txt` | Copy of the upstream `tooltip.txt` (114 entries) from `csl-pywork` |
| `ls_input.txt` | Expanded version with all 219 unique `<ls>` tags mapped (222 entries) |
| `ls_statistics.py` | Script: frequency statistics of all `<ls>` occurrences |
| `ls_coverage.py` | Script: coverage comparison against `ls_input.txt` |
| `redo.sh` | Reproduce everything |

## Workflow

```sh
bash redo.sh             # copy source files & run both scripts
python3 ls_statistics.py # occurrence frequencies only
python3 ls_coverage.py   # coverage comparison only
```

## Results

- **49,234** total `<ls>` tag occurrences across **219** unique values in `ben.txt`.
- **100%** coverage (all 219 unique values have entries in `ls_input.txt`).

_Dr. Mārcis Gasūns_
