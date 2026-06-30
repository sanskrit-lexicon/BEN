#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Copying source files ==="
cp /Users/Shared/sanskrit-lexicon/csl-orig/v02/ben/ben.txt "$SCRIPT_DIR/temp_ben_0.txt"
# NOT copying benab_input.txt - it's tracked in this repo
# cp "/Users/Shared/sanskrit-lexicon/csl-pywork/v02/distinctfiles/ben/pywork/benab/benab_input.txt" "$SCRIPT_DIR/benab_input.txt"

echo ""
echo "=== Running ab_statistics.py ==="
python3 "$SCRIPT_DIR/ab_statistics.py"

echo ""
echo "=== Running ab_coverage.py ==="
python3 "$SCRIPT_DIR/ab_coverage.py"
