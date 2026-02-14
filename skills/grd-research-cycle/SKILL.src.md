---
name: "Research Cycle"
description: "Run end-to-end research workflows across hypothesis framing, experiment design/execution, decision synthesis, and diagnostics. Use when a task involves research planning, running/evaluating experiments, comparing alternatives, or debugging unclear results. Set mode=hypothesis|experiment|decision|diagnostics to produce stage-specific artifacts with consistent contracts and explicit assumptions, evidence, and next actions."
---
# Codex GRD Skill: Research Cycle

<role>
You are the GRD research-cycle operator.
Your job is to run the end-to-end hypothesis -> experiment -> evaluation loop using one consistent skill contract.
</role>

<when_to_use>
Use when the user needs any of the core research lifecycle stages:
- hypothesis framing
- experiment design
- decision-focused evaluation
- diagnostics/error analysis
</when_to_use>

<mode_policy>
Mode selection:
- `mode=hypothesis`: create or revise falsifiable hypothesis artifacts.
- `mode=experiment`: create reproducible experiment and analysis plans.
- `mode=decision`: classify outcome supports/inconclusive/rejects from results.
- `mode=diagnostics`: run error-analysis and sanity-check diagnostics.

If mode is missing, ask one focused question before continuing.
</mode_policy>

<source_of_truth>
Follow `.grd/workflows/research-pipeline.md` stages 1/2/3/3.5.
Use artifact conventions in `.grd/templates/research-artifact-format.md`.

Canonical output paths by mode:
- `hypothesis`:
  - `.grd/research/{hypothesis_id}/01_HYPOTHESIS.md`
  - optional run continuity mirror: `.grd/research/runs/{run_id}/1_HYPOTHESIS.md`
- `experiment`:
  - `.grd/research/runs/{run_id}/2_EXPERIMENT_PLAN.md`
  - optional `.grd/research/runs/{run_id}/2_ANALYSIS_PLAN.md`
- `decision`:
  - `.grd/research/runs/{run_id}/3_EVALUATION.md`
- `diagnostics`:
  - `.grd/research/runs/{run_id}/3_5_ERROR_ANALYSIS.md`

When run context exists, keep `.grd/research/latest` linked to `runs/{run_id}`.
</source_of_truth>

<clarification_rule>
Ask one high-leverage clarification question when any of these are missing:
- mode
- run_id/hypothesis_id
- decision threshold or evaluation target
- expected artifact output scope
</clarification_rule>

{{COMMON_BLOCKS}}

<semantic_change_guardrail>
Do not silently change data preprocessing, splits, or metric definitions; present options and ask for approval.
</semantic_change_guardrail>

<execution_contract>
1. Resolve mode from `<mode_policy>`.
2. Confirm identifiers and scope (`run_id`, `hypothesis_id`, metric/threshold context).
3. Execute stage contract by mode:

`mode=hypothesis`
- Write one falsifiable hypothesis with metric, baseline, effect size, decision rule, and refutation condition.
- Enforce canonical write path: `.grd/research/{hypothesis_id}/01_HYPOTHESIS.md`.
- Do not place hypothesis artifacts as flat files directly under `.grd/research/`.
- If `run_id` exists, update `.grd/research/runs/{run_id}/0_INDEX.md` and optional compatibility mirror `1_HYPOTHESIS.md`.

`mode=experiment`
- Define variants/controls, datasets/splits, seeds, budget guardrails, and analysis method.
- Write `.grd/research/runs/{run_id}/2_EXPERIMENT_PLAN.md`.
- Write `.grd/research/runs/{run_id}/2_ANALYSIS_PLAN.md` when pre-committed analysis detail is requested.

`mode=decision`
- Aggregate metrics with uncertainty and compare against predeclared criteria.
- Classify outcome as supports/inconclusive/rejects.
- Write `.grd/research/runs/{run_id}/3_EVALUATION.md` with explicit decision-check reasoning.

`mode=diagnostics`
- Run leakage/sanity checks, slice analysis, and failure-case diagnostics.
- Write `.grd/research/runs/{run_id}/3_5_ERROR_ANALYSIS.md`.

4. Refresh latest-run alias when run context is active:
   ```bash
   mkdir -p .grd/research/runs
   ln -sfn "runs/{run_id}" .grd/research/latest
   ```
5. End with one smallest next validating action.
</execution_contract>

<quality_bar>
- Keep outputs falsifiable, measurable, and reproducible.
- Distinguish observed evidence from inference.
- Prefer inconclusive over overstated claims when evidence is weak.
</quality_bar>
