# External Integrations

**Analysis Date:** 2025-01-24

## APIs & External Services

**AI Agent Platforms (Installation Targets):**
- **Codex (ChatGPT)** - Targets `.agents/skills`
- **Claude** - Targets `.claude/skills`
- **OpenCode** - Targets `.opencode/skills`
- **Gemini** - Targets `.gemini/skills`
- The core tool `grd-install` (`src/get_research_done/installer.py`) manages deploying assets to these platforms.

**Research & Experimentation:**
- **Weights & Biases (W&B)** - Integrated via templates (`templates/wandb-config.md`) for experiment tracking in research workflows.

## Data Storage

**Databases:**
- **Local Filesystem** - The primary "database" for GSD project state, using files in `.planning/` (e.g., `STATE.md`, `ROADMAP.md`).

**File Storage:**
- **Local Filesystem** - Assets (skills, templates, workflows) are stored locally and copied to target repositories.

## Authentication & Identity

**Auth Provider:**
- **Git/GitHub** - Authentication is handled via local git configuration or environment variables (e.g., `GITHUB_TOKEN`) for repo operations performed by `gsd-tools.js`.

## Monitoring & Observability

**Error Tracking:**
- **None** - Core tool relies on standard error output.

**Logs:**
- **Git History** - GSD framework uses git commits as a primary log of project progress and task completion.

## CI/CD & Deployment

**Hosting:**
- **GitHub** - Source code and distribution (via `pip` install from git).

**CI Pipeline:**
- **None detected** - No `.github/workflows` or similar config found in root.

## Environment Configuration

**Required env vars:**
- None for core installation.
- GSD workflows may require various keys (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) depending on the agents used in the target repository.

**Secrets location:**
- `.env` files (gitignored) - GSD framework standard for storing local secrets.

## Webhooks & Callbacks

**Incoming:**
- **None** - The tool is a CLI and does not listen for webhooks.

**Outgoing:**
- **None** - No outgoing webhooks detected in the core logic.

---

*Integration audit: 2025-01-24*
