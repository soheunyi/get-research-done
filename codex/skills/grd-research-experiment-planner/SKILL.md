---
name: "GRD Experiment Planner"
description: "Plan reproducible experiments with pre-committed analysis design, controls, seeds, splits, and statistical protocol"
---

# Codex GRD Skill: grd-research-experiment-planner

<when_to_use>
Use after hypothesis design and before running experiments, including pre-committed analysis planning.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` Stage 1.5 and Stage 2.
When requested, produce `.grd/research/ANALYSIS_PLAN.md` and `.grd/research/EXPERIMENT_PLAN.md`.
</source_of_truth>

<clarification_rule>
Before any complex task, first ask for the user perspective, constraints, and preferred direction.
If intent remains unclear, pause and ask for pseudocode or a concrete step-by-step outline before continuing.
</clarification_rule>

<delivery_rule>
Default to concise chat output.

- If user explicitly asks for a saved deliverable: write or update artifact files.
- Otherwise: provide a proposed diff outline (files plus key edits) and verification steps.
</delivery_rule>

<output_format>
Always structure the response as:

1) Assumptions (bullet list; call out unknowns)
2) Plan (numbered; smallest-first)
3) Proposed changes / artifacts
   - If user did NOT ask to write files: provide a proposed diff outline plus filenames
   - If user DID ask to write files: write or update artifact files named in <source_of_truth>
4) Verification steps (how to check it worked)
5) Risks and failure modes (brief; include data leakage and confounds when relevant)
</output_format>

<action_policy>
Default: propose actions; do not execute side-effecting steps unless user explicitly asks.
Guardrail: for MED or HIGH complexity tasks, pause and ask for the user perspective before proceeding.

Risk tiers:
- LOW: summarize, plan, draft text, propose diffs, read-only inspection.
- MED: modify code or configs, run tests or training scripts, change evaluation protocol.
- HIGH: delete or overwrite data, touch secrets or credentials, publish externally, deploy, spend money or credits.

Contract:
1) Ask for user thoughts before starting any MED or HIGH complexity task and confirm the preferred direction.
2) List Proposed Actions (files, commands, external calls).
3) Label each action LOW, MED, or HIGH plus rollback plan.
4) Require explicit user approval for MED and HIGH actions.
</action_policy>

<execution_contract>
1. Define primary and secondary endpoints, estimator, and decision thresholds.
2. Define seed aggregation, CI method, significance tests, and multiple comparisons handling when needed.
3. Define strict no test peeking and leakage checklist.
4. Define control and treatment matrix.
5. Define dataset versions, seeds, split strategy, and run budget.
6. Produce `.grd/research/ANALYSIS_PLAN.md` and `.grd/research/EXPERIMENT_PLAN.md` when artifact output is requested.
</execution_contract>
