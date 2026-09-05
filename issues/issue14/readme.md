_Created: 30-04-2020 · Last updated: 05-09-2026_

# issue14 — Study of `<ab>` tags in BEN

Study of `<ab>…</ab>` tag occurrences in the Benfey Sanskrit-English Dictionary, and mapping them to expanded forms.

## Files

| File | Purpose |
|---|---|
| `temp_ben_0.txt` | Copy of the canonical `ben.txt` (86,989 lines, 17,036 entries) from `csl-orig/v02/ben/` at commit [`d050e48`](https://github.com/sanskrit-lexicon/csl-orig/commit/d050e48) |
| `benab_input.txt` | Curated mapping of `<ab>` tag values to their expanded meanings (283 entries). Started from `csl-pywork` source at commit [`69624d9`](https://github.com/sanskrit-lexicon/csl-pywork/commit/69624d9), then expanded. |
| `ab_statistics.py` | Script: frequency statistics of all `<ab>` occurrences |
| `ab_coverage.py` | Script: coverage comparison against `benab_input.txt` |
| `redo.sh` | Reproduce everything |

## Workflow

```sh
bash redo.sh          # copy source files & run both scripts
python3 ab_statistics.py   # occurrence frequencies only
python3 ab_coverage.py     # coverage comparison only
```

## Results

- **68,339** total `<ab>` tag occurrences across **283** unique values in `ben.txt`.
- **100%** coverage: every unique `<ab>` value has an entry in `benab_input.txt`.

### Top 10 most frequent

| Value | Count | % | Cum% |
|---|---|---|---|
| `m.` | 9,490 | 13.89% | 13.89% |
| `i. e.` | 9,168 | 13.42% | 27.30% |
| `adj.` | 8,296 | 12.14% | 39.44% |
| `f.` | 6,518 | 9.54% | 48.98% |
| `n.` | 5,818 | 8.51% | 57.49% |
| `d.` | 4,619 | 6.76% | 64.25% |
| `Comp.` | 3,057 | 4.47% | 68.73% |
| `Par.` | 1,804 | 2.64% | 71.36% |
| `cf.` | 1,657 | 2.42% | 73.79% |
| `Caus.` | 1,384 | 2.03% | 75.81% |

## Scope of expansions

The `benab_input.txt` file was built from the upstream `csl-pywork` source (106 entries) and then expanded with additional abbreviations found in the text:

- **Grammatical abbreviations**: `m.`, `f.`, `n.`, `adj.`, `adv.`, `vb.`, `pass.`, `caus.`, etc.
- **Case/number markers**: `acc.`, `gen.`, `loc.`, `instr.`, `sing.`, `pl.`, `du.`, etc.
- **Verb forms**: `pres.`, `pf.`, `fut.`, `aor.`, `imperat.`, `infin.`, `ptcple.`, etc.
- **Sanskrit grammatical terms**: `Ātm.` (Ātmanepada), `Par.` (Parasmaipada), `Bahuvr.` (Bahuvrihi), `Karmadhār.` (Karmadharaya), etc.
- **Language names**: `Lat.`, `Goth.`, `A.S.`, `O.H.G.`, `Prākṛ.`, etc.
- **Scholar/author names**: `Böhtl.` (Böhtlingk), `Bopp.`, `Stenzl.` (Stenzler), `M.M.` (Max Müller), `Wils.` (Wilson), `Chezy.`/`C.` (Chezy), `Haug.`, `Brockh.` (Brockhaus), `Tacit.` (Tacitus), `T.` (Theodor Benfey), etc.
- **Scholarly apparatus**: `ib.` (ibidem), `cf.` (confer), `q. v.` (quod vide), `sc.` (scilicet), `e. g.` (exempli gratia), `viz.` (videlicet), `ap.` (apud), etc.
- **Text references**: `rec. orn.` (recensio ornatior), `Sch.`/`Schol.` (Scholiast), `sarg.` (sarga), `adhy.` (adhyāya), `MS.`/`MSS.` (manuscript).

_Dr. Mārcis Gasūns_
