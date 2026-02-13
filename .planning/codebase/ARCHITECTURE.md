# Architecture

**Analysis Date:** 2025-02-13

## Pattern Overview

**Overall:** Modular Asset Distribution Architecture

**Key Characteristics:**
- **Decoupled Source of Truth:** Skills, templates, and workflows are maintained in a tool-agnostic format in the project root.
- **Platform-Specific Generation:** Scripts transform core assets into platform-specific wrappers (e.g., Codex, AGY).
- **Multi-Channel Installation:** Assets are deployed to target repositories via a Python CLI (`grd-install`), a Makefile, or a shell script.

## Layers

**Core Assets Layer:**
- Purpose: Tool-agnostic source of truth for research methodologies.
- Location: `skills/`, `templates/`, `workflows/`
- Contains: Markdown-based skill definitions, research artifact templates, and pipeline workflows.
- Depends on: None.
- Used by: Sync scripts, Installer.

**Generation/Wrapper Layer:**
- Purpose: Adapt core assets for specific agent platforms.
- Location: `agy/`, `codex/`
- Contains: Generated wrappers that include platform-specific metadata or formatting.
- Depends on: Core Assets Layer.
- Used by: Sync scripts (to generate), Installer (to deploy).

**Tooling & Automation Layer:**
- Purpose: Automate synchronization and packaging.
- Location: `scripts/`, `Makefile`
- Contains: Python scripts for syncing boilerplate and generating wrappers; Makefile for developer convenience.
- Depends on: Core Assets Layer, Generation Layer.
- Used by: Developers.

**Distribution/Installer Layer:**
- Purpose: Package and install assets into target projects.
- Location: `src/get_research_done/`
- Contains: Python-based installer logic and CLI entry points.
- Depends on: Core Assets Layer.
- Used by: End users.

## Data Flow

**Asset Synchronization Flow:**

1. Developer modifies core skills in `skills/`.
2. Developer runs `make sync-codex` or `make sync-agy`.
3. `scripts/sync_*_wrappers.py` reads core skills and workflows.
4. Wrappers are generated/updated in `codex/` or `agy/`.

**Asset Installation Flow:**

1. User runs `grd-install [dest] --target [target]`.
2. `src/get_research_done/cli.py` parses arguments and calls `install_targets`.
3. `src/get_research_done/installer.py` resolves asset locations (either in-repo or packaged).
4. Assets are copied to target directory structures (e.g., `.grd/`, `.agents/skills/`, `.claude/skills/`).

**State Management:**
- Stateless architecture: The framework provides static assets. State is managed by the external agent system or within the target repository's `.grd/` directory (e.g., `state.md`).

## Key Abstractions

**Skill:**
- Purpose: Defines an agent's role, philosophy, and execution contract.
- Examples: `skills/grd-codebase-mapper/SKILL.md`
- Pattern: Markdown with frontmatter and specific section headers.

**Workflow:**
- Purpose: Orchestrates multiple skills into a research pipeline.
- Examples: `workflows/research-pipeline.md`
- Pattern: Markdown-based procedural guide.

**Template:**
- Purpose: Standardizes research artifacts.
- Examples: `templates/state.md`, `templates/research-notes.md`
- Pattern: Markdown templates with placeholders.

## Entry Points

**CLI - Install:**
- Location: `src/get_research_done/cli.py`
- Triggers: `grd-install` command.
- Responsibilities: Parses user input and installs assets to target directory.

**CLI - Uninstall:**
- Location: `src/get_research_done/uninstall_cli.py`
- Triggers: `grd-uninstall` command.
- Responsibilities: Removes installed assets from target directory.

**Makefile:**
- Location: `Makefile`
- Triggers: `make` commands.
- Responsibilities: Developer-focused automation for syncing and local installation.

## Error Handling

**Strategy:** Fail-fast with informative error messages.

**Patterns:**
- Argument validation in CLI: `parser.error(str(exc))` in `src/get_research_done/cli.py`.
- Asset resolution check: `FileNotFoundError` in `src/get_research_done/installer.py` if assets are missing.

## Cross-Cutting Concerns

**Logging:** Minimal CLI-based status reporting (print statements).
**Validation:** `scripts/sync_skill_boilerplate.py` ensures skills follow a standard structure.
**Deployment:** Packaging via Hatch (`pyproject.toml`) for distribution as a Python package.

---

*Architecture analysis: 2025-02-13*
