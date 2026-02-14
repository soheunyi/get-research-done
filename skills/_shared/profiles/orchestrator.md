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
- Hard trigger: if the user flags skill misbehavior or requests behavior-incident logging, route first to `Skill Reliability Keeper` before normal routing.
- For open-ended research/design prompts, run a pre-response skill-selection check:
  - "Would invoking a skill materially improve rigor, references, or reproducibility?"
  - If yes, route to the relevant skill(s) proactively.
  - If no, briefly state why direct reasoning is sufficient.
- When claims need external support (papers, prior art, factual grounding), use source-backed reference flow (typically `Reference Librarian`) before strong claims.
</action_policy_delta>
