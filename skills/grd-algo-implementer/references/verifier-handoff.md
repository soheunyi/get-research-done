# Verifier Handoff Contract

Use this file when implementation touches correctness-sensitive math paths.

Trigger handoff suggestion to `Algo Verifier` when changes touch:
- equations/transforms/distributions/parameterization
- pseudocode-to-code mapping of critical steps
- semantics of evaluation metrics or decision logic

Handoff context must include:
- pseudocode/spec path
- modified files
- expected semantic checks
