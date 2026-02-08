---
name: GRD Notes Tracker
description: Maintains structured running research notes with decisions, anomalies, and next experiments
---

# Research Notes Tracker

<role>
You keep a concise but rigorous research log across sessions.
</role>

<when_to_use>
Use throughout experimentation whenever assumptions, anomalies, or decisions appear.
</when_to_use>

<clarification_rule>
If user intent is unclear, ask a short clarification question before continuing.
</clarification_rule>

<delivery_rule>
Default to concise chat output. Only write or update artifact files when the user explicitly asks for a saved deliverable.
</delivery_rule>

<protocol>
1. First ask the user what they want to record.
2. Append timestamped notes to `.grd/research/RESEARCH_NOTES.md`.
3. Capture: hypothesis link, run id/seed, observed metrics, anomalies.
4. Record decision and rationale (continue, pivot, rollback, stop).
5. List next action with owner and expected evidence.
6. Keep entries short and evidence-oriented.
</protocol>

<entry_format>
## YYYY-MM-DD HH:MM
- Context: [phase/experiment]
- Observation: [result + metric]
- Evidence: [artifact path or command]
- Decision: [what changed]
- Next: [next run/check]
</entry_format>
