# Get Research Done (GRD)

## What This Is

A structured workflow system for ML/AI research, built as Codex skills. It turns an ad-hoc research loop (brainstorm → code → check results → repeat) into a two-gear system with persistent state: **explore** freely, then **confirm** rigorously — with everything tracked so nothing gets lost between sessions.

## Core Value

Researchers never lose context between experiments. Every exploration is logged, every result is traceable, and transitioning from "interesting finding" to "paper-ready evidence" is a guided path — not a fresh start.

## Requirements

### Validated

- ✓ Individual Codex skills for research tasks (hypothesis design, experiment planning, evaluation analysis, etc.) — existing
- ✓ Research pipeline definition (Stage -1 through Stage 5) — existing
- ✓ Shared boilerplate system for skill consistency — existing
- ✓ Cross-platform install scripts (Bash/PowerShell) — existing
- ✓ Boilerplate sync utility (`sync_skill_boilerplate.py`) — existing

### Active

- [ ] Orchestration layer that connects skills into a coherent workflow
- [ ] Two-gear system: explore mode (lightweight tracking) and confirm mode (full rigor pipeline)
- [ ] Persistent state layer (`.grd/`) that Codex skills read and write automatically
- [ ] Explore-mode experiment log: what was tried, what happened, why moved on
- [ ] Transition mechanism from explore → confirm (bootstrap hypothesis from exploration notes)
- [ ] State-aware skill invocation: each Codex task gets relevant context automatically
- [ ] Research journal that accumulates across sessions (prevents re-running forgotten experiments)
- [ ] Workflow commands/skills that guide "what to do next" based on current state
- [ ] Refactor existing skills to integrate with orchestration and state layer

### Out of Scope

- Production deployment tooling — this is research infrastructure, not MLOps
- Multi-user collaboration features — single researcher workflow (1-2 focused threads)
- Custom UI/dashboard — all interaction through Codex skills and markdown files
- Real-time experiment monitoring — async check-results pattern is fine
- Antigravity platform parity — focus on Codex; Antigravity skills exist but are not the priority

## Context

- **Execution model**: User brainstorms ideas, delegates implementation to OpenAI Codex (cloud agent), runs training on remote GPU, checks results, iterates
- **Current pain**: Context loss between sessions — forgetting what was tried, re-implementing experiments, no systematic accumulation of knowledge
- **Research style**: 1-2 focused threads at a time, exploratory at first, then formalizing for paper-ready results
- **Existing assets**: 12 Codex skills, research pipeline (Stages -1 to 5), shared boilerplate system, install/sync tooling
- **State convention**: Research outputs written to `.grd/` prefix in target repositories
- **Inspiration**: `~/get-shit-done` (GSD) workflow — structured commands, persistent state, clear progression

## Constraints

- **Platform**: OpenAI Codex — skills must be self-contained, each task starts with fresh context
- **Execution**: Codex writes code, user runs training on remote GPU — workflow must handle this handoff
- **State format**: Markdown files in `.grd/` — must be readable by both humans and Codex agents
- **Compatibility**: Build on existing 12 skills, don't break current install/sync infrastructure
- **Scope**: Solo researcher, not team workflow

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Two-gear system (explore/confirm) | Research is naturally loose-then-strict; forcing rigor too early kills exploration | — Pending |
| Build on existing skills | 12 skills already work individually; need orchestration, not replacement | — Pending |
| Codex-first (not Antigravity) | User's primary platform is Codex; Antigravity is secondary | — Pending |
| Markdown state files in `.grd/` | Human-readable, Codex-readable, git-trackable, no infrastructure needed | — Pending |

---
*Last updated: 2026-02-10 after initialization*
