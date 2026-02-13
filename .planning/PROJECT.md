# Get Research Done (GRD)

## What This Is

A research utility suite for ML/AI work that preserves state across sessions and keeps the solo research loop fast.

## Core Value

Researchers focus on the what and why while GRD keeps context, evidence, and next-step guidance coherent.

## Current State

- Shipped milestone: `v1.0 MVP` on 2026-02-13.
- Completed phases: Foundation & Utility, Explore Mode & Journaling, Promotion & Guidance.
- Runtime loop available: `grd log`, `grd next`, `grd promote`.

## Next Milestone Goals

- Unified hypothesis display format across promotion artifacts and CLI views.
- Improve milestone/stat tracking quality in planning summaries.
- Start v1.1 scope definition with fresh requirements.

## Constraints

- Markdown-first persistence in `.grd/`.
- Lightweight CLI ergonomics prioritized over process-heavy orchestration.
- User remains orchestrator; tooling remains assistive.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| User-led orchestration | Research requires high-level human judgment | ✓ Active |
| Markdown state files | Git-friendly, transparent, LLM-readable | ✓ Active |
| Explore -> Promote progression | Keeps solo flow fast while enabling rigor on demand | ✓ Active |

---
*Last updated: 2026-02-13 after v1.0 milestone*
