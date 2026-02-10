---
name: "GRD Attribution and Robustness"
description: "Unify reactive change attribution and proactive ablation planning to isolate causal drivers and robustness"
---

# Codex GRD Skill: grd-research-attribution-and-robustness

<when_to_use>
Use when results changed and you need to explain why, or when positive results need causal isolation and robustness validation.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` Stage 3.5 and Stage 4.
When requested, produce `.grd/research/ATTRIBUTION_AND_ABLATION.md`.
</source_of_truth>

<clarification_rule>
Before any complex task, first ask for the user perspective, constraints, and preferred direction.
If intent remains unclear, pause and ask for pseudocode or a concrete step-by-step outline before continuing.
</clarification_rule>

<precision_contract>
- Provide exact file paths, commands, and expected outputs.
- Use numbered steps and execute smallest-valid slice first.
- State assumptions and unknowns explicitly; do not silently guess.
- Define done criteria and verification commands before execution.
- If blocked, report the blocker and the next minimal unblocked action.
</precision_contract>

<context_budget>
- Read only files directly relevant to the task.
- Start with up to 8 files; if more are needed, state why before continuing.
- Prefer targeted excerpts and summaries over full-file reads.
- Do not scan unrelated directories.
</context_budget>

<intent_lock>
- Before action, restate the user intent in up to 3 sentences.
- If ambiguity could change the outcome, ask one focused clarification.
- For MED/HIGH actions, pause and confirm direction before proceeding.
</intent_lock>

<delivery_rule>
Default to concise chat output.

- If user explicitly asks for a saved deliverable: write or update artifact files.
- Otherwise: provide a proposed diff outline (files plus key edits) and verification steps.
</delivery_rule>

<output_format>
Always structure the response as:

1) Assumptions (bullet list; call out unknowns)
2) Plan (numbered; smallest-first)
3) Proposed changes / artifacts
   - If user did NOT ask to write files: provide a proposed diff outline plus filenames
   - If user DID ask to write files: write or update artifact files named in <source_of_truth>
4) Verification steps (how to check it worked)
5) Risks and failure modes (brief; include data leakage and confounds when relevant)
</output_format>

<action_policy>
Default: propose actions; do not execute side-effecting steps unless user explicitly asks.
Guardrail: for MED or HIGH complexity tasks, pause and ask for the user perspective before proceeding.

Risk tiers:
- LOW: summarize, plan, draft text, propose diffs, read-only inspection.
- MED: modify code or configs, run tests or training scripts, change evaluation protocol.
- HIGH: delete or overwrite data, touch secrets or credentials, publish externally, deploy, spend money or credits.

Contract:
1) Ask for user thoughts before starting any MED or HIGH complexity task and confirm the preferred direction.
2) List Proposed Actions (files, commands, external calls).
3) Label each action LOW, MED, or HIGH plus rollback plan.
4) Require explicit user approval for MED and HIGH actions.
</action_policy>

<execution_contract>
1. Diff run conditions and classify changed versus invariant factors.
2. Flag confounds, leakage risks, and unknowns that block strong attribution.
3. Rank attribution hypotheses by evidence strength.
4. Design the minimal ablation and robustness matrix to isolate plausible causes.
5. Prioritize next experiments by expected information gain and cost.
6. Summarize causal conclusions, remaining uncertainty, and recommended next checks.
7. Produce `.grd/research/ATTRIBUTION_AND_ABLATION.md` when artifact output is requested.
</execution_contract>
