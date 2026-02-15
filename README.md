# get-research-done

Portable research workflow pack for AI/statistics projects.

## Install (Recommended: Python CLI)

Install the package, then run `grd-install` from anywhere.

`pipx` (recommended for isolated CLI tools):

```bash
pipx install "git+https://github.com/soheunyi/get-research-done.git"
```

`pip`:

```bash
python3 -m pip install "git+https://github.com/soheunyi/get-research-done.git"
```

From a local checkout during development:

```bash
python3 -m pip install -e .
```

Install into a target repository:

```bash
# Default target is "core" (runtime + codex/claude/opencode/gemini)
grd-install /path/to/target-repo

# Runtime docs/templates only
grd-install /path/to/target-repo --target runtime

# Per-tool
grd-install /path/to/target-repo --target codex
grd-install /path/to/target-repo --target claude
grd-install /path/to/target-repo --target opencode
grd-install /path/to/target-repo --target gemini

# Multiple targets
grd-install /path/to/target-repo --target runtime,codex

# Show valid target names
grd-install --list-targets
```

Upgrade note:
- `grd-install` and `grd-uninstall` automatically prune legacy removed skill directories from target installs.

Runtime state-aware helper:

```bash
# Show bounded state digest from .grd/STATE.md + .grd/ROADMAP.md
grd --repo-root /path/to/target-repo info

# Machine-readable output
grd --repo-root /path/to/target-repo info --json

# Build state-enriched payload for a specific skill
grd --repo-root /path/to/target-repo run --skill grd-research-cycle
grd --repo-root /path/to/target-repo run --skill grd-research-cycle --json

# Log exploration quickly
grd --repo-root /path/to/target-repo log --what "..." --happened "..." --why "..."

# Suggest next actions for a specific mode
grd --repo-root /path/to/target-repo next --mode explore
grd --repo-root /path/to/target-repo next --mode evaluate --json

# Let GRD infer the best mode from current state
grd --repo-root /path/to/target-repo next

# Promote evidence into unified hypothesis format
grd --repo-root /path/to/target-repo promote \
  --title "Curriculum schedule hypothesis" \
  --what "Added warmup + curriculum" \
  --happened "Validation stabilized" \
  --why "Reduced early optimization shock" \
  --source-entry latest \
  --artifact outputs/metrics.csv
```

Modes available in `grd next --mode`:
- `explore`
- `plan`
- `implement`
- `evaluate`
- `synthesize`
- `promote`

`grd promote` writes hypothesis artifacts to `.grd/hypotheses/` and uses one unified hypothesis format for both saved markdown and CLI display.

Uninstall from a target repository:

```bash
# Remove all GRD-installed skills (keeps .grd runtime artifacts by default)
grd-uninstall /path/to/target-repo

# Remove specific skill targets
grd-uninstall /path/to/target-repo --target codex,claude

# Also remove runtime docs/templates
grd-uninstall /path/to/target-repo --include-runtime

# Show valid uninstall target names
grd-uninstall --list-targets
```

## Install (Make Alternative)

Run from this repository checkout:

```bash
# Show all install targets
make install-help

# Install all supported targets + runtime docs/templates
make install-all DEST=/path/to/target-repo
```

Per-target install:

```bash
# Runtime docs/templates only
make install-runtime DEST=/path/to/target-repo

# Skills by tool
make install-codex DEST=/path/to/target-repo
make install-claude DEST=/path/to/target-repo
make install-opencode DEST=/path/to/target-repo
make install-gemini DEST=/path/to/target-repo

# Core set (runtime + codex/claude/opencode/gemini)
make install-core DEST=/path/to/target-repo
```

## Installed Paths

- Runtime docs/templates:
  - `.grd/workflows/research-pipeline.md`
  - `.grd/templates/*`
- Skills:
  - Codex/OpenCode: `.agents/skills/*/SKILL.md`
  - Claude Code: `.claude/skills/*/SKILL.md`
  - OpenCode native: `.opencode/skills/*/SKILL.md`
  - Gemini CLI: `.gemini/skills/*/SKILL.md`

## Current Shipped Skills

- `grd-research-cycle`
- `grd-question-maker`
- `grd-observer`
- `grd-algo-implementer`
- `grd-algo-verifier`
- `grd-ablation-recommender`
- `grd-ops-and-reproducibility`
- `grd-reference-librarian`
- `grd-research-note-taker`
- `grd-build-architect`
- `grd-state-keeper`
- `grd-skill-reliability-keeper`

## Source Of Truth

- Core skills: `skills/*`
- Core workflow: `workflows/research-pipeline.md`
- Templates: `templates/*`
- Global shared blocks: `skills/_shared/BASE.md`
- Profile base + role deltas: `skills/_shared/profiles/base.md`, `skills/_shared/profiles/{executor,advisor,orchestrator}.md`
- Skill-to-profile map: `skills/_shared/skill-profiles.json`

Skill generation:
- Skill-specific source: `skills/*/SKILL.src.md`
- Generated output: `skills/*/SKILL.md` (via `make sync-skills`)
- Render model: `{{COMMON_BLOCKS}}` expands to global blocks + profile-base blocks + role-specific deltas/overrides.

Skill length budget:
- Budget applies to `SKILL.src.md` only (generated `SKILL.md` is derived output).
- Target: `SKILL.src.md` <= 80 lines.
- Move detailed procedures/examples into `references/` and keep source files task-critical.
- Check with `make check-skill-lengths` (also included in `make check-skills`).

Skill references policy:
- Every `skills/grd-*` skill must include at least one `references/*.md` file.
- `SKILL.src.md` should remain an orchestration shell and explicitly point to `references/...` files for detailed contracts.
- Check with `make check-skill-references` (also included in `make check-skills`).

Questioning policy:
- Shared loop is adaptive-minimal: ask questions only for blocking/material ambiguity.
- Ask at most one high-leverage question per response.
- Options and "Captured so far" recap are optional scaffolding, not mandatory turn-by-turn output.
- Check with `make check-questioning-policy` (also included in `make check-skills`).

Note-taking artifacts:
- `grd-research-note-taker` defaults to `.grd/research/<topic_or_run>/NOTES.md`
- Optional digest append target: `.grd/research/RESEARCH_NOTES.md`

`codex/` and `agy/` are generated compatibility views and are intentionally git-ignored.

## Dev Sync Commands

```bash
# Sync shared boilerplate into skills
make sync-skills

# Validate shared boilerplate sync
make check-skills

# Regenerate compatibility views locally (git-ignored)
make sync-codex
make sync-agy
```

## Script Installer (Optional)

Shell:

```bash
bash scripts/install.sh /path/to/target-repo
```

PowerShell:

```powershell
.\scripts\install.ps1 -Root "C:\path\to\target-repo"
```
