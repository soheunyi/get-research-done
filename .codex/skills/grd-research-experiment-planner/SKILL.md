---
name: "grd-research-experiment-planner"
description: "Plan reproducible experiments with controls, seeds, splits, and statistical protocol"
---

# Codex GRD Skill: grd-research-experiment-planner

<when_to_use>
Use after hypothesis design and before running experiments.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/workflows/research-pipeline.md` Stage 2.
</source_of_truth>

<execution_contract>
1. Define control/treatment matrix.
2. Define dataset versions, seeds, split strategy, and run budget.
3. Define metrics, CI, and significance tests.
4. Produce `.gsd/research/EXPERIMENT_PLAN.md`.
</execution_contract>
