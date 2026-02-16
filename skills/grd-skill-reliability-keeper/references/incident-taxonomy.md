# Incident Taxonomy and Dual Verification

Use this file to classify incidents and verify reliability claims.

## Incident Classes

- routing/sequencing
- suggestion quality
- context portability
- artifact integrity
- metadata/timestamp
- safety gating
- contract mismatch

## Per-Class Dual Verification

For each applicable class, record:
1. Contract check:
- Does target skill contract include the expected guardrail/rule?
- Record pass/fail with confidence.
2. Behavior check:
- Do observed outputs/artifacts show the rule was followed?
- Record pass/fail with confidence.
3. Missing evidence notes:
- What evidence is unavailable?
- What concrete follow-up check resolves uncertainty?

## Routing/Sequencing Evidence Checklist

For `routing/sequencing` incidents, include:
- matched trigger phrase (or explicit "no deterministic match")
- pre-edit routing announcement evidence (exact line, or explicit absence)
- first mutated artifact/path
- ordering check: note capture happened before state/checkpoint mutation
- follow-up evidence hook (for example, route trace line in response plus log entry reference)

## Context Portability Specific Checks

Contract must include portability guardrails for context-free transfer.
Behavior evidence must show:
- expanded terms at first mention,
- explicit setup sentence with objective/regime/selection target/metrics,
- prompt understandable with zero prior session context.

## Incident Record Minimum Fields

- triggering request/context
- expected behavior (contract)
- observed behavior
- reproduction steps
- root-cause hypothesis
- desired behavior/improvement request
- minimal fix recommendation
- follow-up signal to improve skill contract/prompt
