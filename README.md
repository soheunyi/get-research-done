# get-research-done

Portable research workflow pack for AI/statistics projects.

## What it includes
- Antigravity research pipeline doc (generated): `agy/workflows/research-pipeline.md`
- Core research pipeline doc: `workflows/research-pipeline.md`
- Antigravity skills (generated wrappers): `agy/skills/*`
- Core skills: `skills/*`
- Stateful status helper skill: `skills/grd-state-keeper/SKILL.md`
- Conversational what-next colleague: `skills/grd-what-next-colleague/SKILL.md`
- Brownfield codebase-mapping skill: `skills/grd-codebase-mapper/SKILL.md`
- Phase implementation research skill: `skills/grd-phase-researcher/SKILL.md`
- Guided questioning loop shared block: `skills/_shared/COMMON_BLOCKS.md`
- Templates: `templates/research-notes.md`, `templates/wandb-config.md`, `templates/state.md`, `templates/roadmap.md`, `templates/research-artifact-format.md`, `templates/run-index.md`

## AGY Wrapper Sync
`skills/` + `workflows/` are the source of truth. `agy/` and `codex/` are generated compatibility views.

Regenerate wrappers after core skill/workflow changes:

```bash
python3 scripts/sync_codex_wrappers.py
python3 scripts/sync_agy_wrappers.py
```

Do not manually edit generated files in `agy/` or `codex/`.

## Skill Boilerplate Sync
Shared skill boilerplate lives in:

- `skills/_shared/COMMON_BLOCKS.md`

To update shared blocks:

1. Edit `skills/_shared/COMMON_BLOCKS.md`
2. Run `python3 scripts/sync_skill_boilerplate.py --fix`
3. Commit resulting skill updates

Checks:

- `python3 scripts/sync_skill_boilerplate.py --check`
- `make sync-skills` (same as `--fix`)
- `make sync-codex` (sync skill boilerplate + regenerate `codex/` view)
- `make check-skills` (same as `--check`)
- `make sync-agy` (regenerate AGY wrappers from core skills/workflows)

## Stateful Loop (Recommended)
For GSD-like continuity in Codex sessions:

1. Start with `grd-state-keeper`
2. Maintain `.grd/STATE.md` and `.grd/ROADMAP.md`
3. Route to stage skill (`grd-codebase-mapper`, `grd-phase-researcher`, etc.)
4. Return to state-keeper after each major result to update next action

Run artifact convention:
- Use `.grd/research/runs/{run_id}/` for linked artifacts (`0_INDEX.md`, `1_HYPOTHESIS.md`, `2_EXPERIMENT_PLAN.md`, `3_EVALUATION.md`)
- Keep `.grd/research/latest` as a symlink to the active run directory (`.grd/research/runs/{run_id}/`)

## Manual Transplant
`workflows/research-pipeline.md` is a referenced guidance doc used by skills, so keep it in `.grd/workflows/`.

```bash
# Codex + OpenCode (primary docs-aligned path)
mkdir -p /path/to/target-repo/.agents/skills
cp -R get-research-done/skills/* /path/to/target-repo/.agents/skills/

# Claude Code
mkdir -p /path/to/target-repo/.claude/skills
cp -R get-research-done/skills/* /path/to/target-repo/.claude/skills/

# OpenCode native path
mkdir -p /path/to/target-repo/.opencode/skills
cp -R get-research-done/skills/* /path/to/target-repo/.opencode/skills/

# Gemini CLI workspace skills
mkdir -p /path/to/target-repo/.gemini/skills
cp -R get-research-done/skills/* /path/to/target-repo/.gemini/skills/

# Runtime docs and templates
mkdir -p /path/to/target-repo/.grd/workflows /path/to/target-repo/.grd/templates
cp -R get-research-done/workflows/* /path/to/target-repo/.grd/workflows/
cp -R get-research-done/templates/* /path/to/target-repo/.grd/templates/
```

## Install both (Antigravity + Codex)
From the repository where this folder exists, run:

```bash
bash get-research-done/scripts/install.sh /path/to/target-repo
```

PowerShell:

```powershell
.\get-research-done\scripts\install.ps1 -Root "C:\path\to\target-repo"
```

Make-based installs (from this repo):

```bash
# Show install targets
make install-help

# Install everything
make install-all DEST=/path/to/target-repo

# Install per tool
make install-codex DEST=/path/to/target-repo
make install-claude DEST=/path/to/target-repo
make install-opencode DEST=/path/to/target-repo
make install-gemini DEST=/path/to/target-repo
make install-agy DEST=/path/to/target-repo

# Runtime docs/templates only
make install-runtime DEST=/path/to/target-repo
```

## Docs-aligned skill locations
- Codex: `.agents/skills/*/SKILL.md` (plus legacy `.codex/skills/*/SKILL.md` copied by installer)
- Claude Code: `.claude/skills/*/SKILL.md`
- OpenCode: `.opencode/skills/*/SKILL.md` (also discovers `.claude/skills` and `.agents/skills`)
- Gemini CLI: `.gemini/skills/*/SKILL.md`
