# Ablation Policy

Use this file for detailed ablation design rules.

## Required Inputs
- target method/component inventory
- baseline definition
- run budget (time/compute)
- success metric and minimum meaningful effect

## Planning Heuristics
- prioritize by expected information gain per run
- avoid collinear/overlapping variants in early rounds
- include at least one sanity-control ablation
- enforce smallest informative run set first

## Required Fields Per Ablation
- component/factor
- hypothesis
- expected direction/magnitude
- priority and rationale
- minimum run count
