# Skill Routing Examples

Use these examples to resolve ambiguous prompts when hot-path routing alone is insufficient.

## Ambiguous Intent Examples

1. Prompt: "Can you sanity-check this implementation and summarize where it diverges from the spec?"
- Route: `Algo Verifier`
- Why: primary intent is semantic compliance validation, not note capture.

2. Prompt: "I need a concise prompt for deep literature synthesis on this topic."
- Route: `Question Maker`
- Why: primary output is a delegated deep-research prompt.

3. Prompt: "These results are noisy; propose targeted ablations and then log a structured note."
- Route sequence: `Ablation Recommender` -> `Research Note Taker`
- Why: ablation design first, then normalization artifact.

4. Prompt: "The last skill flow was wrong; log the incident and then summarize this run."
- Route sequence: `Skill Reliability Keeper` -> domain skill (if needed) -> `Research Note Taker`
- Why: reliability-first sequencing is mandatory.

5. Prompt: "Map recurring request patterns and suggest whether we need a new skill."
- Route: `Observer`
- Why: pattern detection/new-skill opportunity evaluation.

## Sequencing Examples

1. Reliability + references:
- `Skill Reliability Keeper` -> `Reference Librarian`

2. Reliability + execution + notes:
- `Skill Reliability Keeper` -> substantive skill (for example `Research Cycle` or `Algo Implementer`) -> `Research Note Taker`

3. Plain checkpoint-only:
- `Research State Keeper (mode=checkpoint)`

## Usage Notes

- Treat these as precedence examples, not exhaustive policy.
- If an example conflicts with hot-path rules, hot-path rules win.
