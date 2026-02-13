# GSD Research Pipeline

Use this pipeline when the primary goal is AI/statistics research instead of production feature delivery.

Artifact format reference:
- `templates/research-artifact-format.md`

Run convention:
- Group linked artifacts under `.grd/research/runs/{run_id}/`
- Maintain `.grd/research/latest` alias to the active run directory (`.grd/research/runs/{run_id}/`)

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
- `.grd/research/RESEARCH_NOTES.md`

## Stage 0.5: Phase Execution Research (Optional)
- For implementation-heavy phases, research stack patterns and pitfalls before writing plans or coding.
- Produce prescriptive guidance that minimizes trial-and-error during execution.

Output:
- `.grd/research/phases/{phase_id}-RESEARCH.md`

## Stage 0.75: Deep Reasoning Question Draft (Optional)
- Draft a high-quality prompt/question for external deep-thinking or deep-research (literature survey) models.
- Summarize relevant context, clarify the exact question, and define all mathematical terms/symbols explicitly.
- For literature-review prompts, specify topic boundaries, inclusion/exclusion criteria, and source/citation expectations.
- Add strict answer-format expectations and success criteria to reduce ambiguity.

Output:
- `.grd/research/questions/{question_id}-QUESTION.md`

## Stage 1: Hypothesis Design
- Define one falsifiable hypothesis.
- Define target metric, baseline, and minimum effect size.
- Define hard stop criteria (time/budget) and validity threats.
- Use iterative thesis -> antithesis -> synthesis questioning to refine assumptions before locking the hypothesis.
- Commit analysis decision rule for this run (`analysis_committed: true`) before execution-heavy stages.
- After locking hypothesis, nudge `Research State Keeper` to append a hypothesis handoff note for Stage 3 traceability.

Output:
- `.grd/research/runs/{run_id}/0_INDEX.md`
- `.grd/research/runs/{run_id}/1_HYPOTHESIS.md`

## Stage 2: Experiment Plan
- Build an experiment matrix: variants, controls, datasets, seeds.
- Define evaluation protocol: splits, folds, confidence intervals, statistical test.
- Define reproducible run commands and artifact paths.

Output:
- `.grd/research/runs/{run_id}/2_EXPERIMENT_PLAN.md`
- `.grd/research/runs/{run_id}/2_ANALYSIS_PLAN.md` (optional)

## Stage 2.5: Experiment Tracking (W&B Recommended)
- Standardize run metadata and artifact lineage.
- Ensure every claim can be traced to a run and artifact.

Output:
- `.grd/research/runs/{run_id}/2_WANDB_CONFIG.md`

## Stage 3: Evaluation Analysis
- Summarize raw results with uncertainty, not only point metrics.
- Run significance checks and compare against baseline and SOTA target.
- Classify outcome: supports / inconclusive / rejects hypothesis.
- Cross-check results against Stage 1 hypothesis fields (prediction, decision rule, refutation condition) before final classification.

Output:
- `.grd/research/runs/{run_id}/3_EVALUATION.md`

## Stage 3.5: Error Analysis and Sanity Checks
- Slice analysis across data subsets and inspect failure cases.
- Run sanity checks (label shuffle and controls where relevant).
- Confirm no leakage, correct split usage, and stable evaluation scripts.

Output:
- Preferred: `.grd/research/runs/{run_id}/3_5_ERROR_ANALYSIS.md`
- Compatibility fallback: `ERROR_ANALYSIS.md` (legacy path)

## Stage 4: Ablation and Robustness
- Isolate contribution of each major component.
- Run stress tests: seed sensitivity, data slice robustness, hyperparameter range.
- Identify brittle assumptions and failure regions.

Output:
- `.grd/research/runs/{run_id}/4_ABLATION.md`

## Stage 4.5: Numerical Stability and Determinism (if applicable)
- Audit nondeterminism sources and seed propagation.
- Check numerical stability (tolerances, precision, overflow, underflow).
- Run convergence or refinement tests when using discretizations or solvers.

Output:
- `.grd/research/runs/{run_id}/4_NUMERICS_AUDIT.md`
- `.grd/research/runs/{run_id}/4_RANDOMNESS_AUDIT.md`

## Stage 5: Reproducibility Packaging
- Lock environment, dataset versions, and exact commands.
- Publish a minimal replication path from clean checkout.
- Produce concise research summary with claims tied to evidence.

Output:
- `.grd/research/runs/{run_id}/5_REPRODUCIBILITY.md`
- `.grd/research/runs/{run_id}/6_RESEARCH_SUMMARY.md`
