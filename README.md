# get-research-done

Portable research workflow pack for AI/statistics projects.

## Install (Recommended: Make)

Run from this repository:

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

## Source Of Truth

- Core skills: `skills/*`
- Core workflow: `workflows/research-pipeline.md`
- Templates: `templates/*`
- Shared blocks: `skills/_shared/COMMON_BLOCKS.md`

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
