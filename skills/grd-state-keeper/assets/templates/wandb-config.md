# WANDB_CONFIG

## Project Identity
- Entity: [team/user]
- Project: [project-name]
- Default tags: [research, phase-x, model-y]

## Run Schema (Required)
- hypothesis_id
- experiment_id
- variant_id
- seed
- dataset_version
- commit_sha

## Metric Policy
- Primary metric: [for example: val_f1]
- Secondary metrics: [for example: val_loss, calibration_error]
- Report cadence: [step/epoch]

## Artifact Policy
- Model artifact name: [pattern]
- Dataset artifact name: [pattern]
- Aliases: [baseline, candidate, best, vN]

## Reproducibility Policy
- Resume policy: [must/optional]
- Offline policy: [wandb offline + later sync]
- Export policy: [tables/files to persist outside W&B]
