---
name: Research Notes Tracker
description: Maintains structured running research notes with decisions, anomalies, and next experiments
---

# Research Notes Tracker

<role>
You keep a concise but rigorous research log across sessions.
</role>

<when_to_use>
Use throughout experimentation whenever assumptions, anomalies, or decisions appear.
</when_to_use>

<protocol>
1. Append timestamped notes to `.gsd/research/RESEARCH_NOTES.md`.
2. Capture: hypothesis link, run id/seed, observed metrics, anomalies.
3. Record decision and rationale (continue, pivot, rollback, stop).
4. List next action with owner and expected evidence.
5. Keep entries short and evidence-oriented.
</protocol>

<entry_format>
## YYYY-MM-DD HH:MM
- Context: [phase/experiment]
- Observation: [result + metric]
- Evidence: [artifact path or command]
- Decision: [what changed]
- Next: [next run/check]
</entry_format>
