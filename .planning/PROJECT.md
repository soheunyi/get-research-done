# Get Research Done (GRD)

## What This Is

A research utility suite for ML/AI research, built as Codex skills. It is a **"collection of tools to reduce annoyance"** in the research loop. Instead of a rigid automated orchestrator, it provides a persistent state layer (`.grd/`) and utilities that help the researcher maintain context across experiments without manual overhead.

## Core Value

Researchers focus on the "what" and "why" while the tool handles the "where" and "how" of context retention. It reduces the friction of logging experiments, tracking hypotheses, and preparing evidence for results.

## Requirements

### Validated

- ✓ Individual Codex skills for research tasks (hypothesis design, experiment planning, etc.) — existing
- ✓ Research pipeline definition (Stage -1 through Stage 5) — existing
- ✓ Shared boilerplate system for skill consistency — existing
- ✓ Cross-platform install scripts (Bash/PowerShell) — existing
- ✓ Boilerplate sync utility (`sync_skill_boilerplate.py`) — existing

### Active

- [ ] **State-Aware CLI**: A utility to invoke Codex skills with automatic `.grd/` context injection
- [ ] **Persistent State Layer**: Structured `.grd/` directory for experiment logs, state, and notes
- [ ] **Research Journal**: A single file that accumulates findings across sessions to prevent context loss
- [ ] **Explore-mode Logging**: Lightweight tracking of "what was tried and why" during exploration
- [ ] **Refactor Existing Skills**: Update 12+ skills to read/write from the common `.grd/` layer
- [ ] **Evidence Promotion**: Easy transition from loose exploration notes to formal pipeline stages

### Out of Scope

- Autonomous agent-driven orchestration — User is the orchestrator
- Production MLOps/Deployment tooling
- Multi-user collaboration
- Real-time experiment monitoring

## Context

- **Execution model**: User orchestrates the workflow, using GRD utilities to invoke skills, run training, and capture results.
- **Current pain**: Manual tracking is tedious; context is lost between sessions; repeating failed experiments.
- **State convention**: Research outputs written to `.grd/` prefix in target repositories.
- **Inspiration**: A lightweight version of `gsd` focused on research utility rather than complex task management.

## Constraints

- **Platform**: OpenAI Codex (cloud-based, stateless per task).
- **Format**: Markdown files in `.grd/` (human/agent readable, git-trackable).
- **Execution**: Must handle the handoff between local orchestration and remote GPU execution.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| User-led Orchestration | Research requires high-level human intuition; tools should assist, not lead | ✓ Fixed |
| Markdown State Files | Git-friendly, no DB required, easy for LLMs to parse | ✓ Fixed |
| Two-gear system (Explore/Confirm) | Matches natural research flow (loose ideation followed by rigorous proof) | ✓ Active |

---
*Last updated: 2026-02-13*
