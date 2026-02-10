---
name: "GRD Ideation and Reasoning"
description: "Combine cited idea discovery with structured tradeoff reasoning to recommend the next validating research direction"
---

# Codex GRD Skill: grd-research-ideation-and-reasoning

<when_to_use>
Use when the user needs research idea discovery plus decision-quality reasoning across multiple candidate approaches.
</when_to_use>

<source_of_truth>
Use `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` to align recommendations with stage goals.
When requested, write `.grd/research/IDEATION_AND_REASONING.md`.
</source_of_truth>

<clarification_rule>
Before searching or recommending, ask a short clarification question about scope, constraints, and desired output.
If intent remains unclear, ask for pseudocode or a concrete step-by-step outline before continuing.
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
1. Confirm topic scope, constraints, success metric, and acceptable risk.
2. Search high-signal sources with priority on primary references (papers, official docs, benchmark sites, maintainer repos).
3. Distill key evidence and separate evidence from inference.
4. Generate 2-4 candidate approaches grounded in cited references.
5. Evaluate tradeoffs for each approach: assumptions, expected impact, risk, effort, and time.
6. Recommend one approach with explicit rationale and known failure modes.
7. Propose the next smallest validating action and optional follow-up experiments.
8. Produce `.grd/research/IDEATION_AND_REASONING.md` when artifact output is requested.
9. Ask whether to save a research note as `.grd/research/notes/<timestamp_title>.md`.
</execution_contract>

<quality_bar>
- Distinguish evidence vs inference explicitly.
- Avoid uncited claims.
- Prefer recent and authoritative sources.
</quality_bar>
