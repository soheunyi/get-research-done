# Checkpoint Operations Contract

Use this file when running `Research State Keeper` in `mode=checkpoint`.

## Checkpoint Behavior

1. Infer minimal updates from recent artifacts/commits and current state files.
2. Ask at most one clarification question only if it changes the next action.
3. Update only changed fields in `.grd/STATE.md` and `.grd/ROADMAP.md`.
4. Recommend exactly one smallest high-confidence next skill/action.
5. Keep `Decisions -> Current decisions (active constraints)` current and append key shifts to `Decision log (append-only)`.
6. Update `Experiment queue (planned)` and `Run registry (executed evidence)` when new experiment intent/results exist.

## Activity Capture Policy

Default append behavior:
- `checkpoint`: append one compact entry to `.grd/research/RESEARCH_NOTES.md`.
- `kickoff`: append one compact kickoff entry after initialization.
- `colleague`: append only with explicit user confirmation.

Entry minimum fields:
- Context
- Observation
- Evidence (file path or command)
- Decision
- Next action

## Timestamp Guard

When writing a time-specific note header in `.grd/research/RESEARCH_NOTES.md`:
1. Fetch exact local system time immediately before write.
2. If exact time is unnecessary or unavailable, use explicit date-only format (`YYYY-MM-DD`).
3. Never infer/approximate timestamps from conversational flow.

## Terminology Policy

Maintain `## Terminology (only what is referenced above)` in `.grd/STATE.md` when explicit user request exists or repeated shorthand could cause ambiguity.

Entry format:
- `term`: canonical label
- `definition`: plain-language meaning in project context
- `notation`: symbols/domains/dimensions when needed
- `operationalization`: measurable/implementation meaning when relevant
- `code pointer`: file:function for implementation anchor
- `aliases`: optional synonyms/shorthand

## Artifact Placement Policy

Default ad-hoc research artifact path:
- `.grd/research/<topic_slug>/<artifact_name>.md`

Allowed flat path only when user explicitly requests it:
- `.grd/research/<artifact_name>.md`

Canonical exceptions:
- `.grd/research/RESEARCH_NOTES.md`
- `.grd/research/runs/{run_id}/0_INDEX.md`

## Feedback Rollup

If `.grd/SKILL_FEEDBACK_LOG.md` exists during checkpoint:
1. Scan recent entries for recurrence.
2. Surface top 1-3 recurring failure patterns.
3. Convert recurring issues into roadmap queue items with owner and verification check.
