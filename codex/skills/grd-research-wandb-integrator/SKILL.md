---
name: "grd-research-wandb-integrator"
description: "Standardize Weights & Biases tracking for reproducible experiment lineage"
---

# Codex GRD Skill: grd-research-wandb-integrator

<when_to_use>
Use when research requires systematic run tracking, artifact lineage, and cross-run comparison.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` Stage 2.5 and write `.grd/research/WANDB_CONFIG.md`.
</source_of_truth>

<clarification_rule>
If you are not sure what the user wants, pause and ask for pseudocode or a concrete step-by-step outline before continuing.
</clarification_rule>

<delivery_rule>
Default to concise chat output. Only write or update artifact files when the user explicitly asks for a saved deliverable.
</delivery_rule>

<execution_contract>
1. Define W&B naming and metadata schema.
2. Enforce logging of config, seed, dataset version, and commit SHA.
3. Define artifact and alias conventions.
4. Include offline/resume policies and generate `.grd/research/WANDB_CONFIG.md`.
</execution_contract>
