# Architecture

**Analysis Date:** 2026-02-10

## Pattern Overview

**Overall:** Skill-based Agent Framework with Dual-Platform Support (Antigravity + Codex)

**Key Characteristics:**
- Skills-as-modules pattern: Each skill encapsulates a single responsibility (hypothesis design, experiment planning, evaluation analysis)
- Dual-platform architecture: Antigravity supports slash commands; Codex uses referenced guidance docs and installed skills
- Workflow pipelines: Sequential research stage progression (Stage -1 → Stage 5) with prescribed outputs at each stage
- Shared boilerplate system: Common XML-based blocks sync across Codex skills via Python utility
- Template-driven documentation: Research notes, W&B config, and skill outputs follow standardized templates

## Layers

**Skill Definition Layer:**
- Purpose: Define Claude AI personas and execution protocols for specialized research tasks
- Location: `codex/skills/*/SKILL.md` and `agy/skills/*/SKILL.md`
- Contains: Role definitions, clarity rules, delivery rules, execution protocols, output formats
- Depends on: Shared boilerplate blocks (`codex/skills/_shared/COMMON_BLOCKS.md`), workflow guidance
- Used by: Codex and Antigravity agents to guide Claude behavior during task execution

**Workflow Guidance Layer:**
- Purpose: Define canonical research pipeline stages and expected outputs
- Location: `codex/workflows/research-pipeline.md`, `agy/workflows/research-pipeline.md`
- Contains: 6 primary stages (with substages in Codex version) describing research progression
- Depends on: Nothing (source of truth)
- Used by: Skills reference these as `@GSD_ROOT@` paths; downstream implementation planning

