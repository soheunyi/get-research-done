# Technology Stack

**Analysis Date:** 2025-01-24

## Languages

**Primary:**
- Python 3.9+ - Core CLI logic (`src/get_research_done/`), installation scripts, and skill sync utilities (`scripts/`).

**Secondary:**
- JavaScript (Node.js) - GSD (Get Shit Done) framework tools (`.gemini/get-shit-done/bin/gsd-tools.js`).
- Shell (Bash/PowerShell) - Installation scripts (`scripts/install.sh`, `scripts/install.ps1`).
- Markdown - All "skills", templates, and workflows are defined in Markdown (`skills/`, `templates/`, `workflows/`).

## Runtime

**Environment:**
- Python 3.9+
- Node.js (required for GSD tools in `.gemini/`)

**Package Manager:**
- Python `pip` / `hatch` - Project uses `pyproject.toml` for packaging.
- Lockfile: None detected in root (typical for library/template repos).

## Frameworks

**Core:**
- GSD (Get Shit Done) Framework - Used for workflow management, project initialization, and phase execution.
- Hatchling - Build backend for the Python package.

**Testing:**
- Not detected (no dedicated testing framework or `tests/` directory found in root).

**Build/Dev:**
- Hatch - Used for building the wheel and sdist.
- Makefile - Orchestrates skill syncing and local installation targets.

## Key Dependencies

**Critical:**
- `hatchling` >= 1.21 - Build system defined in `pyproject.toml`.
- `importlib.resources` - Used in `src/get_research_done/installer.py` to manage packaged assets.

**Infrastructure:**
- Git - Heavily integrated via `gsd-tools.js` for project state tracking and commits.

## Configuration

**Environment:**
- `.planning/config.json` - GSD project-level configuration (generated during `new-project` workflow).
- `.env` files - Supported by GSD framework for external service keys (not used by the core `get-research-done` tool itself).

**Build:**
- `pyproject.toml` - Main project configuration and build definitions.
- `Makefile` - Developer task orchestration.

## Platform Requirements

**Development:**
- Cross-platform (macOS/Linux/Windows) with Python and Node.js.

**Production:**
- Distributed as a Python package.
- Supports installation into target repositories using various agent environments (`.agents`, `.claude`, `.opencode`, `.gemini`).

---

*Stack analysis: 2025-01-24*
