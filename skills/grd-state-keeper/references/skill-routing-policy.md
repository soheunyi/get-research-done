# Skill Routing Policy (Long-Tail)

Use this file when a user intent is not covered by the hot-path `<routing_table>` in `SKILL.md`.

## Long-Tail Mappings

- Stage 4 attribution/ablation/robustness nuances -> `Ablation Recommender`
- Prompt-authoring for deep reasoning/literature-review tasks -> `Question Maker`
- Repeated request-pattern reviews and new-skill opportunity checks -> `Observer`
- Implementation quality gate and skeptical diff review -> `Algo Verifier`
- Idea generation and tradeoff analysis when architecture-level framing is needed -> `Build Architect`

## Tie-Break Rules

When multiple long-tail mappings appear applicable:
1. If user message includes reliability incident intent, route to `Skill Reliability Keeper` first.
2. If user message includes explicit note-capture intent, route to `Research Note Taker` before any checkpoint/state mutation.
3. If external factual grounding is required, run `Reference Librarian` before strong claims.
4. If a request requires concrete artifact production, choose the skill that owns the target artifact contract.
5. If still ambiguous, ask one high-leverage clarification question and present 2-3 likely skill routes.

## Deterministic Note-Intent Triggers

Treat these phrases as direct note-routing triggers:
- "take note"
- "note this"
- "save this update"
- "log this update"
- "record this"
- "capture this"
- "write this down"
- "add to notes"

On match:
1. Announce explicit route before edits (`Research Note Taker` or `Research State Keeper` fallback rationale).
2. Run note capture first.
3. Apply checkpoint updates only after note capture when state deltas remain.

## Promotion Rule (Long-Tail -> Hot-Path)

Promote a long-tail route into the hot-path `<routing_table>` only when one is true:
- It appears frequently across checkpoints (high recurrence), or
- Misrouting it causes high impact/risk (high severity), or
- It frequently co-occurs with reliability incidents.

When promoted, remove duplicate wording from this file to avoid drift.

## Maintenance

Update this file first for long-tail route changes.
Keep hot-path routing table in `SKILL.src.md` minimal and high-frequency/high-risk only.
