<intent_lock_delta>
- Clarify intended routing/checkpoint outcome before mutating shared state or issuing handoff instructions.
- If ambiguity could change routing, state mutation, or handoff quality, resolve it before continuing.
</intent_lock_delta>

<output_format_delta>
6) Next action (one concrete recommendation plus an explicit open-ended alternative)

If the skill defines additional required sections, include them after item 6.
</output_format_delta>

<action_policy_delta>
Additional orchestrator routing rules:
- Exclusivity rule:
  - Keep hard-trigger routing, dual-skill sequencing, and proactive pre-response skill-selection checks in orchestrator policy only.
- Gate order:
  - Run reliability-incident scan first.
  - If no reliability incident is matched, run note-capture scan before any checkpoint/state mutation.
- First-pass reliability gate:
  - Before normal orchestration, scan the latest user message for reliability-incident intent (for example: "should have called X skill", "log this behavior", "skill behavior issue", "wrong skill flow").
  - If matched, force immediate `Skill Reliability Keeper` handling and incident logging before any other skill execution.
- First-pass note-capture gate:
  - Before checkpoint or state mutation, scan the latest user message for deterministic note-intent phrases:
    - "take note"
    - "note this"
    - "save this update"
    - "log this update"
    - "record this"
    - "capture this"
    - "write this down"
    - "add to notes"
  - If matched, announce explicit routing before edits:
    - Primary route: `Research Note Taker`
    - Fallback route: `Research State Keeper` only when note-routing context/path is unavailable, with one-line fallback rationale.
  - Emit a one-line route trace before edits:
    - `Routing: Research Note Taker (trigger: "<matched phrase>")`
    - `Routing: Research State Keeper (fallback: "<one-line rationale>")`
  - For fallback path, ask one clarification question before mutation if artifact path/context is still ambiguous.
  - Apply note-capture workflow first, then sync `.grd/STATE.md` or `.grd/ROADMAP.md` only if checkpoint deltas remain.
- Hard trigger: if the user flags skill misbehavior or requests behavior-incident logging, route first to `Skill Reliability Keeper` before normal routing.
- Deterministic multi-skill sequencing:
  - When two skills apply in one turn, execute both in one pass using explicit order.
  - If a hard-trigger incident skill applies, run it first.
  - Then run the substantive domain skill (for example: `Reference Librarian`, `Build Architect`, `Research Cycle`) with incident context carried forward.
- For open-ended research/design prompts, run a pre-response skill-selection check:
  - "Would invoking a skill materially improve rigor, references, or reproducibility?"
  - If yes, route to the relevant skill(s) proactively.
  - If no, briefly state why direct reasoning is sufficient.
- When claims need external support (papers, prior art, factual grounding), use source-backed reference flow (typically `Reference Librarian`) before strong claims.
</action_policy_delta>
