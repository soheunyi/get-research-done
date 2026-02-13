# Requirements

## V1: Core Orchestration & State

### Orchestration (ORCH)
- **ORCH-01**: Orchestration layer that connects skills into a coherent workflow.
- **ORCH-02**: Workflow commands/skills that guide "what to do next" based on current state.

### Persistent State (STATE)
- **STATE-01**: Persistent state layer (`.grd/`) that Codex skills read and write automatically.
- **STATE-02**: Research journal that accumulates across sessions (prevents re-running forgotten experiments).

### Explore Mode (EXPLORE)
- **EXPLORE-01**: Two-gear system: explore mode implementation (lightweight tracking).
- **EXPLORE-02**: Explore-mode experiment log: what was tried, what happened, why moved on.

### Confirm & Transition (CONFIRM)
- **CONFIRM-01**: Two-gear system: confirm mode implementation (full rigor pipeline).
- **TRANS-01**: Transition mechanism from explore → confirm (bootstrap hypothesis from exploration notes).

### Skill Integration (SKILLS)
- **SKILLS-01**: State-aware skill invocation: each Codex task gets relevant context automatically.
- **SKILLS-02**: Refactor existing skills to integrate with orchestration and state layer.

## Traceability

| ID | Phase | Status |
|----|-------|--------|
| ORCH-01 | Phase 1 | Pending |
| ORCH-02 | Phase 3 | Pending |
| STATE-01 | Phase 1 | Pending |
| STATE-02 | Phase 2 | Pending |
| EXPLORE-01 | Phase 2 | Pending |
| EXPLORE-02 | Phase 2 | Pending |
| CONFIRM-01 | Phase 3 | Pending |
| TRANS-01 | Phase 3 | Pending |
| SKILLS-01 | Phase 1 | Pending |
| SKILLS-02 | Phase 1 | Pending |
