# Implementation Contract

Use this file for algorithm implementation details.

## Core Rules
- correctness before optimization
- vectorization first for batch/tensor/array operations; avoid elementwise Python loops on hot paths when equivalent vectorized ops exist
- deterministic defaults for seeds and ordering
- smallest testable slice first
- explicit assumptions and failure modes

## Vectorization-First Philosophy
- Prefer shape-stable tensor/array operations that make intent explicit and reduce interpreter overhead.
- If non-vectorized logic is required, document the reason (for example: unavoidable control dependence, memory constraints, or readability in non-hot path).
- After vectorization changes, add at least one shape/broadcast correctness check in tests.

## Required Outputs
- module/function mapping
- data contract mapping
- complexity + bottleneck summary
- focused tests for correctness + boundary cases

## Artifact
Write `.grd/research/ALGO_IMPLEMENTATION.md` when requested.
