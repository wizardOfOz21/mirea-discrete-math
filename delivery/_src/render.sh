#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
NAME="${1:-1a-graphs}"
case "$NAME" in
  ''|*[!a-zA-Z0-9_-]*) echo "Укажите имя .tex-файла без расширения и пути." >&2; exit 1 ;;
esac
BUILD="$(mktemp -d "${TMPDIR:-/tmp}/discmath-latex.XXXXXX")"
trap 'rm -rf "$BUILD"' EXIT
tectonic --outdir "$BUILD" "$DIR/$NAME.tex"
cp "$BUILD/$NAME.pdf" "$DIR/../$NAME.pdf"
