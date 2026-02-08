---
name: "grd-research-deep-thinker"
description: "Structure ambiguous research decisions into options, tradeoffs, and a defensible recommendation"
---

# Codex GRD Skill: grd-research-deep-thinker

<when_to_use>
Use when a research decision is ambiguous, multiple methods are plausible, or the user asks for deeper reasoning before execution.
</when_to_use>

<source_of_truth>
Use `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` to align recommendations with stage goals.
</source_of_truth>

<clarification_rule>
If you are not sure what the user wants, ask for pseudocode or a concrete step-by-step outline before continuing.
</clarification_rule>

<execution_contract>
1. Define the decision question, constraints, and success criteria.
2. Generate 2-4 candidate approaches.
3. Evaluate tradeoffs: assumptions, expected impact, risk, effort, and time.
4. Recommend one approach with explicit rationale and known failure modes.
5. Propose the next smallest validating action.
6. Produce `.grd/research/DEEP_THINKING.md` when artifact output is requested.
</execution_contract>
