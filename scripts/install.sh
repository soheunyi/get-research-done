#!/bin/bash
set -euo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="${1:-.}"
mkdir -p "$ROOT"
ROOT="$(cd "$ROOT" && pwd)"

# Project-local skill locations (official docs + compatibility)
mkdir -p \
  "$ROOT/.agents/skills" \
  "$ROOT/.claude/skills" \
  "$ROOT/.opencode/skills" \
  "$ROOT/.gemini/skills" \
  "$ROOT/.codex/skills" \
  "$ROOT/.agent/skills" \
  "$ROOT/.grd/templates" \
  "$ROOT/.grd/workflows"

# Core skills: shared across Codex/Claude/OpenCode/Gemini layouts.
cp -R "$PACK_DIR/skills/"* "$ROOT/.agents/skills/"
cp -R "$PACK_DIR/skills/"* "$ROOT/.claude/skills/"
cp -R "$PACK_DIR/skills/"* "$ROOT/.opencode/skills/"
cp -R "$PACK_DIR/skills/"* "$ROOT/.gemini/skills/"
cp -R "$PACK_DIR/skills/"* "$ROOT/.codex/skills/"   # legacy Codex layouts
cp -R "$PACK_DIR/agy/skills/"* "$ROOT/.agent/skills/" # legacy AGY layout

cp -R "$PACK_DIR/templates/"* "$ROOT/.grd/templates/"
cp -R "$PACK_DIR/workflows/"* "$ROOT/.grd/workflows/"

# Copy workflow references (without copying .git or unrelated repo files).
mkdir -p "$ROOT/get-research-done/agy"
rm -rf "$ROOT/get-research-done/agy/workflows" "$ROOT/get-research-done/workflows"
cp -R "$PACK_DIR/agy/workflows" "$ROOT/get-research-done/agy/"
cp -R "$PACK_DIR/workflows" "$ROOT/get-research-done/"

# Keep templates/scripts/readme available in target pack path for manual transplant.
rm -rf "$ROOT/get-research-done/templates" "$ROOT/get-research-done/scripts"
cp -R "$PACK_DIR/templates" "$ROOT/get-research-done/"
cp -R "$PACK_DIR/scripts" "$ROOT/get-research-done/"
cp "$PACK_DIR/README.md" "$ROOT/get-research-done/README.md"

echo "Installed get-research-done pack into $ROOT"
echo "Skill targets:"
echo "  - $ROOT/.agents/skills      (Codex/OpenCode)"
echo "  - $ROOT/.claude/skills      (Claude/OpenCode)"
echo "  - $ROOT/.opencode/skills    (OpenCode)"
echo "  - $ROOT/.gemini/skills      (Gemini CLI workspace skills)"
echo "  - $ROOT/.codex/skills       (legacy compatibility)"
echo "Runtime docs: $ROOT/.grd/workflows/research-pipeline.md"
echo 'Use GRD skills: $grd-hypothesis-designer, $grd-experiment-planner, $grd-evaluation-analyst'
