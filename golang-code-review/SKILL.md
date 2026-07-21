---
name: golang-code-review
description: >-
  Use when the user asks for a Go/Golang code review, PR review of Go code,
  concurrent Go review, DDD/architecture review of a Go service, or Go security
  review — and this skill is explicitly attached or named (never auto-invoke).
disable-model-invocation: true
---

# Golang Code Review

Multi-agent Go review grounded in *100 Go Mistakes and How to Avoid Them*, official Go docs, concurrency pitfalls, security, and pragmatic DDD/hexagonal boundaries. Four specialist agents run in parallel; one final evaluator synthesizes. Deliverable is always `code-review.MD`.

## When to use

- User asks for code review / PR review of Go
- Skill is **attached or named** (do not auto-invoke)

## Workflow

```
Review Progress:
- [ ] Scope + evidence plan
- [ ] Optional: go vet / tests -race on changed packages
- [ ] Spawn 4 specialist agents in parallel
- [ ] Collect specialist findings (reject thin findings)
- [ ] Spawn final-evaluator
- [ ] Write code-review.MD from template
- [ ] Confirm path with user
```

### 1. Scope

Target: PR, branch diff, uncommitted changes, or named paths. Ask once if unclear. Prefer `git diff` / PR files over whole-repo reads.

Record in the report:

- Go module path / `go` version if visible (`go.mod`)
- Packages touched
- Whether concurrency, HTTP, SQL, or domain packages changed (drives empty-lens flags)

### 2. Evidence (parent agent)

Before or while specialists run, gather facts when the repo allows:

```bash
go vet ./<changed>/...
go test -race ./<changed>/...   # if feasible; note if skipped
```

Attach command output summaries to the final report under **Meta**. Do not block the review forever on slow tests — note what ran and what did not.

### 3. Four specialists in parallel

Same scope for each. Each **must read** its reference(s) and [finding-rubric.md](references/finding-rubric.md).

| Agent | Lens | Must read |
|-------|------|-----------|
| `quality` | Idioms, types, errors, stdlib, tests — *100 Go Mistakes* | [go-100-mistakes.md](references/go-100-mistakes.md), [finding-rubric.md](references/finding-rubric.md) |
| `security` | Authz, injection, secrets, HTTP defaults, vulns | [security.md](references/security.md), [finding-rubric.md](references/finding-rubric.md) |
| `architecture` | Boundaries, DDD, hexagonal, package design | [architecture-ddd.md](references/architecture-ddd.md), [finding-rubric.md](references/finding-rubric.md) |
| `concurrency` | Races, leaks, channels, context, sync | [concurrency.md](references/concurrency.md), [finding-rubric.md](references/finding-rubric.md) |

**Specialist prompt** (fill placeholders):

```
You are the <LENS> reviewer for Go code.
Scope: <diff summary + file list>
Read and follow: <reference paths>
Also follow: references/finding-rubric.md

Rules:
- Only this lens. No drive-by style nits outside the lens.
- Every finding needs: severity, location (path:line), issue, recommendation, example (Go snippet or before/after), and when applicable mistake_id (#N from 100 Go Mistakes) or cwe/rule id.
- Prefer concrete evidence from the diff over hypotheticals. Mark speculative items severity=low and label "speculative".
- If the change clearly engages this lens but you find nothing: say "No issues" AND list what you checked (5–10 bullets).
- Rank findings critical → nit.
```

### 4. Final evaluator

One agent after all four return. Inputs = full specialist outputs + Meta evidence.

```
You synthesize four Go review lenses into one coherent review.
Inputs: quality, security, architecture, concurrency findings + any vet/race notes.

Rules:
- Deduplicate; keep highest severity + richest recommendation
- Conflicts: correctness/safety/security > architecture purity > style
- Flag empty lens that should not be empty (e.g. new goroutines but concurrency said No issues without checklist)
- Produce: executive summary (3–5 bullets), overall verdict, merged ranked table, paste-to-requester draft
- Do not invent issues unsupported by specialists unless an empty lens missed an obvious risk — then add under Synthesis/Gaps with severity and label "evaluator-added"
```

### 5. Write `code-review.MD`

Overwrite workspace-root `code-review.MD` (or user path). Structure: [templates/code-review.MD](templates/code-review.MD).

Must include:

- Separate sections per lens + Synthesis
- Each finding points to `path:line` + recommendation + example
- **Paste to requester** block ready to copy
- Severities: `critical` | `high` | `medium` | `low` | `nit`

## Severity

| Level | Use when |
|-------|----------|
| critical | Exploit, data loss, deadlock, broken domain invariant in prod path |
| high | Likely bug, confirmed/plausible race, authz hole, wrong error handling on hot path |
| medium | Real risk under load/change; boundary leak that will hurt soon |
| low | Smell, missing test, speculative with weak evidence |
| nit | Naming/docs/clarity only |

## Hard rules

- Prefer [go.dev](https://go.dev/doc/) / Effective Go / Go memory model over folklore
- Quality findings cite `#N` from [go-100-mistakes.md](references/go-100-mistakes.md) when they map
- Do not invent APIs or packages not in the code
- Huge scope → prioritize changed files; list out-of-scope explicitly
- Never auto-invoke

## Additional resources

- [references/go-100-mistakes.md](references/go-100-mistakes.md)
- [references/concurrency.md](references/concurrency.md)
- [references/security.md](references/security.md)
- [references/architecture-ddd.md](references/architecture-ddd.md)
- [references/finding-rubric.md](references/finding-rubric.md)
- [references/sources.md](references/sources.md)
- [templates/code-review.MD](templates/code-review.MD)
