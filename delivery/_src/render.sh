#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD="$(mktemp -d "${TMPDIR:-/tmp}/discmath-latex.XXXXXX")"
trap 'rm -rf "$BUILD"' EXIT
tectonic --outdir "$BUILD" "$DIR/1a-graphs.tex"
cp "$BUILD/1a-graphs.pdf" "$DIR/../1a-graphs.pdf"
