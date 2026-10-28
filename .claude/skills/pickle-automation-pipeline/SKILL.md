---
name: pickle-automation-pipeline
description: Entry point for writing a new Pickle automation. Use whenever the user wants to write, add, or create an automation / test / test script for the Pickle app. Runs the 4-stage pipeline - collect docs (Jira, PRD, Figma), generate context, generate test cases, generate test script - and runs the pipeline stages in order with user approval gates.
---

# Pickle Automation Pipeline

Orchestrates the full flow from requirement documents to a runnable test script. Each stage is its own skill; invoke them in order with the Skill tool and **never skip a stage or a gate**.

## Workspace

All artifacts for one feature live in `automation_workspace/<feature-slug>/` (create it; `<feature-slug>` is kebab-case, confirm it with the user):

```
automation_workspace/<feature-slug>/
  sources.md        # stage 1 output: the collected documents
  context.md        # stage 2 output: consolidated context
  testcases.md      # stage 3 output: approved test cases
  (scripts go to tests/ and pickle_automation/pages/)
```

Write `status.md` in that folder after each stage (stage name, done/pending, date) so the pipeline can resume if interrupted. On start, if `automation_workspace/<feature-slug>/status.md` exists, offer to resume from the first incomplete stage.

## Stages

| # | Skill | Gate before the stage |
|---|-------|-----------------------|
| 1 | `pickle-collect-docs` | none - starts immediately |
| 2 | `pickle-generate-context` | **Ask permission** to generate context from the collected docs |
| 3 | `pickle-generate-testcases` | Show the context summary; user confirms it before test cases |
| 4 | `pickle-generate-testscript` | User approves the test cases. Stage 4 first calls `pickle-inspect-screen` to read real selectors from the running app, then generates the script, then asks for runtime inputs (phone number etc.) **before running** |

## Rules

- Announce the stage you are entering ("Stage 2/4: generating context") and the stage you finished.
- If the user says to stop or revise, stay in the current stage; do not advance.
- Never invent requirements. Anything not in the documents is an open question for the user.
- Secrets/PII (phone numbers, OTPs, tokens) are only ever passed as environment variables at run time; never written into committed files.

## Setup is separate (never part of a run)

Machine setup and adding an app build are **standalone, one-time skills** (`pickle-setup-environment`, `pickle-add-app`). Do **not** invoke them from this pipeline and do not ask the user about them at the start of a run. Only if a run fails because the environment or APK is missing or broken, say which standalone skill to run and stop there.

Helpers used during stage 4:

| Skill | Use for |
|-------|---------|
| `pickle-inspect-screen` | **Always called first in stage 4**: read real selectors from the running app before writing page objects |
| `pickle-run-tests` | Boot emulator + Appium when they are not running; run tests, report per TC |
