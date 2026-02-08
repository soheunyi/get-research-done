---
name: "grd-research-wandb-integrator"
description: "Standardize Weights & Biases tracking for reproducible experiment lineage"
---

# Codex GRD Skill: grd-research-wandb-integrator

<when_to_use>
Use when research requires systematic run tracking, artifact lineage, and cross-run comparison.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/workflows/research-pipeline.md` Stage 2.5 and write `.gsd/research/WANDB_CONFIG.md`.
</source_of_truth>

<execution_contract>
1. Define W&B naming and metadata schema.
2. Enforce logging of config, seed, dataset version, and commit SHA.
3. Define artifact and alias conventions.
4. Include offline/resume policies and generate `.gsd/research/WANDB_CONFIG.md`.
</execution_contract>
