# BEN — Benfey *A Sanskrit-English Dictionary* (1866)

Development and correction repository for **Theodor Benfey's *A Sanskrit-English Dictionary***, a Sanskrit→English dictionary, part of the [Cologne Digital Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) (CDSL). The canonical source text lives in [`csl-orig/v02/ben/ben.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/ben/ben.txt) (17,036 entries); this repository holds the development, correction, and enrichment work.

Notable for comparative/etymological notes, including Greek cognates (`<lang n="greek">`).

## Documentation

- [CLAUDE.md](CLAUDE.md) — repository guide and data-format reference.
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) — markup tag reference.
- [CONTRIBUTING.md](CONTRIBUTING.md) · [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## Contents

| Path | Purpose |
|---|---|
| `2021-10-02/` | `2021-10-02/` working files |
| `abbrev/` | Abbreviation-markup preparation |
| `ben_ab/` | `ben_ab/` working files |
| `eng_error_lang/` | `eng_error_lang/` working files |
| `greek/` | `greek/` working files |
| `issues/` | Per-issue working files |
| `verbs01/` | Verb identification: maps verb entries to MW roots, with Devanāgarī renderings |

## Timeline

| Period | Activity |
|---|---|
| 2020 | Repository activity begins (first tracked issues) |
| 2021–2024 | Ongoing corrections, markup, and comparison work |
| 2026-05 | Issue taxonomy, citation metadata, documentation |

## Projects & Milestones

| Milestone | Open | Closed | Total |
|---|---|---|---|
| Dictionary to Book | 0 | 0 | 0 |
| Digitization Quality | 1 | 3 | 4 |
| Structured Data | 0 | 4 | 4 |
| Major Enhancements | 3 | 0 | 3 |
| **Total** | **4** | **7** | **11** |

```mermaid
pie showData
  title BEN issues by milestone
  "Digitization Quality" : 4
  "Structured Data" : 4
  "Major Enhancements" : 3
```

## Issues

```mermaid
pie showData
  title BEN issues by type
  "markup" : 4
  "content-enhancement" : 3
  "encoding" : 2
  "bug" : 1
  "scan-quality" : 1
```

### Open

| # | Title | Type | Severity | Milestone |
|---|---|---|---|---|
| 1 | verbs01 | content-enhancement | medium | Major Enhancements |
| 5 | Mine Andhrabharati's version | content-enhancement | medium | Major Enhancements |
| 7 | oM, o~, and Unicode Character 'DEVANAGARI OM' | bug | minor | Digitization Quality |
| 11 | docs-pass: BEN documentation review | content-enhancement | medium | Major Enhancements |

### Solved

| # | Title | Type | Severity | Milestone |
|---|---|---|---|---|
| 2 | Abbreviation markup | markup | minor | Structured Data |
| 3 | Addl. strings for ab, ls and bot markings | markup | minor | Structured Data |
| 4 | New scanned images | scan-quality | minor | Digitization Quality |
| 6 | Greek text | encoding | minor | Digitization Quality |
| 8 | Greek text proofreading | encoding | minor | Digitization Quality |
| 9 | Replacing ben_hwextra with Lbody | markup | minor | Structured Data |
| 10 | [markup] Minor ben.txt Markup Oddities | markup | minor | Structured Data |

## Labels

### Type labels

| Label | Meaning |
|---|---|
| `link-target` | Click-throughs from `<ls>` abbreviations to scanned PDF pages |
| `link-splitting` | Splitting combined `SOURCE N,N` refs into per-page links |
| `markup` | Normalising XML tag content |
| `text-correction` | Corrections to English/Sanskrit definitions or headwords |
| `content-enhancement` | New material or structural additions beyond correction |
| `encoding` | SLP1/IAST transcoding, character normalisation |
| `scan-quality` | Replacing blurry/skewed/missing scan pages |
| `bug` | Broken links, XML errors, broken downloads |
| `question` | Scholarly questions requiring research |

### Severity labels

| Label | Meaning |
|---|---|
| `minor` | Targeted fix — a handful of lines or a single file |
| `medium` | Standard unit of work — one batch of corrections |
| `hard` | Large effort spanning many sources or files |

## Contributors

| Contributor | Commits |
|---|---|
| funderburkjim | 20 |
| gasyoun (Mārcis Gasūns) | 8 |
| drdhaval2785 | 7 |
| AnnaRybakovaT | 1 |

## Source

- **Author**: Benfey, Theodor
- **Title**: *A Sanskrit-English Dictionary*
- **Place / Publisher**: London: Longmans, Green
- **Year(s)**: 1866
- **Language pair**: Sanskrit → English
- **Size (CDSL headword index)**: 17,036 entries
- **License (digital edition)**: CC BY-SA 4.0
- See [CITATION.cff](CITATION.cff) for machine-readable citation.

## Encoding

- UTF-8 (NFC) throughout.
- Sanskrit text in SLP1 transliteration, wrapped in `{#…#}`; English gloss / italic display text in `{%…%}`.
- Devanāgarī and IAST display forms are generated at display time, not stored in the source.

## How it works

```mermaid
flowchart LR
  S["Print scan"] -->|keyboarding| O["csl-orig/v02/ben/ben.txt"]
  O -->|updateByLine.py| C["change_*.txt corrections"]
  C --> O
  O --> V["verbs01/ verb identification"]
  O -->|csl-pywork build| X["ben.xml"]
  X --> A["csl-app web display"]
```

---
*Issue taxonomy and documentation per the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md).*
