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
| `ls_statistics.py` | Script: frequency statistics of all `<ls>` occurrences |
| `ls_coverage.py` | Script: coverage comparison against `temp_ls_input.txt` |
| `redo.sh` | Reproduce everything |

## Workflow

```sh
bash redo.sh             # copy source files & run both scripts
python3 ls_statistics.py # occurrence frequencies only
python3 ls_coverage.py   # coverage comparison only
```

## Results

- **49,234** total `<ls>` tag occurrences across **219** unique values in `ben.txt`.
- **50.7%** coverage (111 of 219 unique values have entries in `tooltip.txt`).

### Top 10 most frequent

| Value | Count | % |
|---|---|---|
| `MBh.` | 7,384 | 15.00% |
| `Man.` | 6,058 | 12.30% |
| `Rām.` | 5,162 | 10.48% |
| `Pañc.` | 4,797 | 9.74% |
| `Chr.` | 3,017 | 6.13% |
| `Bhāg. P.` | 1,896 | 3.85% |
| `Hit.` | 1,740 | 3.53% |
| `Rājat.` | 1,326 | 2.69% |
| `Vikr.` | 1,162 | 2.36% |
| `Śāk.` | 1,106 | 2.25% |

### Uncovered high-frequency tags

The top tags lacking expansions (≥20 occurrences):

| Value | Count |
|---|---|
| `Hit. pr.` | 91 |
| `Berl. Monatsb.` | 56 |
| `Pañc. pr.` | 28 |
| `Journ. of the German Oriental Society` | 20 |
| `Brahmav.` | 8 |
| `Lass. Anth.` | 7 |
| `Viṣṇu P.` | 7 |
| `Berol.` | 6 |
| `Bhāg.` | 6 |
| `Kāśīkh.` | 5 |
| `Skandap., Kāśīkh.` | 4 |
| `VP.` | 4 |
