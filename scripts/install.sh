#!/bin/bash
set -euo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="${1:-.}"
mkdir -p "$ROOT"
ROOT="$(cd "$ROOT" && pwd)"

# Project-local skill locations (docs-aligned)
mkdir -p \
  "$ROOT/.agents/skills" \
  "$ROOT/.claude/skills" \
  "$ROOT/.opencode/skills" \
  "$ROOT/.gemini/skills" \
  "$ROOT/.grd/templates" \
  "$ROOT/.grd/workflows"

# Core skills: shared across Codex/Claude/OpenCode/Gemini layouts.
cp -R "$PACK_DIR/skills/"* "$ROOT/.agents/skills/"
cp -R "$PACK_DIR/skills/"* "$ROOT/.claude/skills/"
cp -R "$PACK_DIR/skills/"* "$ROOT/.opencode/skills/"
cp -R "$PACK_DIR/skills/"* "$ROOT/.gemini/skills/"

cp -R "$PACK_DIR/templates/"* "$ROOT/.grd/templates/"
cp -R "$PACK_DIR/workflows/"* "$ROOT/.grd/workflows/"

echo "Installed get-research-done pack into $ROOT"
echo "Skill targets:"
echo "  - $ROOT/.agents/skills      (Codex/OpenCode)"
echo "  - $ROOT/.claude/skills      (Claude/OpenCode)"
echo "  - $ROOT/.opencode/skills    (OpenCode)"
echo "  - $ROOT/.gemini/skills      (Gemini CLI workspace skills)"
echo "Runtime docs: $ROOT/.grd/workflows/research-pipeline.md"
echo 'Use GRD skills: Research Cycle, Question Maker, Observer, Algo Implementer, Algo Verifier, Ablation Recommender, Research Ops and Reproducibility, Reference Librarian, Build Architect, Research State Keeper, Skill Reliability Keeper'
