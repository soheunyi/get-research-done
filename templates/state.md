# STATE — durable research memory (single source of truth)

**TL;DR:** <one-line current objective> | **North-star metric:** <metric> | **Next:** <next action>

## Metadata
- Updated: <YYYY-MM-DD HH:MM TZ>
- Stage: <int or name>
- Repo commit: <git sha>
- Active thread: <short slug>
- Active run id: <R-... or empty>
- Analysis committed: <true/false>

## Now (hot state)
### Objective
- <current objective, 1–3 bullets>

### Success criteria
- Primary metric(s): <...>
- Secondary metric(s): <...>
- Required artifacts: <what files/plots/tables must be produced>
- Repro requirement: <what makes it reproducible>

### Next 1–3 actions
1) <imperative action>
2) <imperative action>
3) <imperative action>

### Entry points (what to run / edit)
- Command(s): `<...>`
- Key scripts: `<...>`
- Key configs: `<...>`
- Key functions/modules: `<...>`

## Decisions
### Current decisions (active constraints)
- <bullet decisions that are currently in force>

### Decision log (append-only)
| date (<TZ>) | id | decision | rationale | consequences | pointers |
|---|---|---|---|---|---|
| <YYYY-MM-DD> | D-<YYYYMMDD-XX> | <...> | <...> | <...> | <file/func/issue/pr> |

## Experiment queue (planned)
| priority | exp id | change vs baseline | settings | expected signal | est cost | status | pointers |
|---|---|---|---|---|---|---|---|
| P0 | E-<YYYYMMDD-XX> | <...> | <...> | <...> | <low/med/high> | <todo/running/done> | <...> |

## Run registry (executed evidence)
| run id | date (<TZ>) | commit | cmd/script | config pointer | seeds | key metrics | artifact path | notes |
|---|---|---|---|---|---|---|---|---|
| R-<YYYYMMDD-XX> | <YYYY-MM-DD> | <sha> | <...> | <...> | <...> | <...> | <...> | <...> |

## Baselines (optional, compact)
- Baseline name: <...>
  - Definition: <what it is>
  - Pointer: <code/config>
  - Expected range: <metric ranges if known>

## Terminology (only what is referenced above)
- **<term>**
  - definition: <math/words>
  - notation: <symbols and domains/dimensions>
  - operationalization: <tensor shapes / data schema>
  - code pointer: <file:function>
  - aliases: <...>

## Open questions
- [ ] <question phrased so it can be answered by an experiment or proof>
- [ ] <...>

## Risks
- <risk>: <impact> | <mitigation>

## Constraints
- Environment: <...>
- Time budget: <...>
- Cost budget: <...>
- Quality bar: <...>

## References (optional)
- <paper/tooling links or citations; keep short>

## Handoff
- Last completed: <what was last finished>
- Required context for next run: <minimum context to resume>
