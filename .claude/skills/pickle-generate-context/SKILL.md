---
name: pickle-generate-context
description: Only invoked by pickle-automation-pipeline (do not start it directly, so the approval gates are not skipped). Stage 2 of the Pickle automation pipeline. After asking the user's permission, consolidates Jira, PRD and Figma sources into a single context.md (flows, screens, rules, open questions). Use after pickle-collect-docs.
---

# Stage 2 - Generate context

## Permission gate (mandatory)

Before reading further or writing anything, ask via AskUserQuestion:

> "I've collected: <list of sources and their status>. Generate the automation context from these documents?"
> Options: **Yes, generate** / **No, let me add or change documents first**

If "No", return to `pickle-collect-docs` for the requested changes. Do not proceed without an explicit yes.

## Generate

Read `automation_workspace/<feature-slug>/sources.md` and the existing code (`pickle_automation/pages/`, `tests/`, `pickle_automation/config.py`) so the context reflects what is already automated. Write `context.md`:

```markdown
# Context - <feature>
## Goal            (1-3 sentences)
## User flows      (numbered steps per flow, from PRD + Figma)
## Screens         (name, key elements, Figma node if known)
## Business rules & acceptance criteria   (each tagged with its source: Jira/PRD/Figma)
## Test data needs (accounts, phone numbers, OTP handling, images, environments)
## Existing automation (page objects/tests that can be reused)
## Conflicts       (where sources disagree)
## Open questions  (anything unspecified - never guess)
```

## Gate out

Show the user a short summary (flows count, rules count, open questions). Ask them to answer open questions or confirm the context. Fold answers into `context.md`. Only then move to `pickle-generate-testcases`.
