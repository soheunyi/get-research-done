# Prompt Output and Quality Spec

Use this file to enforce final prompt structure and quality.

## Core Draft Requirements

1. Draft one core question with optional sub-questions.
2. Add constraints (allowed methods, disallowed shortcuts, rigor/time bounds).
3. Specify expected answer format and success criteria.
4. Include ambiguity guardrails and common failure modes.
5. Include final section:
- `## User Additional Question (Optional)`
- `[User can add one extra question here.]`

## Mode-Specific Structure

For `deep_reasoning` prompts, make setup explicit:
- symbols and definitions
- domain/conditions
- objective function or target claim
- what prove/derive/estimate/bound means in context

For `lit_review` prompts, make research setup explicit:
- research question framing
- inclusion/exclusion criteria and source quality preference
- date range
- synthesis sections and citation requirements

## Artifact Structure (When Writing Files)

1. Format and Mode Declaration
2. Context Summary
3. Main Question
4. Definitions / Math Setup (deep reasoning)
5. Literature Review Scope and Search Strategy (lit review)
6. Constraints
7. Expected Answer Format
8. Success Criteria
9. Pitfalls To Avoid
10. User Additional Question (Optional)
11. Outcome Notes (optional, post-response)

## Quality Checks

- Remove vague terms unless operationalized.
- Expose assumptions explicitly.
- Ensure every symbol is defined once.
- Make evaluation/success criteria checkable where possible.
