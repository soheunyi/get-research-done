# get-research-done

Portable research workflow pack for AI/statistics projects.

## What it includes
- Antigravity research pipeline doc: `agy/workflows/research-pipeline.md`
- Codex research pipeline doc: `codex/workflows/research-pipeline.md`
- Antigravity skills: `agy/skills/*`
- Codex skills: `codex/skills/*`
- Templates: `templates/research-notes.md`, `templates/wandb-config.md`

## Codex Skill Boilerplate Sync
Shared Codex skill boilerplate lives in:

- `codex/skills/_shared/COMMON_BLOCKS.md`

To update shared blocks:

1. Edit `codex/skills/_shared/COMMON_BLOCKS.md`
2. Run `python3 scripts/sync_skill_boilerplate.py --fix`
3. Commit resulting skill updates

Checks:

- `python3 scripts/sync_skill_boilerplate.py --check`
- `make sync-skills` (same as `--fix`)
- `make check-skills` (same as `--check`)

## Transplant for Antigravity only
Antigravity supports slash commands (for example `/grd-...`) from workflow assets in `agy/workflows/`.

Copy these into your target repo:

```bash
mkdir -p /path/to/target-repo/.agent/skills
cp -R get-research-done/agy/skills/* /path/to/target-repo/.agent/skills/
cp -R get-research-done/agy/workflows /path/to/target-repo/get-research-done/agy/
```

## Transplant for Codex only
Codex does not support Antigravity slash commands. In Codex, `codex/workflows/research-pipeline.md` is a referenced guidance doc used by Codex skills (not a slash-command source), so keep it alongside installed skills.

```bash
mkdir -p /path/to/target-repo/.codex/skills
cp -R get-research-done/codex/skills/* /path/to/target-repo/.codex/skills/
cp -R get-research-done/codex/workflows /path/to/target-repo/get-research-done/codex/
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
