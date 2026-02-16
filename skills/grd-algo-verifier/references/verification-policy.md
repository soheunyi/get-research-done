# Verification Policy

Prefer semantic equivalence over textual similarity.

Always assess:
- step mapping coverage
- control-flow/data-flow parity
- invariant preservation
- vectorization-first adherence for eligible batch/tensor/array paths
- behavior-impact severity

Vectorization-first checks:
- mark as deviation when elementwise loops replace equivalent vectorized operations on hot paths
- do not flag as deviation when non-vectorized logic is explicitly justified (for example: control dependence, memory limits, or non-hot-path readability)
- call out shape/broadcast risk when vectorization changes semantics

Confidence rubric:
- high: core steps and invariants match with direct evidence
- medium: likely match with partial evidence
- low: missing evidence or unresolved mismatch risk
