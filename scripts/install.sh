#!/bin/bash
set -euo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="${1:-.}"
mkdir -p "$ROOT"
ROOT="$(cd "$ROOT" && pwd)"

mkdir -p "$ROOT/.agent/skills" "$ROOT/.codex/skills" "$ROOT/.grd/templates"

cp -R "$PACK_DIR/agy/skills/"* "$ROOT/.agent/skills/"
cp -R "$PACK_DIR/codex/skills/"* "$ROOT/.codex/skills/"
cp "$PACK_DIR/templates/research-notes.md" "$ROOT/.grd/templates/research-notes.md"
cp "$PACK_DIR/templates/wandb-config.md" "$ROOT/.grd/templates/wandb-config.md"

# Also copy this pack into the target so installer scripts are available there.
if [ "$ROOT/get-research-done" != "$PACK_DIR" ]; then
  rm -rf "$ROOT/get-research-done"
  cp -R "$PACK_DIR" "$ROOT/get-research-done"
fi

echo "Installed get-research-done pack into $ROOT"
echo 'Use Codex skills: $grd-research-hypothesis-designer, $grd-research-experiment-planner, $grd-research-evaluation-analyst'
