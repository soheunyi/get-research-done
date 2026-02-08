---
name: "GRD Change Attribution Inspector"
description: "Determine what changed vs stayed invariant across runs to explain observed metric deltas"
---

# Codex GRD Skill: grd-research-change-attribution-inspector

<when_to_use>
Use when comparing baseline vs candidate runs and you need clear attribution of gains/losses.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` and produce `.grd/research/CHANGE_ATTRIBUTION.md`.
</source_of_truth>

<clarification_rule>
If you are not sure what the user wants, pause and ask for pseudocode or a concrete step-by-step outline before continuing.
</clarification_rule>

<delivery_rule>
Default to concise chat output. Only write or update artifact files when the user explicitly asks for a saved deliverable.
</delivery_rule>

<execution_contract>
1. Diff run conditions and classify changed/invariant factors.
2. Flag confounds and unknowns that block attribution.
3. Rank attribution hypotheses by evidence strength.
4. Output findings and next ablations in `.grd/research/CHANGE_ATTRIBUTION.md`.
</execution_contract>
