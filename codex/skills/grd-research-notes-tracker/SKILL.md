---
name: "grd-research-notes-tracker"
description: "Maintain structured research notes with observations, decisions, and next actions"
---

# Codex GRD Skill: grd-research-notes-tracker

<when_to_use>
Use during and after experiment runs to keep a durable research trail.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` and update `.grd/research/RESEARCH_NOTES.md`.
</source_of_truth>

<clarification_rule>
If user intent is unclear, ask a short clarification question before continuing.
</clarification_rule>

<delivery_rule>
Default to concise chat output. Only write or update artifact files when the user explicitly asks for a saved deliverable.
</delivery_rule>

<execution_contract>
1. First ask the user what they want to record.
2. Append a timestamped note entry.
3. Include observation, evidence pointer, decision, and next action.
4. Keep notes compact and reproducibility-focused.
</execution_contract>
