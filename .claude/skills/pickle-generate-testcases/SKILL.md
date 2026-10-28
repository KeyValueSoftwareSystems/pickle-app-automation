---
name: pickle-generate-testcases
description: Only invoked by pickle-automation-pipeline (do not start it directly, so the approval gates are not skipped). Stage 3 of the Pickle automation pipeline. Turns context.md into structured, prioritized test cases (positive, negative, edge) in testcases.md and gets user approval. Use after pickle-generate-context.
---

# Stage 3 - Generate test cases

Input: `automation_workspace/<feature-slug>/context.md`. Output: `testcases.md`.

## Write cases

One block per case:

```markdown
### TC-001 - <short title>
- Priority: P0 | P1 | P2
- Type: smoke | regression | negative | edge
- Traces to: <acceptance criterion / rule from context.md>
- Preconditions:
- Test data: (use placeholders: <PHONE_NUMBER>, <OTP> - never real values)
- Steps:
  1. ...
- Expected result:
- Automate: yes | no (reason, e.g. needs real OTP / manual visual check)
```

Coverage: every acceptance criterion maps to at least one case; add negative (invalid phone, wrong/expired OTP, no network) and edge cases the documents imply. End the file with a traceability table (criterion -> TC ids) and list any criterion with no case.

Pytest markers in this repo are `mobile`, `smoke`, `regression`. Type maps to markers as: `smoke` -> `smoke`; `regression`, `negative` and `edge` -> `regression` (every automated test also gets `mobile`).

## Approval gate

Present a compact table (ID, title, priority, automate?). Ask via AskUserQuestion: **Approve all** / **Approve with changes** / **Regenerate**. Apply changes, and only proceed to `pickle-generate-testscript` with the approved set (let the user pick which cases to automate now).