**Shared Boilerplate Layer:**
- Purpose: Centralize common XML-based protocol blocks for DRY skill definition
- Location: `codex/skills/_shared/COMMON_BLOCKS.md`
- Contains: 7 reusable blocks (context_budget, intent_lock, precision_contract, anti_enterprise, delivery_rule, output_format, action_policy)
- Depends on: Nothing (canonical reference)
- Used by: Codex skill files via sync utility; Codex only (Antigravity skills don't use boilerplate)

**Synchronization Utility Layer:**
- Purpose: Maintain consistency of shared blocks across all Codex skills
- Location: `scripts/sync_skill_boilerplate.py`
- Contains: Python script that parses COMMON_BLOCKS.md, finds insertion points in each skill, updates in-place or validates
- Depends on: COMMON_BLOCKS.md, Python 3.6+
- Used by: `make sync-skills` (updates), `make check-skills` (validates)

**Installation Layer:**
- Purpose: Enable skill and workflow transplantation to target repositories
- Location: `scripts/install.sh` (bash), `scripts/install.ps1` (PowerShell)
- Contains: Directory creation and recursive copy logic for Codex/Antigravity skills
- Depends on: Nothing (self-contained)
- Used by: Users transplanting skills to external projects

## Data Flow

**Skill Execution Flow:**

1. **User Request** → Codex or Antigravity agent receives task
2. **Skill Lookup** → Agent loads SKILL.md for the task domain
3. **Protocol Parsing** → Agent extracts `<role>`, `<clarification_rule>`, `<output_format>`, and other XML tags
4. **Workflow Guidance** → Agent consults referenced `research-pipeline.md` for stage context
5. **Execution** → Agent follows protocol; generates outputs at prescribed paths
6. **Output Validation** → Agent checks output against `<output_format>` specification

**Synchronization Flow:**

1. **Edit COMMON_BLOCKS.md** → User updates shared boilerplate
2. **Run `make sync-skills`** → Python script loads canonical blocks
3. **Parse Skill Files** → Script finds insertion points (after `<source_of_truth>` or `<clarification_rule>`)
4. **In-Place Update** → Script replaces old block with new canonical version
5. **Verification** → Script or user runs `make check-skills` to validate all skills match

**Installation Flow:**

1. **User runs install script** → Provides target repository path
2. **Directory creation** → `.agent/skills/` (Antigravity) or `.codex/skills/` (Codex) created
3. **Recursive copy** → All skills and workflows copied to target
4. **Cross-platform support** → Bash for POSIX, PowerShell for Windows

**State Management:**
- No persistent state in repository; all state created/managed in user's working directory
- Research outputs written to `.grd/` prefix per research-pipeline.md conventions
- Skill definitions are immutable (source of truth); only boilerplate changes

## Key Abstractions

**Skill:**
- Purpose: Encapsulates a reusable Claude AI behavior for one research domain
- Examples: `grd-hypothesis-designer`, `grd-experiment-planner`, `research-notes-tracker`
- Pattern: YAML frontmatter + XML-tagged protocol blocks + markdown narrative
- Scope: Single responsibility (design, plan, execute, analyze, or track)

**Workflow Pipeline:**
- Purpose: Describe sequential research progression from concept to publication
- Examples: `codex/workflows/research-pipeline.md` (11 stages), `agy/workflows/research-pipeline.md` (9 stages)
- Pattern: Numbered stages with purpose, constraints, and prescribed output paths
- Scope: Full research lifecycle

**Boilerplate Block:**
- Purpose: Standardize common protocol across all skills (context budgets, clarity rules, etc.)
- Examples: `<intent_lock>`, `<precision_contract>`, `<action_policy>`
- Pattern: XML-tagged markdown blocks in COMMON_BLOCKS.md, synced to skill files
- Scope: Codex skills only; Antigravity defines boilerplate inline

**Research Output Artifact:**
- Purpose: Standardized documentation at each pipeline stage
- Examples: `HYPOTHESIS.md`, `EXPERIMENT_PLAN.md`, `EVALUATION.md`, `REPRODUCIBILITY.md`
- Pattern: Markdown files with prescribed sections (assumptions, plan, artifacts, verification, risks)
- Scope: Research working directory (`.grd/`, user-defined prefix)

## Entry Points

**Codex Entry Points:**
- Location: `.codex/skills/grd-*/SKILL.md` (user's target repository)
- Triggers: User invokes Codex skill in chat
- Responsibilities: Load SKILL.md, extract protocol, execute research task, output artifacts

**Antigravity Entry Points:**
- Location: `.agent/skills/research-*/SKILL.md` (user's target repository)
- Triggers: User types `/command-name` in Antigravity chat
- Responsibilities: Slash command routing, skill execution, artifact generation

**Installation Entry Point:**
- Location: `scripts/install.sh` or `scripts/install.ps1` (get-research-done repo)
- Triggers: `bash scripts/install.sh /path/to/target` or PowerShell equivalent
- Responsibilities: Create skill directories, copy all skills/workflows, verify structure

**Synchronization Entry Point:**
- Location: `scripts/sync_skill_boilerplate.py` (get-research-done repo)
- Triggers: `make sync-skills` or `python3 scripts/sync_skill_boilerplate.py --fix`
- Responsibilities: Load COMMON_BLOCKS.md, update all Codex skill files in-place, report changes

## Error Handling

**Strategy:** Prescriptive protocols prevent ambiguity; XML tags enforce clarity before execution.

**Patterns:**
- **Intent Clarification**: `<intent_lock>` forces pause before MED/HIGH complexity tasks; asks focused question
- **Scope Validation**: `<context_budget>` limits file reads; prevents out-of-scope exploration
- **Output Specification**: `<output_format>` prescribes exact structure; enables downstream consumption
- **Action Policy**: `<action_policy>` separates LOW (propose) from MED/HIGH (pause + confirm) actions
- **Precision Contract**: `<precision_contract>` requires exact file paths, not vague references

## Cross-Cutting Concerns

**Workflow Alignment:** Every skill includes `<source_of_truth>` pointing to corresponding pipeline stage. Codex version includes fine-grained stages (0.5, 1.5, 2.5, 3.5, 4.5); Antigravity simplifies to primary stages.

**Anti-Enterprise Values:** All skills include `<anti_enterprise>` block excluding team coordination, sprint ceremonies, stakeholder management, and ceremonial documentation. These are non-negotiable boundaries.

**Boilerplate Consistency (Codex):** Python sync utility ensures all 12 Codex skills maintain identical context_budget, intent_lock, precision_contract, anti_enterprise, delivery_rule, output_format, and action_policy blocks. Tag mismatch detected at check-time.

**Portability:** Skills and workflows designed for zero-assumption transplantation. Installation scripts create minimal directory structure; skills reference workflows via `@GSD_ROOT@` paths (adjusted during transplant).

**Evidence-Based Documentation:** All skill output formats require (1) Assumptions, (2) Plan (numbered steps), (3) Proposed Changes/Artifacts, (4) Verification Steps, (5) Risks and Failure Modes. This ensures downstream consumers have evidence trail.

---

*Architecture analysis: 2026-02-10*
