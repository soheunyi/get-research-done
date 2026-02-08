---
name: "grd-research-idea-seeker"
description: "Search the web for relevant references, cite them, and generate evidence-backed research idea sketches"
---

# Codex GRD Skill: grd-research-idea-seeker

<when_to_use>
Use when user wants related work discovery, external references, or idea generation grounded in citations.
</when_to_use>

<source_of_truth>
Align ideas with `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` stage expectations.
</source_of_truth>

<clarification_rule>
Before searching, ask a short clarification question about scope, constraints, and desired output if missing.
</clarification_rule>

<delivery_rule>
Default to concise chat output. Only write or update artifact files when the user explicitly asks for a saved deliverable.
</delivery_rule>

<execution_contract>
1. Confirm topic scope and constraints (time, compute, risk tolerance, success metric).
2. Search web sources with priority on primary references (papers, official docs, benchmark sites, maintainer repos).
3. Filter to high-signal references that directly inform the user question.
4. Summarize each selected reference briefly with claim, method, and relevance.
5. Generate 3-5 research idea sketches linked to cited references.
6. For each sketch include: hypothesis, novelty angle, first experiment, risk, and decision metric.
7. Return a clear references list (title + URL) for every cited source.
8. Write `.grd/research/IDEA_SEEKER.md` when artifact output is requested.
</execution_contract>

<quality_bar>
- Distinguish evidence vs inference explicitly.
- Avoid uncited claims.
- Prefer recent and authoritative sources.
</quality_bar>
