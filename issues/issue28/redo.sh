#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== step1: split & resolve compound suffixes ==="
python3 step1.py temp_ben_0.txt temp_ben_1.txt log1.tsv

echo ""
echo "=== step2: assign permanent L-numbers ==="
python3 step2.py temp_ben_1.txt temp_ben_2.txt log2.tsv

echo ""
echo "=== Done ==="
echo "Output: temp_ben_2.txt"
echo "Log:    log1.tsv, log2.tsv"
