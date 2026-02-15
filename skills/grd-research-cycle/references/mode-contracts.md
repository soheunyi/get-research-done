# Mode Contracts

## hypothesis
- define falsifiable claim, baseline, effect size, decision rule
- write `.grd/research/{hypothesis_id}/01_HYPOTHESIS.md`

## experiment
- variants/controls, splits, seeds, budget, analysis method
- write `.grd/research/runs/{run_id}/2_EXPERIMENT_PLAN.md`
- optional `.grd/research/runs/{run_id}/2_ANALYSIS_PLAN.md`

## decision
- aggregate uncertainty-aware metrics and classify supports/inconclusive/rejects
- write `.grd/research/runs/{run_id}/3_EVALUATION.md`

## diagnostics
- run leakage/sanity/slice checks
- write `.grd/research/runs/{run_id}/3_5_ERROR_ANALYSIS.md`
