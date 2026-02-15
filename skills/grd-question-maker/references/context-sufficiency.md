# Context Sufficiency and Portability Contract

Use this file before finalizing any prompt.

## Required for All Prompts

- Objective: what user wants to learn/decide.
- Scope boundary: in-scope vs out-of-scope.
- Deliverable format: selected output format.
- Audience rigor: practical overview vs formal depth.

If any required field is missing, continue clarification before drafting unless user explicitly asks for assumption-based speed.

## Mode-Specific Requirements

### `deep_reasoning`
- Explicit definitions of terms/symbols.
- Domain/conditions.
- Objective claim or quantity to derive/estimate/prove.

### `lit_review`
- Topic boundary and inclusion/exclusion rules.
- Source expectations (for example: papers only, peer-reviewed preferred).
- Time window/horizon.
- Synthesis format (narrative/table/taxonomy/gaps).

## Portability Guard

Before final output:
1. Expand acronyms at first mention.
2. Replace internal shorthand with explicit method/task descriptions.
3. Include a standalone setup sentence containing:
- task objective
- data regime (snapshot-only vs sequence)
- selection target
- evaluation metric definitions
4. Run transfer check: "Is this prompt self-contained for a model with zero session context?"
5. If not unambiguously yes, revise before output.
