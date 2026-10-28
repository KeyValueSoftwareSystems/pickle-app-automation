---
name: pickle-collect-docs
description: Only invoked by pickle-automation-pipeline (do not start it directly, so the approval gates are not skipped). Stage 1 of the Pickle automation pipeline. Asks the user, one at a time, for the Jira ticket, PRD, and Figma design, and records each in sources.md. Use when starting a Pickle automation or when documents are missing.
---

# Stage 1 - Collect documents

Collect the source documents **one input at a time**. Ask a single question, wait for the answer, record it, then ask the next. Use AskUserQuestion when the options are discrete (e.g. "provide / skip"), otherwise ask in plain text.

## Order

1. **Jira** - ticket key or URL (e.g. `PICK-123`).
2. **PRD** - link, file path in the repo, or pasted text.
3. **Figma** - design URL (frame/page link preferred).
4. **Anything else?** - optional extras (API docs, previous test cases). Skip if none.

For each input, the user may answer **"skip"** / "don't have it". Record it as `not provided` and continue; warn that gaps will be flagged as open questions later.

## Fetching content

- Local file path: read it with Read.
- Public URL: try WebFetch. If it requires auth, or an Atlassian/Figma tool is available in the session (MCP), use it. If neither works, tell the user and ask them to paste the relevant content (ticket description + acceptance criteria; PRD sections; Figma screen names and flows).
- Never claim you read a document you could not access.

## Output: `automation_workspace/<feature-slug>/sources.md`

```markdown
# Sources - <feature>
## Jira
- Reference: <key/url>
- Status: fetched | pasted | not provided
- Content: <title, description, acceptance criteria, verbatim or tightly trimmed>
## PRD
...
## Figma
- Screens/flows: <list>
...
```

Finish by showing the user a one-line status per source and hand off to the next stage (permission is requested by `pickle-generate-context`).
