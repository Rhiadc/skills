# Discoveries workflow (gated)

Open **only after the job finishes**, when proposing or logging reusable Go learnings. Do not load at cold start.

## Where to log (project-local)

Append to the **workspace** file (never into the installed skill):

```text
.cursor/golang-discoveries.md
```

Create `.cursor/` and the file if missing. If the user prefers another path, use it once and remember for the session.

Do **not** write discoveries into `~/.cursor/skills/...` or this skill’s folder (symlink installs would mutate the shared skill).

## Timing

Propose discoveries **only after** implementation + evidence are done (or the user ends the task). Cap **at most 3** (light: usually 0–1). If nothing reusable: one line — “No discoveries this session.”

## What counts

Keep: reusable Go practice, recurring user corrections, `#N` / go.dev / Cheney clarifications that change next-time behavior.

Skip: ticket trivia, secrets, business rules, duplicates of SKILL/shared refs, speculation without evidence.

## Proposal format (chat)

```markdown
### Discovery: <short title>
- **Finding:** What happened or what we learned (from this job)
- **Why it matters:** Risk/cost if ignored next time
- **Importance:** high | medium | low — one clause
- **Rule for next time:** Prefer / avoid …
- **Target:** always-on | security | concurrency | architecture | testing | quality | tooling
- **Tags:** optional `#N`, `repo:`
```

Sort high → low importance.

## Write policy

1. Propose after the job (format above).
2. Append to `.cursor/golang-discoveries.md` only after user confirms (“log it” / “log all”).
3. **Promote** into this skill's always-on standards or its `references/` only when the user asks, or the same discovery is reinforced twice and they agree — then mark `promoted` in the log.

Prefer general rules over project paths; use `repo:` for project-specific notes.

## Entry template (prepend newest)

```markdown
## YYYY-MM-DD — <short title>

| | |
|--|--|
| Status | logged |
| Importance | high \| medium \| low |
| Target | always-on \| security \| concurrency \| architecture \| testing \| quality \| tooling |
| Tags | `#N` optional; `repo:` optional |
| Source | user-correction \| bug \| evidence-failure \| design-choice |

**Finding:** …

**Why it matters:** …

**Do instead:** …
```

## Promotion

Merge into the thinnest place (always-on bullet vs gated shared ref). Prefer **high** importance first. Do not bloat SKILL.md.
