# GSD Research Pipeline

Use this pipeline when the primary goal is AI/statistics research instead of production feature delivery.

## Interaction Contract (Questioning First)
- Before entering a stage, run a short guided questioning loop if the request is open-ended.
- Ask one high-leverage question per turn and provide 2-4 concrete options.
- Always include an explicit open-ended path: "If none fit, describe your own direction."
- After each answer, summarize captured constraints before asking the next question.
- Stop questioning when the next verifiable action is clear; avoid completeness theater.

Recommended question order:
1. Goal and "done" definition
2. Scope boundaries and exclusions
3. Execution environment and constraints
4. Preferred tradeoff (speed, rigor, novelty, cost)

Continuity handoff:
- Record decisions in `.grd/STATE.md` under `Decisions`, `AI Agent's Discretion`, and `Deferred`.
- Use those constraints to drive stage outputs.

## Persistent State Layer (Always On)
- Keep `.grd/STATE.md` as the canonical memory for locked decisions and constraints.
- Keep `.grd/ROADMAP.md` as the active queue of milestones and smallest next actions.
- Update both after major stage transitions or when direction changes.
- If state files are missing or empty, initialize through Stage -1 codebase mapping before choosing later stages.

Output:
- `.grd/STATE.md`
- `.grd/ROADMAP.md`

## Stage -1: Codebase Mapping (Brownfield / Drift Check)
- Capture current repository purpose, architecture shape, and known constraints.
- Define target repository shape for current research direction.
- List prioritized gaps from current to target with smallest next actions.

Output:
- `.grd/codebase/CURRENT.md`
- `.grd/codebase/TARGET.md`
- `.grd/codebase/GAPS.md`

## Stage 0: Research Notes (Continuous)
- Keep a running evidence log as experiments evolve.
- Capture anomalies, discarded branches, and decision rationale.
- Nudge optional thought-log entries when beliefs update or reasoning fails (do not enforce full template each time).

Output:
- `RESEARCH_NOTES.md`

## Stage 0.5: Phase Execution Research (Optional)
- For implementation-heavy phases, research stack patterns and pitfalls before writing plans or coding.
- Produce prescriptive guidance that minimizes trial-and-error during execution.

Output:
- `.grd/research/phases/{phase_id}-RESEARCH.md`

## Stage 1: Hypothesis Design
- Define one falsifiable hypothesis.
- Define target metric, baseline, and minimum effect size.
- Define hard stop criteria (time/budget) and validity threats.
- Use iterative thesis -> antithesis -> synthesis questioning to refine assumptions before locking the hypothesis.
- After locking hypothesis, nudge state tracking to append a hypothesis handoff note for Stage 3 traceability.

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
- Cross-check results against Stage 1 hypothesis fields (prediction, decision rule, refutation condition) before final classification.

Output:
- `EVALUATION.md`

## Stage 4: Ablation and Robustness
- Isolate contribution of each major component.
- Run stress tests: seed sensitivity, data slice robustness, hyperparameter range.
- Identify brittle assumptions and failure regions.

Output:
- `ABLATION.md`

## Stage 5: Reproducibility Packaging
- Lock environment, dataset versions, and exact commands.
- Publish a minimal replication path from clean checkout.
- Produce concise research summary with claims tied to evidence.

Output:
- `REPRODUCIBILITY.md`
- `RESEARCH_SUMMARY.md`
