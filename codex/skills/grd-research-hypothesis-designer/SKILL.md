---
name: "GRD Hypothesis Designer"
description: "Define falsifiable hypotheses, metrics, and stop criteria for research phases"
---

# Codex GRD Skill: grd-research-hypothesis-designer

<when_to_use>
Use for hypothesis framing before writing experiment code.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` Stage 1.
</source_of_truth>

<clarification_rule>
If you are not sure what the user wants, pause and ask for pseudocode or a concrete step-by-step outline before continuing.
</clarification_rule>

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

Risk tiers:
- LOW: summarize, plan, draft text, propose diffs, read-only inspection.
- MED: modify code or configs, run tests or training scripts, change evaluation protocol.
- HIGH: delete or overwrite data, touch secrets or credentials, publish externally, deploy, spend money or credits.

Contract:
1) List Proposed Actions (files, commands, external calls).
2) Label each action LOW, MED, or HIGH plus rollback plan.
3) Require explicit user approval for MED and HIGH actions.
</action_policy>

<execution_contract>
1. Write one falsifiable hypothesis.
2. Define baseline, metric, effect size, and decision threshold.
3. Define stop criteria and validity threats.
4. Produce `.grd/research/HYPOTHESIS.md`.
</execution_contract>
