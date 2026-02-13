# Roadmap: Get Research Done (GRD)

## Overview

Build a suite of utilities that reduce research overhead by managing persistent state in `.grd/`. The goal is to provide a "context-aware toolkit" that researchers use to run experiments without losing knowledge between sessions.

## Phases

- [ ] **Phase 1: Foundation & Utility** - Establish the `.grd/` state layer and the CLI utility for state-aware skill invocation.
- [ ] **Phase 2: Explore Mode & Journaling** - Implement lightweight experiment logging and long-term knowledge accumulation.
- [ ] **Phase 3: Promotion & Guidance** - Build tools to promote exploration to formal evidence and provide state-based next-step guidance.

## Phase Details

### Phase 1: Foundation & Utility
**Goal**: Build the core `.grd/` persistence layer and the helper to inject this state into Codex skills.
**Requirements**: [STATE-01, STATE-03, UTIL-01, SKILLS-01, SKILLS-02]
**Success Criteria**:
  1. `.grd/` directory is managed and structured.
  2. CLI can successfully prepended `.grd/` state to Codex skill prompts.
  3. Core skills are refactored to read from this shared state.

### Phase 2: Explore Mode & Journaling
**Goal**: Enable easy logging of "loose" exploration and accumulate it in a persistent journal.
**Requirements**: [STATE-02, UTIL-02]
**Success Criteria**:
  1. Researchers can log experiments with minimal friction ("what/happened/why").
  2. The Research Journal accurately reflects findings across multiple sessions.

### Phase 3: Promotion & Guidance
**Goal**: Support the transition from exploration to rigor and offer simple state-based guidance.
**Requirements**: [UTIL-03]
**Success Criteria**:
  1. Exploration notes can be used to bootstrap formal hypothesis stages.
  2. The tool can suggest which skill might be useful next based on current `.grd/` state.

## Progress

| Phase | Status | Completed |
|-------|--------|-----------|
| 1. Foundation & Utility | Not started | - |
| 2. Explore Mode & Journaling | Not started | - |
| 3. Promotion & Guidance | Not started | - |
