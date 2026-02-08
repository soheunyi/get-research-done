# get-research-done

Portable research workflow pack for AI/statistics projects.

## What it includes
- Research pipeline doc: `workflows/research-pipeline.md`
- AGY skills: `.agents/skills/*`
- Codex skills: `.codex/skills/*`
- Templates: `templates/research-notes.md`, `templates/wandb-config.md`

## Install into another repo
From the repository where this folder exists:

```bash
bash get-research-done/scripts/install.sh /path/to/target-repo
```

PowerShell:

```powershell
.\get-research-done\scripts\install.ps1 -Root "C:\path\to\target-repo"
```
