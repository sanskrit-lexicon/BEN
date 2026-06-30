#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "========================================"
echo "  BEN pipeline: step1 → step2 → step3 → step4"
echo "========================================"
echo

# ---- step1 ----
echo ">>> step1.py (CDSL transformations + AB normalization) <<<"
python3 step1.py 2>&1
echo

# ---- step2 ----
echo ">>> step2.py (abbreviation tagging) <<<"
python3 step2.py 2>&1
echo

# ---- step3 ----
echo ">>> step3.py (page line numbers into AB) <<<"
python3 step3.py 2>&1
echo

# ---- step4 ----
echo ">>> step4.py (Greek tags from CDSL into AB) <<<"
python3 step4.py 2>&1
echo

# ---- final diff ----
echo "========================================"
echo "  Final diff (CDSL ben3 vs AB ben4)"
echo "========================================"
git diff --word-diff-regex=. --no-index \
  derivatives/temp_cdsl_ben3.txt \
  derivatives/temp_ab_ben4.txt \
  | wc -c
echo

echo "Pipeline complete."
