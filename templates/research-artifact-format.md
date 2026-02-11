# Research Artifact Naming and Frontmatter

Use this format for stage artifacts in `.grd/research/`.

## Directory Convention (Run-Centric)

Create one directory per linked hypothesis/plan/evaluation set.

Pattern:
- Run directory: `.grd/research/runs/{run_id}/`
- Run id: `YYMMDD_{summary}`

Examples:
- `.grd/research/runs/260211_adaptive_basis/`
- `.grd/research/runs/260215_sparse_correction/`

Required files in each run directory:
- `0_INDEX.md`
- `1_HYPOTHESIS.md`
- `2_EXPERIMENT_PLAN.md`
- `3_EVALUATION.md`

Optional files:
- `2_ANALYSIS_PLAN.md`
- `2_WANDB_CONFIG.md`
- `4_ABLATION.md`
- `4_NUMERICS_AUDIT.md`
- `4_RANDOMNESS_AUDIT.md`
- `5_REPRODUCIBILITY.md`
- `6_RESEARCH_SUMMARY.md`

## Latest Run Alias

Keep a single alias to the active run:
- `.grd/research/latest` -> `.grd/research/runs/{run_id}/`

Recommended command:

```bash
mkdir -p .grd/research/runs
ln -sfn "runs/{run_id}" .grd/research/latest
```

## Common Frontmatter (Required)

```yaml
---
run_id: "YYMMDD_slug"
artifact_type: "<index|hypothesis|analysis_plan|experiment_plan|evaluation|ablation|wandb_config|reproducibility|research_summary|numerics_audit|randomness_audit>"
stage: "<0|1|2|3|4|5>"
analysis_committed: <true|false>
title: "<short human title>"
summary: "<1-2 line summary>"
status: "<draft|active|superseded|validated|rejected|archived>"
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
owner: "<user|ai-agent>"
tags: []
depends_on: []
---
```

## Field Format Reference

- `run_id`: string, pattern `YYMMDD_slug` (example: `260211_adaptive_basis`)
- `artifact_type`: enum
  - `index|hypothesis|analysis_plan|experiment_plan|evaluation|ablation|wandb_config|reproducibility|research_summary|numerics_audit|randomness_audit`
- `stage`: integer-like string enum `0|1|2|3|4|5`
- `analysis_committed`: boolean (`true` or `false`)
- `title`: short string, 3-80 chars
- `summary`: short string, 1-2 lines
- `status`: enum `draft|active|superseded|validated|rejected|archived`
- `created_at`, `updated_at`: date string `YYYY-MM-DD`
- `owner`: enum `user|ai-agent`
- `tags`: list of strings
- `depends_on`: list of strings (artifact ids or relative artifact paths)

## Stage-Specific Frontmatter Additions

### INDEX
- `current_decision`: enum `supports|inconclusive|rejects|pending`
- `next_action`: one-line imperative string
- Artifact inventory should be inferred from files in `.grd/research/runs/{run_id}/` rather than duplicated in frontmatter.

Example:
```yaml
current_decision: "pending"
next_action: "Run seed sweep with fixed dataset split."
```

### Hypothesis
- `hypothesis_id`: string id (recommended: `HYP-YYMMDD-slug`)
- `primary_metric`: metric key string (for example: `val_f1`)
- `decision_rule`: explicit threshold/comparator string
- `refutation_condition`: explicit falsification condition string

Example:
```yaml
hypothesis_id: "HYP-260211-adaptive-basis"
primary_metric: "val_f1"
decision_rule: "supports if delta_val_f1 >= 0.02 over baseline with p < 0.05"
refutation_condition: "reject if delta_val_f1 < 0.005 across 5 seeds"
```

### Experiment / Analysis Plan
- `hypothesis_id`: string id matching hypothesis artifact
- `plan_id`: string id (recommended: `PLAN-YYMMDD-slug`)
- `dataset_version`: immutable dataset ref string
- `seed_policy`: explicit seed spec string
- `budget_guardrail`: compute/time cap string

Example:
```yaml
hypothesis_id: "HYP-260211-adaptive-basis"
plan_id: "PLAN-260211-seed-sweep"
dataset_version: "dataset-v3.2.1"
seed_policy: "seeds=[11,22,33,44,55]"
budget_guardrail: "max 20 GPU-hours"
```

### Evaluation
- `hypothesis_id`: string id
- `plan_id`: string id
- `outcome`: enum `supports|inconclusive|rejects`
- `decision_check`: short string verifying planned rule vs observed result

Example:
```yaml
hypothesis_id: "HYP-260211-adaptive-basis"
plan_id: "PLAN-260211-seed-sweep"
outcome: "inconclusive"
decision_check: "threshold not met; p-value above precommitted cutoff"
```

### Reproducibility
- `commit_sha`: git sha string (7+ chars)
- `environment_lock`: lockfile or image identifier string
- `rerun_command`: exact shell command string

Example:
```yaml
commit_sha: "fe6e3b7"
environment_lock: "conda-lock@sha256:abcd1234"
rerun_command: "python train.py --config runs/260211_adaptive_basis/config.yaml"
```

## Minimal Operational Rule

If you create or update a stage artifact:
1. write to `.grd/research/runs/{run_id}/{ARTIFACT}.md`
2. refresh `.grd/research/latest` alias to `runs/{run_id}`
3. keep frontmatter complete and current
