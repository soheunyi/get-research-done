---
name: "GRD Idea Seeker"
description: "Search the web for relevant references, cite them, and generate evidence-backed research idea sketches"
---

# Codex GRD Skill: grd-research-idea-seeker

<when_to_use>
Use when user wants related work discovery, external references, or idea generation grounded in citations.
</when_to_use>

<source_of_truth>
Align ideas with `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` stage expectations.
</source_of_truth>

<clarification_rule>
Before searching, ask a short clarification question about scope, constraints, and desired output if missing.
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
1. Confirm topic scope and constraints (time, compute, risk tolerance, success metric).
2. Search web sources with priority on primary references (papers, official docs, benchmark sites, maintainer repos).
3. Filter to high-signal references that directly inform the user question.
4. Summarize each selected reference briefly with claim, method, and relevance.
5. Generate 3-5 research idea sketches linked to cited references.
6. For each sketch include: hypothesis, novelty angle, first experiment, risk, and decision metric.
7. Return a clear references list (title + URL) for every cited source.
8. Write `.grd/research/IDEA_SEEKER.md` when artifact output is requested.
9. Ask whether to save a research note as `.grd/research/notes/<timestamp_title>.md`.
</execution_contract>

<quality_bar>
- Distinguish evidence vs inference explicitly.
- Avoid uncited claims.
- Prefer recent and authoritative sources.
</quality_bar>
