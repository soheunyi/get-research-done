# AGENTS.md — GSD Operating Contract

This repository uses the **Get Shit Done (GSD)** framework with a Codex-native mirror under:
- `.agents/commands/gsd/`
- `.agents/get-shit-done/workflows/`
- `.agents/agents/`

Use `.agents/*` as the **primary** source of truth for `/gsd:*` requests.
Use `.gemini/*` only as fallback if a required file is missing from `.agents/*`.

## Command Resolution

When user requests `/gsd:<name> [args]`:

1. Open `.agents/commands/gsd/<name>.toml`.
2. If missing, open `.gemini/commands/gsd/<name>.toml`.
3. Read its `prompt`, `execution_context`, and `process` sections.
4. Open referenced workflow files under `.agents/get-shit-done/workflows/` (fallback `.gemini/get-shit-done/workflows/`).
5. Execute the workflow steps directly in this repo (do not hand-wave).

If a command file is missing, report that clearly and stop.

## Execution Rules

1. Prefer local execution through repo scripts and files.
2. Use `node ./.agents/get-shit-done/bin/gsd-tools.js ...` whenever the workflow specifies it (fallback: `.gemini/...` if needed).
3. Create/update artifacts in `.planning/` exactly where the workflow expects.
4. Preserve phase continuity:
   - discuss-phase -> CONTEXT.md
   - plan-phase -> RESEARCH.md + *-PLAN.md
   - execute-phase -> *-SUMMARY.md + *-VERIFICATION.md + roadmap/state updates
5. Run verification commands listed in plans/workflows and report real results.

## Phase Workflow (Default)

For milestone phases, follow this sequence unless user asks otherwise:

1. `/gsd:discuss-phase <N>`
2. `/gsd:plan-phase <N>`
3. `/gsd:execute-phase <N>`
4. `/gsd:verify-work <N>` (or phase verification path in workflow)

## Context Fidelity

When `*-CONTEXT.md` exists, treat its `Implementation Decisions` as locked:

1. Implement locked decisions exactly.
2. Keep deferred ideas out of current phase scope.
3. Use "Claude's Discretion" areas for technical choices only.

## Git + Commit Behavior

1. Do not revert unrelated local changes.
2. Commit only files relevant to the requested GSD step.
3. Make atomic commits: one logical change per commit.
4. Use workflow-style commit messages (e.g., `docs(04): ...`, `feat(03): ...`).

## Repo-Specific Notes

1. Prefer `.agents/*` for command/workflow execution in Codex sessions.
2. `.gemini/*` may still contain tracked framework files; use as fallback only.
3. Keep command behavior compatible with existing `scout` CLI conventions.
