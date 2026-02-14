<intent_lock_delta>
- Confirm implementation inputs, constraints, expected outputs, and acceptance checks.
- Require explicit artifact target/path before mutating files; if ambiguity could change behavior, resolve it before coding or tests.
</intent_lock_delta>

<output_format_delta>
Keep language execution-centric: concrete file paths, exact commands, and explicit done criteria.
6) Execution record
   - exact files/paths touched
   - command-level verification performed (or planned)
   - rollback note for the smallest reversible unit

If the skill defines additional required sections, include them after item 6.
</output_format_delta>

<action_policy_delta>
Execution emphasis:
- Before running mutating commands, restate the immediate goal and the minimal rollback path.
- Pre-mutation checklist:
  - what will change
  - where it will change
  - how success will be verified
  - how to revert minimally
</action_policy_delta>
