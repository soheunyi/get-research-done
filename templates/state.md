# STATE

Use this file as the durable memory for what is decided versus still open.

## Snapshot
- Updated: [YYYY-MM-DD HH:MM]
- Current stage: [0|1|2|3|4|5]
- Analysis committed: [true|false]
- Active run id: [YYMMDD_slug or empty]
- Active thread: [short thread name]
- Next action: [single concrete action]

## Recent Activity (Latest 3)
- [YYYY-MM-DD HH:MM] [what changed] -> [next action]
- [YYYY-MM-DD HH:MM] [what changed] -> [next action]
- [YYYY-MM-DD HH:MM] [what changed] -> [next action]

## Decisions (Locked)
- [decision + why]

## AI Agent's Discretion
- [areas where agent can choose approach]

## Deferred (Out of Scope)
- [explicitly postponed items]

## Constraints
- Environment: [Codex sandbox only / Codex + remote GPU / orchestrated external infra]
- Time budget: [for example: 2 hours]
- Cost budget: [for example: max 4 long runs]
- Quality bar: [paper-ready / prototype / exploration]

## Risks and Unknowns
- [risk or unknown]

## Handoff
- Last completed: [artifact or experiment id]
- Required context for next run: [minimum context packet]
