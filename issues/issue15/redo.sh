#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Copying source files ==="
cp /Users/Shared/sanskrit-lexicon/csl-orig/v02/ben/ben.txt "$SCRIPT_DIR/temp_ben_0.txt"
cp "/Users/Shared/sanskrit-lexicon/csl-pywork/v02/distinctfiles/ben/pywork/benauth/tooltip.txt" "$SCRIPT_DIR/temp_ls_input.txt"

echo ""
echo "=== Running ls_statistics.py ==="
python3 "$SCRIPT_DIR/ls_statistics.py"

echo ""
echo "=== Running ls_coverage.py ==="
python3 "$SCRIPT_DIR/ls_coverage.py"
