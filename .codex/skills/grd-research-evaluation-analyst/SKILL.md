---
name: "grd-research-evaluation-analyst"
description: "Analyze results with uncertainty and significance to classify hypothesis outcome"
---

# Codex GRD Skill: grd-research-evaluation-analyst

<when_to_use>
Use when experiment outputs are available and you need a decision.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/workflows/research-pipeline.md` Stage 3.
</source_of_truth>

<execution_contract>
1. Aggregate results with uncertainty ranges.
2. Compare against baseline and effect size targets.
3. Run planned significance tests.
4. Produce `.gsd/research/EVALUATION.md`.
</execution_contract>
