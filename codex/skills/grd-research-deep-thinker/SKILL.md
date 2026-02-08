---
name: "GRD Deep Thinker"
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

<delivery_rule>
Default to concise chat output. Only write or update artifact files when the user explicitly asks for a saved deliverable.
</delivery_rule>

<execution_contract>
1. Ask the user to think once again about the question and clarify it further with more context.
2. Define the decision question, constraints, and success criteria.
3. Generate 2-4 candidate approaches.
4. Evaluate tradeoffs: assumptions, expected impact, risk, effort, and time.
5. Recommend one approach with explicit rationale and known failure modes.
6. Propose the next smallest validating action.
7. Produce `.grd/research/DEEP_THINKING.md` when artifact output is requested.
</execution_contract>
