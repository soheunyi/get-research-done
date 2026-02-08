---
name: "GRD Ablation Planner"
description: "Design ablations and robustness checks to isolate true contribution"
---

# Codex GRD Skill: grd-research-ablation-planner

<when_to_use>
Use after positive results to validate causality and robustness.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` Stage 4.
</source_of_truth>

<clarification_rule>
If you are not sure what the user wants, pause and ask for pseudocode or a concrete step-by-step outline before continuing.
</clarification_rule>

<delivery_rule>
Default to concise chat output. Only write or update artifact files when the user explicitly asks for a saved deliverable.
</delivery_rule>

<execution_contract>
1. Define components and assumptions to isolate.
2. Design ablation matrix and robustness checks.
3. Rank brittle regions and failure modes.
4. Produce `.grd/research/ABLATION.md`.
</execution_contract>
