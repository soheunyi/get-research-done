---
name: "grd-research-hypothesis-designer"
description: "Define falsifiable hypotheses, metrics, and stop criteria for research phases"
---

# Codex GRD Skill: grd-research-hypothesis-designer

<when_to_use>
Use for hypothesis framing before writing experiment code.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` Stage 1.
</source_of_truth>

<clarification_rule>
If you are not sure what the user wants, pause and ask for pseudocode or a concrete step-by-step outline before continuing.
</clarification_rule>

<delivery_rule>
Default to concise chat output. Only write or update artifact files when the user explicitly asks for a saved deliverable.
</delivery_rule>

<execution_contract>
1. Write one falsifiable hypothesis.
2. Define baseline, metric, effect size, and decision threshold.
3. Define stop criteria and validity threats.
4. Produce `.grd/research/HYPOTHESIS.md`.
</execution_contract>
