---
name: "grd-research-change-attribution-inspector"
description: "Determine what changed vs stayed invariant across runs to explain observed metric deltas"
---

# Codex GRD Skill: grd-research-change-attribution-inspector

<when_to_use>
Use when comparing baseline vs candidate runs and you need clear attribution of gains/losses.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/workflows/research-pipeline.md` and produce `.gsd/research/CHANGE_ATTRIBUTION.md`.
</source_of_truth>

<execution_contract>
1. Diff run conditions and classify changed/invariant factors.
2. Flag confounds and unknowns that block attribution.
3. Rank attribution hypotheses by evidence strength.
4. Output findings and next ablations in `.gsd/research/CHANGE_ATTRIBUTION.md`.
</execution_contract>
