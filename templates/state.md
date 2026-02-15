# STATE

Use this file as the durable memory for what is decided versus still open.

## Snapshot
- Updated: [YYYY-MM-DD HH:MM]
- Current stage: [0|1|2|3|4|5]
- Analysis committed: [true|false]
- Active run id: [YYMMDD_slug or empty]
- Active thread: [short thread name]
- Next action: [single concrete action]

## Decisions (Current)
- [decision + why]
- [revise only with explicit user instruction or new contradicting evidence]

## AI Agent's Discretion
- [areas where agent can choose approach]

## Deferred (Out of Scope)
- [explicitly postponed items]

## Constraints
- Environment: [Codex sandbox only / Codex + remote GPU / orchestrated external infra]
- Time budget: [for example: 2 hours]
- Cost budget: [for example: max 4 long runs]
- Quality bar: [paper-ready / prototype / exploration]

## Terminology Registry
- term: [canonical short label]
  definition: [plain-language meaning in this project]
  operationalization: [how this is measured/computed/applied]
  aliases: [optional shorthand, comma-separated]

## Risks and Unknowns
- [risk or unknown]

## Handoff
- Last completed: [artifact or experiment id]
- Required context for next run: [minimum context packet]
