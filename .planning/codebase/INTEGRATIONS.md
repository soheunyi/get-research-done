# External Integrations

**Analysis Date:** 2026-02-10

## APIs & External Services

**Experiment Tracking:**
- Weights & Biases (W&B) - Optional experiment tracking and artifact management
  - SDK/Client: `wandb` Python package
  - Auth: `WANDB_API_KEY` environment variable
  - Purpose: Run metadata, metric logging, artifact versioning, model checkpoint storage
  - Integration Skill: `agy/skills/research-wandb-integrator/`

## Data Storage

**Databases:**
- Not detected - This is a documentation and configuration system, not a data application

**File Storage:**
- Local filesystem only
  - Research artifacts stored locally: `EXPERIMENT_PLAN.md`, `EVALUATION.md`, `REPRODUCIBILITY.md`
  - Output paths: `.grd/codebase/`, `.grd/research/phases/`

**Caching:**
- None detected

## Authentication & Identity

**Auth Provider:**
- Custom: W&B API key authentication via environment variable
  - Implementation: `WANDB_API_KEY` passed to wandb SDK
  - Guardrail: Never commit credentials; environment variable only
  - Reference: `agy/skills/research-wandb-integrator/SKILL.md` line 42

## Monitoring & Observability

**Error Tracking:**
- None detected - No external error tracking service integrated

**Logs:**
- Standard output only
  - Python scripts log to console via argparse and print statements
  - W&B logs optional: integration skill handles W&B logging configuration

## CI/CD & Deployment

**Hosting:**
- Portable system: No centralized hosting
  - Designed for transplant into target repositories
  - Antigravity: Copy to `.agent/skills/` in target repo
  - Codex: Copy to `.codex/skills/` in target repo

**CI Pipeline:**
- Local validation only:
  - `make check-skills` - Validates skill boilerplate consistency against `COMMON_BLOCKS.md`
  - `scripts/sync_skill_boilerplate.py --check` - Same validation

**Installation Scripts:**
- `scripts/install.sh` - Bash installation for macOS/Linux
- `scripts/install.ps1` - PowerShell installation for Windows
- Target: Copies skills to `.agent/skills/` (Antigravity) or `.codex/skills/` (Codex) in target repo

## Environment Configuration

**Required env vars:**
- `WANDB_API_KEY` - Weights & Biases API key (only if using W&B integration)
- `PYTHON` - Python executable path (optional, defaults to `python3` in Makefile)

**Secrets location:**
- Environment variables only
- Never hardcoded in configuration files
- W&B integration explicitly guardrails against logging secrets (line 42 in research-wandb-integrator SKILL.md)

## Webhooks & Callbacks

**Incoming:**
- None detected

**Outgoing:**
- W&B API calls (optional): Run creation, metric logging, artifact upload
  - Only when user explicitly enables W&B integration skill
  - Non-blocking: Offline mode supported with later sync

## Workflow Integration Points

**Codex Integration:**
- Research pipeline reference: `codex/workflows/research-pipeline.md`
- Skill location: `codex/skills/{skill-name}/SKILL.md`
- Shared boilerplate: `codex/skills/_shared/COMMON_BLOCKS.md` (synced to all skills)

**Antigravity Integration:**
- Research pipeline reference: `agy/workflows/research-pipeline.md`
- Skill location: `agy/skills/{skill-name}/`
- Slash command support: `/grd-*` commands from workflow assets

## Research Artifact Dependencies

**Workflow Stage Outputs:**

| Stage | Output File | External Dependency |
|-------|------------|-------------------|
| -1 | `.grd/codebase/CURRENT.md`, `TARGET.md`, `GAPS.md` | None (codebase mapping) |
| 0 | `RESEARCH_NOTES.md` | None (local documentation) |
| 0.5 | `.grd/research/phases/{phase_id}-RESEARCH.md` | None (execution guidance) |
| 1 | `HYPOTHESIS.md` | None (research planning) |
| 1.5 | `ANALYSIS_PLAN.md` | None (statistical planning) |
| 2 | `EXPERIMENT_PLAN.md` | None (experiment design) |
| 2.5 | `WANDB_CONFIG.md` | W&B (optional) |
| 3 | `EVALUATION.md` | None (result analysis) |
| 3.5 | `ERROR_ANALYSIS.md` | None (analysis) |
| 4 | `ABLATION.md` | None (robustness testing) |
| 4.5 | `NUMERICS_AUDIT.md`, `RANDOMNESS_AUDIT.md` | None (determinism audit) |
| 5 | `REPRODUCIBILITY.md`, `RESEARCH_SUMMARY.md` | None (final documentation) |

## Framework Transplant Targets

**Installation paths for target repositories:**

**Antigravity:**
- Skills destination: `/path/to/target-repo/.agent/skills/`
- Workflows destination: `/path/to/target-repo/get-research-done/agy/`
- Integration: Slash commands (`/grd-*`) become available

**Codex:**
- Skills destination: `/path/to/target-repo/.codex/skills/`
- Workflows destination: `/path/to/target-repo/get-research-done/codex/`
- Integration: Skills referenced in Claude planning and execution

---

*Integration audit: 2026-02-10*
