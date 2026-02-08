---
name: "grd-research-randomness-auditor"
description: "Audit seeds and nondeterminism sources to keep experiments reproducible and comparable"
---

# Codex GRD Skill: grd-research-randomness-auditor

<when_to_use>
Use when runs differ unexpectedly or when you need robust seed discipline before conclusions.
</when_to_use>

<source_of_truth>
Follow `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md` and produce `.grd/research/RANDOMNESS_AUDIT.md`.
</source_of_truth>

<execution_contract>
1. Enumerate RNG sources and seed propagation points.
2. Verify logged seed metadata and determinism settings.
3. Quantify seed variance on key metrics.
4. Output remediation checklist in `.grd/research/RANDOMNESS_AUDIT.md`.
</execution_contract>
