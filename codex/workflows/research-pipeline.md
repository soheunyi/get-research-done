# GSD Research Pipeline

Use this pipeline when the primary goal is AI/statistics research instead of production feature delivery.

## Stage 0: Research Notes (Continuous)
- Keep a running evidence log as experiments evolve.
- Capture anomalies, discarded branches, and decision rationale.

Output:
- `RESEARCH_NOTES.md`

## Stage 1: Hypothesis Design
- Define one falsifiable hypothesis.
- Define target metric, baseline, and minimum effect size.
- Define hard stop criteria (time/budget) and validity threats.

Output:
- `HYPOTHESIS.md`

## Stage 1.5: Analysis Plan (Pre-commit)
- Define primary vs secondary metrics.
- Define aggregation across seeds (mean/std and CI method).
- Define statistical test or estimator (and multiple comparisons strategy if needed).
- Define leakage checks and no test peeking rule.

Output:
- `ANALYSIS_PLAN.md`

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

## Stage 3.5: Error Analysis and Sanity Checks
- Slice analysis across data subsets and inspect failure cases.
- Run sanity checks (label shuffle and controls where relevant).
- Confirm no leakage, correct split usage, and stable evaluation scripts.

Output:
- `ERROR_ANALYSIS.md`

## Stage 4: Ablation and Robustness
- Isolate contribution of each major component.
- Run stress tests: seed sensitivity, data slice robustness, hyperparameter range.
- Identify brittle assumptions and failure regions.

Output:
- `ABLATION.md`

## Stage 4.5: Numerical Stability and Determinism (if applicable)
- Audit nondeterminism sources and seed propagation.
- Check numerical stability (tolerances, precision, overflow, underflow).
- Run convergence or refinement tests when using discretizations or solvers.

Output:
- `NUMERICS_AUDIT.md`
- `RANDOMNESS_AUDIT.md`

## Stage 5: Reproducibility Packaging
- Lock environment, dataset versions, and exact commands.
- Publish a minimal replication path from clean checkout.
- Produce concise research summary with claims tied to evidence.

Output:
- `REPRODUCIBILITY.md`
- `RESEARCH_SUMMARY.md`
