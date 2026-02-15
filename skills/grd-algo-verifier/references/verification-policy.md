# Verification Policy

Prefer semantic equivalence over textual similarity.

Always assess:
- step mapping coverage
- control-flow/data-flow parity
- invariant preservation
- behavior-impact severity

Confidence rubric:
- high: core steps and invariants match with direct evidence
- medium: likely match with partial evidence
- low: missing evidence or unresolved mismatch risk
