# Roadmap: Get Research Done (GRD)

## Overview

Transform the current ad-hoc research loop into a systematic two-gear system (Explore and Confirm) with persistent state tracking in `.grd/`. This roadmap builds on existing Codex skills to provide an orchestrated workflow that prevents context loss and guides researchers from initial exploration to formal results.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: Foundation & State** - Establish the `.grd/` persistence layer and orchestration framework.
- [ ] **Phase 2: Explore Mode & Journal** - Enable lightweight experiment logging and long-term knowledge accumulation.
- [ ] **Phase 3: Transition & Rigor** - Implement the promotion mechanism from exploration to formal pipeline and guided workflow.

## Phase Details

### Phase 1: Foundation & State
**Goal**: Establish the `.grd/` state layer and orchestration framework so skills can share context.
**Depends on**: Nothing (first phase)
**Requirements**: [STATE-01, ORCH-01, SKILLS-01, SKILLS-02]
**Success Criteria** (what must be TRUE):
  1. `.grd/` directory is automatically initialized and used by skills for persistence.
  2. Orchestration layer can invoke a Codex skill with relevant state context injected.
  3. Core existing skills are refactored to read/write from the `.grd/` state layer.
**Plans**: 3 plans

Plans:
- [ ] 01-01: Implement persistent state layer (`.grd/` management)
- [ ] 01-02: Build orchestration framework and state-aware skill invocation
- [ ] 01-03: Refactor core skills for state and orchestration integration

### Phase 2: Explore Mode & Journal
**Goal**: Enable lightweight experiment logging and persistent research notes.
**Depends on**: Phase 1
**Requirements**: [EXPLORE-01, EXPLORE-02, STATE-02]
**Success Criteria** (what must be TRUE):
  1. User can initiate an "explore" session with automatic lightweight tracking enabled.
  2. Experiment logs capturing "what/happened/why" are automatically generated in `.grd/`.
  3. Research journal accumulates findings across multiple sessions as a single source of truth.
**Plans**: 2 plans

Plans:
- [ ] 02-01: Implement Explore-mode and experiment logging mechanism
- [ ] 02-02: Develop the persistent Research Journal system

### Phase 3: Transition & Rigor
**Goal**: Implement the promotion mechanism from exploration to formal pipeline and guided workflow.
**Depends on**: Phase 2
**Requirements**: [CONFIRM-01, TRANS-01, ORCH-02]
**Success Criteria** (what must be TRUE):
  1. User can bootstrap a formal hypothesis (Stage 0) directly from exploration notes.
  2. Confirm-mode enforces the full research pipeline (Stages -1 to 5) rigor.
  3. System provides intelligent "what to do next" guidance based on current `.grd/` state.
**Plans**: 2 plans

Plans:
- [ ] 03-01: Build transition mechanism (explore → confirm) and Confirm-mode rigor
- [ ] 03-02: Implement workflow guidance commands

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & State | 0/3 | Not started | - |
| 2. Explore Mode & Journal | 0/2 | Not started | - |
| 3. Transition & Rigor | 0/2 | Not started | - |
