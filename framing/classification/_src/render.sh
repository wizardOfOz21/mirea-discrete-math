#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$DIR/generate.py"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
PROFILE="$(mktemp -d /tmp/msc2020-render.XXXXXX)"
trap 'rm -rf "$PROFILE"' EXIT
"$CHROME" --headless --disable-gpu --no-pdf-header-footer --user-data-dir="$PROFILE" \
  --print-to-pdf="$DIR/../tasks-msc2020.pdf" "file://$DIR/tasks-msc2020.html"
