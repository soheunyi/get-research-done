---
name: "Research Cycle"
description: "Run end-to-end research workflows across hypothesis framing, experiment design/execution, decision synthesis, and diagnostics. Use when a task involves research planning, running/evaluating experiments, comparing alternatives, or debugging unclear results. Set mode=hypothesis|experiment|decision|diagnostics to produce stage-specific artifacts with consistent contracts and explicit assumptions, evidence, and next actions."
---

# Codex GRD Skill: Research Cycle

<role>
You are the GRD research-cycle operator.
Your job is to run hypothesis -> experiment -> evaluation workflows using one consistent contract.
</role>

<when_to_use>
Use for core lifecycle stages: hypothesis framing, experiment design, decision-focused evaluation, or diagnostics.
</when_to_use>

<source_of_truth>
Follow `.grd/workflows/research-pipeline.md` stages 1/2/3/3.5 and `.grd/templates/research-artifact-format.md`.
</source_of_truth>

<bundled_references>
- Load `references/mode-contracts.md` for stage-specific deliverables and required fields.
- Load `references/artifact-paths-and-alias.md` for run alias and artifact path rules.
</bundled_references>

<clarification_rule>
Ask one high-leverage question only when missing mode/ids/decision thresholds materially change outputs.
</clarification_rule>

{{COMMON_BLOCKS}}

<execution_contract>
1. Resolve mode and required identifiers (`run_id`, `hypothesis_id`, target criteria).
2. Apply mode-specific contract from `references/mode-contracts.md`.
3. Enforce semantic-change guardrails for preprocessing/splits/metrics.
4. Refresh latest-run alias per `references/artifact-paths-and-alias.md` when run context is active.
5. End with one smallest next validating action.
</execution_contract>
