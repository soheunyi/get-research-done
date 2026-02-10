# Technology Stack

**Analysis Date:** 2026-02-10

## Languages

**Primary:**
- Python 3 - Core scripting language for skill orchestration and utilities
- Markdown - Documentation and skill definitions across Codex and Antigravity systems

**Configuration:**
- YAML - Workflow and configuration metadata (embedded in markdown frontmatter)

## Runtime

**Environment:**
- Python 3.x (3.7+ implied by f-strings and pathlib usage in `scripts/sync_skill_boilerplate.py`)
- CLI/Shell (Bash/PowerShell for installation and make targets)

**Package Manager:**
- pip (Python dependencies installed via standard mechanisms)
- Makefile (Task automation, see `Makefile`)
- Lockfile: Not detected (no requirements.txt, Pipfile, or poetry.lock)

## Frameworks

**Core:**
- Antigravity - Research workflow orchestration framework for slash commands (`.agent/skills/` integration)
- Codex - Research skill system for Claude-based research workflows (`.codex/skills/` integration)

**Research Utilities:**
- Weights & Biases (W&B) - Experiment tracking and metadata management
  - Purpose: Run lineage, metric comparison, artifact traceability
  - Integration: Optional W&B integrator skill (`agy/skills/research-wandb-integrator/`)
  - Auth: `WANDB_API_KEY` environment variable (secrets not hardcoded)

**Build/Dev:**
- Python standard library (pathlib, argparse, re, sys) - Used in `scripts/sync_skill_boilerplate.py`

## Key Dependencies

**Critical:**
- Python stdlib: pathlib, re, argparse - Core utilities for skill synchronization
- Weights & Biases SDK (optional) - Experiment tracking integration
  - Package: `wandb`
  - Why it matters: Enables run reproducibility, metric comparisons, and artifact versioning

**Infrastructure:**
- Git - Version control (`.git/` directory present)
- Make - Task automation (build/test/deployment commands)

## Configuration

**Environment:**
- Python path: System Python 3.x (invoked via `python3` in Makefile)
- W&B configuration: `WANDB_API_KEY` via environment variables only (no hardcoded credentials)
- Project structure conventions: `.agent/` for Antigravity, `.codex/` for Codex skill installation

**Build:**
- `Makefile`: Task orchestration
  - `make sync-skills` - Syncs shared skill boilerplate across codex skills
  - `make check-skills` - Validates skill boilerplate consistency
- `scripts/sync_skill_boilerplate.py` - Python script for synchronizing shared blocks across SKILL.md files

**Skill Configuration:**
- Shared blocks defined in: `codex/skills/_shared/COMMON_BLOCKS.md`
- Blocks sync to all skill files in: `codex/skills/*/SKILL.md`
- Required YAML metadata in skills: name, description (in frontmatter)

## Platform Requirements

**Development:**
- Python 3.7+ (or higher for f-string support)
- macOS/Linux/Windows compatible (shell install scripts provided)
- Git for version control
- Make for task automation

**Production:**
- Deployment target: Antigravity framework (`.agent/skills/`) or Codex system (`.codex/skills/`)
- W&B account optional (for experiment tracking workflows)
- No external database or server required - purely documentation and configuration system

## Documentation & Configuration Files

**Key Paths:**
- `codex/workflows/research-pipeline.md` - Codex research workflow guidance
- `agy/workflows/research-pipeline.md` - Antigravity research workflow guidance
- `codex/skills/_shared/COMMON_BLOCKS.md` - Shared skill boilerplate (source of truth)
- `templates/wandb-config.md` - W&B configuration template
- `templates/research-notes.md` - Research notes template

## Workflow Output Targets

The stack supports generation of standardized research documentation:
- `.grd/codebase/CURRENT.md`, `TARGET.md`, `GAPS.md` - Codebase mapping outputs
- `.grd/research/phases/{phase_id}-RESEARCH.md` - Phase research outputs
- `HYPOTHESIS.md`, `EXPERIMENT_PLAN.md`, `ANALYSIS_PLAN.md` - Research planning documents
- `WANDB_CONFIG.md` - Experiment tracking configuration
- `EVALUATION.md`, `ABLATION.md`, `REPRODUCIBILITY.md` - Research analysis documents

---

*Stack analysis: 2026-02-10*
