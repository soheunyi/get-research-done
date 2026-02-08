---
name: "grd-research-ablation-planner"
description: "Design ablations and robustness checks to isolate true contribution"
---

# Codex GRD Skill: grd-research-ablation-planner

<when_to_use>
Use after positive results to validate causality and robustness.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/workflows/research-pipeline.md` Stage 4.
</source_of_truth>

<execution_contract>
1. Define components and assumptions to isolate.
2. Design ablation matrix and robustness checks.
3. Rank brittle regions and failure modes.
4. Produce `.gsd/research/ABLATION.md`.
</execution_contract>
