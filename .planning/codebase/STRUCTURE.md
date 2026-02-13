# Codebase Structure

**Analysis Date:** 2025-02-13

## Directory Layout

```
get-research-done/
├── agy/                # AGY-specific agent wrappers (generated)
├── codex/              # Codex-specific agent wrappers (generated)
├── scripts/            # Automation scripts for syncing and installation
├── skills/             # Core skill definitions (Source of Truth)
│   ├── _shared/        # Shared skill components
│   └── grd-*/          # Individual skill directories
├── src/                # Python source code
│   └── get_research_done/
│       ├── cli.py      # Installation CLI
│       └── installer.py # Installation logic
├── templates/          # Research artifact templates
├── workflows/          # Research pipeline definitions
├── Makefile            # Developer automation
└── pyproject.toml      # Project configuration and packaging
```

## Directory Purposes

**agy/:**
- Purpose: Contains generated wrappers for the AGY agent platform.
- Contains: `skills/` and `workflows/` mirrored from core assets.

**codex/:**
- Purpose: Contains generated wrappers for the Codex agent platform.
- Contains: `skills/` and `workflows/` mirrored from core assets.

**scripts/:**
- Purpose: Maintenance and synchronization tools.
- Key files: `sync_agy_wrappers.py`, `sync_codex_wrappers.py`, `sync_skill_boilerplate.py`.

**skills/:**
- Purpose: The primary source of truth for agent capabilities.
- Contains: Directories for each skill, containing `SKILL.md` and `SKILL.src.md`.

**src/get_research_done/:**
- Purpose: The core logic for distributing the assets.
- Key files: `installer.py` handles the file copying logic; `cli.py` and `uninstall_cli.py` provide the user interface.

**templates/:**
- Purpose: Standardized Markdown templates for research activities.
- Contains: Files like `state.md`, `lit-review.md`, and `research-notes.md`.

**workflows/:**
- Purpose: High-level research process definitions.
- Key files: `research-pipeline.md`.

## Key File Locations

**Entry Points:**
- `src/get_research_done/cli.py`: Main entry for `grd-install`.
- `src/get_research_done/uninstall_cli.py`: Main entry for `grd-uninstall`.
- `Makefile`: Entry point for developer tasks.

**Configuration:**
- `pyproject.toml`: Defines package metadata, dependencies, and entry points.

**Core Logic:**
- `src/get_research_done/installer.py`: The engine that manages asset deployment.

**Testing:**
- Not detected (No dedicated `tests/` directory found in root, though `gsd-tools.test.js` exists in `.gemini/get-shit-done/bin/` which appears to be a separate or legacy component).

## Naming Conventions

**Files:**
- Skills: `SKILL.md` within a directory named `grd-[skill-name]`.
- Templates: `[kebab-case].md`.
- Scripts: `[snake_case].py`.

**Directories:**
- Skill folders: `grd-[name]`.
- Platform folders: `agy`, `codex`.

## Where to Add New Code

**New Skill:**
- Implementation: Create a new directory in `skills/` (e.g., `skills/grd-new-skill/`) and add `SKILL.md`.
- Sync: Run `make sync-codex` and `make sync-agy` to generate wrappers.

**New Template:**
- Implementation: Add a new `.md` file to `templates/`.

**New Workflow:**
- Implementation: Add a new `.md` file to `workflows/`.

**Installer Logic:**
- Implementation: Modify `src/get_research_done/installer.py`.

## Special Directories

**.grd/:**
- Purpose: Target directory in the user's repository where templates and workflows are installed.
- Generated: Yes (by `grd-install`).
- Committed: No (in this repo), but intended to be committed in the *target* repo.

**agy/ and codex/:**
- Purpose: Contain platform-specific wrappers.
- Generated: Yes (by sync scripts).
- Committed: Yes.

---

*Structure analysis: 2025-02-13*
