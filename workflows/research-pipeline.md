# GSD Research Pipeline

Use this pipeline when the primary goal is AI/statistics research instead of production feature delivery.

## Stage 1: Hypothesis Design
- Define one falsifiable hypothesis.
- Define target metric, baseline, and minimum effect size.
- Define hard stop criteria (time/budget) and validity threats.

Output:
- `HYPOTHESIS.md`

## Stage 2: Experiment Plan
- Build an experiment matrix: variants, controls, datasets, seeds.
- Define evaluation protocol: splits, folds, confidence intervals, statistical test.
- Define reproducible run commands and artifact paths.

Output:
- `EXPERIMENT_PLAN.md`

## Stage 2.5: Experiment Tracking (W&B Recommended)
- Standardize run metadata and artifact lineage.
- Ensure every claim can be traced to a run and artifact.

Output:
- `WANDB_CONFIG.md`

## Stage 3: Evaluation Analysis
- Summarize raw results with uncertainty, not only point metrics.
- Run significance checks and compare against baseline and SOTA target.
- Classify outcome: supports / inconclusive / rejects hypothesis.

Output:
- `EVALUATION.md`

## Stage 4: Ablation and Robustness
- Isolate contribution of each major component.
- Run stress tests: seed sensitivity, data slice robustness, hyperparameter range.
- Identify brittle assumptions and failure regions.

Output:
- `ABLATION.md`

## Stage 0: Research Notes (Continuous)
- Keep a running evidence log as experiments evolve.
- Capture anomalies, discarded branches, and decision rationale.

Output:
- `RESEARCH_NOTES.md`

## Stage 5: Reproducibility Packaging
- Lock environment, dataset versions, and exact commands.
- Publish a minimal replication path from clean checkout.
- Produce concise research summary with claims tied to evidence.

Output:
- `REPRODUCIBILITY.md`
- `RESEARCH_SUMMARY.md`
