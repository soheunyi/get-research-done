# Verifier Handoff Contract

Default behavior:
- Suggest an optional follow-up with `Algo Verifier` after implementation.
- Do not run `Algo Verifier` unless the user explicitly asks.

Use triggered handoff context when implementation touches correctness-sensitive math paths.

Trigger handoff suggestion to `Algo Verifier` when changes touch:
- equations/transforms/distributions/parameterization
- pseudocode-to-code mapping of critical steps
- semantics of evaluation metrics or decision logic

Handoff context must include:
- pseudocode/spec path
- modified files
- expected semantic checks
