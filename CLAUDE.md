# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**BEN** is the corrections and research repository for the Cologne digitization of Benfey's *Sanskrit-English Dictionary* (1866). The canonical source lives in `csl-orig/v02/ben/ben.txt`.

## Architecture

| Directory | Purpose |
|---|---|
| `issues/` | Per-issue correction workflows (`issueNNN/` pattern) |
| `verbs01/` | Root identification: maps Benfey entries to MW root spellings, identifies prefixed verbs (upasargas) |
| `abbrev/` | Abbreviation research and markup |
| `ben_ab/` | Abbreviation pipeline for the CDSL display |
| `eng_error_lang/` | Language wordlists (Latin, A.S., O.H.G., Gothic, etc.) used to filter false positives in English spell-checking |
| `greek/` | Greek loanword and citation research |
| `2021-10-02/` | Batch error corrections from Oct 2021 |

### Issue correction pattern (`issues/issueNNN/`)

Each issue folder follows the standard workflow:
1. Copy current `ben.txt` to a local `temp_ben_0.txt` (not tracked by git)
2. Apply corrections incrementally as `temp_ben_1.txt`, `temp_ben_2.txt`, etc.
3. Rebuild XML with `generate_dict.sh` and validate with `xmlchk_xampp.sh`
4. Commit the corrected file to `csl-orig`, then sync to Cologne
5. Commit issue documentation back here

### Verb root pipeline (`verbs01/`)

Identifies Benfey verb entries and maps them to their MW equivalents:
- `ben_verb_filter.py` — identifies root entries in `ben.txt`
- Preverb mapping aligns Benfey prefixed verbs with MW headwords

## Common Commands

### Apply line-level corrections
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh ben ../../BENScan/2020
sh xmlchk_xampp.sh ben
```

## Dependencies

- **Python 3**
- **ben.txt** — in `$BASE/cologne/csl-orig/v02/ben/ben.txt`
