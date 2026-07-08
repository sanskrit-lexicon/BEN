# Issue 29: `<ab>` → `<lex>` tag conversion

## Files
- `convert_lex_tags.py` — Python script that applies the transformations below.
- `temp_ben_1.txt` — Output file (derived from `csl-orig/v02/ben/ben.txt`) with all changes applied.

## Changes

### 1. Abbreviation tag conversion (`<ab>` → `<lex>`)
| Original `<ab>` | New `<lex>` tag | Count |
|---|---|---|
| `<ab>Adj.</ab>` | `<lex>Adj.</lex>` | 1 |
| `<ab>adj.</ab>` | `<lex>adj.</lex>` | 8,296 |
| `<ab>adv.</ab>` | `<lex>adv.</lex>` | 1,042 |
| `<ab>f.</ab>` | `<lex>f.</lex>` | 6,518 |
| `<ab>fem.</ab>` | `<lex>fem.</lex>` | 52 |
| `<ab>ind.</ab>` | `<lex>ind.</lex>` | 6 |
| `<ab>indecl.</ab>` | `<lex>indecl.</lex>` | 28 |
| `<ab>m.</ab>` | `<lex>m.</lex>` | 9,490 |
| `<ab>msc.</ab>` | `<lex>msc.</lex>` | 6 |
| `<ab>n.</ab>` | `<lex>n.</lex>` | 5,795 |
| `<ab>ntr.</ab>` | `<lex>ntr.</lex>` | 9 |

### 2. `<ab>n.</ab>` preserved inside `<ls>`
23 instances of `<ab>n.</ab>` inside `<ls>…</ls>` are kept as `<ab>n.</ab>` because these mark 'note' (Latin *nota*), not the neuter gender.  
Example: `<ls>.... <ab>n.</ab> ....</ls>`.

### 3. Space insertions
| Before | After | Count |
|---|---|---|
| `<ab>i.e.</ab>` | `<ab>i. e.</ab>` | 9,208 |
| `<ab>s.v.</ab>` | `<ab>s. v.</ab>` | 106 |
| `<ab>v.r.</ab>` | `<ab>v. r.</ab>` | 309 |

### 4. Remove `<ab>` wrapper after `<ls>Hit.`
| Before | After | Count |
|---|---|---|
| `<ls>Hit. <ab>Pr.</ab>` | `<ls>Hit. Pr.` | 26 |

## Running
```sh
python3 convert_lex_tags.py
```
Output: `temp_ben_1.txt`.
