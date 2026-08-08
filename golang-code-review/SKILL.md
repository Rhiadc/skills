---
name: golang-code-review
description: >-
  Use when the user asks for a Go/Golang code review, PR review, pull-request
  or diff review of Go code, concurrent Go review, DDD/architecture review of a
  Go service, Go security review, Go test/coverage review, -race / govulncheck
  feedback, or wants a code-review.md deliverable — and this skill is
  explicitly attached or named (never auto-invoke).
disable-model-invocation: true
---

# Golang Code Review

Multi-agent Go review grounded in *100 Go Mistakes*, official Go docs, [Dave Cheney](https://dave.cheney.net/), concurrency, security, tests, and pragmatic DDD/hexagonal boundaries. Specialists run in parallel; the parent writes the deliverable after a final evaluator merges. Deliverable is always a filled review markdown file.

## When to use

- User asks for code review / PR / diff review of Go
- Skill is **attached or named**

## When NOT to use

- Non-Go changes (or Go is incidental generated stubs only)
- User wants a one-line opinion on a single snippet (answer in chat; skip multi-agent)
- Skill not attached — do not auto-invoke
- User wants code written → `golang-development`

## Workflow

```
Review Progress:
- [ ] Scope + mode (full | lite); obtain the actual diff
- [ ] Optional: context brain if multi-service PR
- [ ] Evidence: lint / vet / test -race / govulncheck on changed packages
- [ ] Spawn specialists in parallel (sequential fallback if Task unavailable)
- [ ] Collect findings (reject thin; re-ask once if needed)
- [ ] Spawn final-evaluator
- [ ] Parent writes review file from template
- [ ] Confirm path with user
```

### 1. Scope + mode

Target: PR, branch diff, uncommitted changes, or named paths. Ask once if unclear.

**Obtain the actual diff** (`git diff`, `git diff main...HEAD`, or `gh pr diff`) and pass the file list plus hunks or a faithful summary to every specialist. Prefer the diff over whole-repo reads.

**Full mode** (default when unsure): all five specialists.

**Lite mode** — use when the diff is small (roughly ≤1 package / ≤~100 LOC) **and** no new goroutines, HTTP/SQL surfaces, authz, or domain boundary moves:

- Run `quality` + `tests` + `security` only
- Skip `architecture` and `concurrency` unless the diff clearly engages them
- `quality` may use [go-100-priority.md](references/go-100-priority.md) instead of the full catalog
- Still run final-evaluator on whatever returned

**Multi-service PRs:** if the workspace root has `context-brain/`, skim its `index.md` + `map.md` and the in-scope service sections (see `context-discovery`) before judging cross-service contract changes.

Record in the report:

- Go module path / `go` version (`go.mod`)
- Packages touched; mode (full | lite)
- Whether concurrency, HTTP, SQL, domain, or `_test.go` changed

### 2. Evidence (parent agent)

Prefer the repo's lint entrypoint when present, matching what `golang-development` runs:

```bash
golangci-lint run ./<changed>/...   # or: staticcheck ./<changed>/...
go vet ./<changed>/...
go test -race ./<changed>/...      # note if skipped
govulncheck ./<changed>/...        # note if skipped / not installed
```

Attach command output summaries under **Meta**. Do not block forever on slow tests — note what ran and what did not.

### 3. Specialists in parallel

Launch with the **Task** tool in one turn (parallel). Same scope and diff for each. Each **must read** its reference(s) and [finding-rubric.md](references/finding-rubric.md).

**If the Task tool is unavailable**, run the lenses sequentially in-process with the same prompts and references, and note "sequential fallback" under Meta. Do not silently drop lenses.

| Agent | Lens | Must read |
|-------|------|-----------|
| `quality` | Idioms, types, errors, stdlib — *100 Go Mistakes* + Cheney API/package cues | [go-100-mistakes.md](references/go-100-mistakes.md), [dave-cheney.md](references/dave-cheney.md), [finding-rubric.md](references/finding-rubric.md) |
| `tests` | Test design, coverage of the change, hermeticity, fuzz/bench | [testing.md](references/testing.md), [finding-rubric.md](references/finding-rubric.md) |
| `security` | Authz, injection, secrets, HTTP defaults, vulns | [security.md](references/security.md), [finding-rubric.md](references/finding-rubric.md) |
| `architecture` | Boundaries, DDD, hexagonal, package design | [architecture-ddd.md](references/architecture-ddd.md), [dave-cheney.md](references/dave-cheney.md) (package names), [finding-rubric.md](references/finding-rubric.md) |
| `concurrency` | Races, leaks, channels, context, sync | [concurrency.md](references/concurrency.md), [dave-cheney.md](references/dave-cheney.md) (goroutine lifetime), [finding-rubric.md](references/finding-rubric.md) |

**Lens ownership** (reduce dupes):

| Topic | Owner |
|-------|--------|
| HTTP timeouts / body limits (#81) | `security` |
| WaitGroup / channels / ctx cancel | `concurrency` |
| Interface-at-consumer / utils packages (#5–#7, #13) | `architecture` (quality only if not a boundary issue) |
| Missing/weak tests for the change; table-driven shape | `tests` |
| Production data race in app code | `concurrency` (`tests` only flags missing `-race`/leak tests) |

**Specialist prompt** (fill placeholders; include absolute paths to refs):

```
You are the <LENS> reviewer for Go code.
Scope: <diff summary + file list>
Mode: <full|lite>
Read and follow: <reference paths>
Also follow: <abs>/references/finding-rubric.md

Rules:
- Base every finding on the actual diff provided (hunks/paths, or run git show). Do not review unrelated files.
- Only this lens. No drive-by style nits outside the lens.
- Every finding needs: severity, location (path:line), issue, recommendation, example (Go snippet or before/after), and when applicable mistake_id (#N), Cheney post, or cwe/rule id.
- Prefer concrete evidence from the diff over hypotheticals. Mark speculative items severity=low and label "speculative".
- If the change clearly engages this lens but you find nothing: say "No issues" AND list what you checked (5–10 bullets tied to files/symbols in the diff).
- Rank findings critical → nit. Cap nits at 5.
- Return findings using the Accept field shape from the rubric (so the parent can merge).
```

If a specialist returns thin findings, **re-ask once** with the Reject examples from the rubric. Then drop or keep.

### 4. Final evaluator

One agent after specialists return. Inputs = full specialist outputs + Meta evidence.

```
You synthesize Go review lenses into one coherent merge.
Inputs: quality, tests, security, architecture, concurrency (whichever ran) + lint/vet/race/govulncheck notes.

Rules:
- Deduplicate; keep highest severity + richest recommendation
- Conflicts: correctness/safety/security > tests proving the fix > architecture purity > style
- Flag empty lens that should not be empty
- Produce ONLY: executive summary (3–5 bullets), overall verdict, merged ranked table (with stable IDs Q#/T#/S#/A#/C#), paste-to-requester draft, conflicts, gaps/evaluator-added
- Do not invent issues unsupported by specialists unless an empty lens missed an obvious risk — then add under Gaps with severity and label "evaluator-added"
- Map severities into paste buckets: critical+high → Must; medium → Should; low+nit → Nits
- Verdict: any Must → request-changes; only Should/Nits → approve-with-nits; nothing or nits-only after judgment → approve
```

### 5. Parent writes the review file

**Parent agent** (not the evaluator) fills [templates/code-review.md](templates/code-review.md) using evaluator merge + specialist detail.

- Default path: ask once, else `code-review.md` at workspace root (or `code-review-<short-scope>.md` if a prior review exists)
- Overwrite only when the user confirms or path is unique to this review
- Repeat `### Qn` / `Tn` / … blocks per finding; for empty lenses keep the section with **No issues** + checklist
- Cap **Nits** in Paste at 5

Must include: per-lens sections + Synthesis, `path:line`, recommendation, example, Paste block, severities `critical|high|medium|low|nit`.

## Severity

| Level | Use when |
|-------|----------|
| critical | Exploit, data loss, deadlock, broken domain invariant in prod path |
| high | Likely bug, confirmed/plausible race, authz hole, wrong error handling on hot path |
| medium | Real risk under load/change; boundary leak; **behavior change with no/weak test** |
| low | Smell, speculative with weak evidence |
| nit | Naming/docs/clarity only |

### Paste buckets

| Severity | Paste section |
|----------|----------------|
| critical, high | Must address |
| medium | Should address |
| low, nit | Nits (optional) |

## Hard rules

- Prefer [go.dev](https://go.dev/doc/) / Effective Go / Go memory model / [Code Review Comments](https://go.dev/wiki/CodeReviewComments) over folklore
- Secondary: [Dave Cheney](https://dave.cheney.net/) via [dave-cheney.md](references/dave-cheney.md) — cite post titles, don't paste long excerpts
- Quality findings cite `#N` from [go-100-mistakes.md](references/go-100-mistakes.md) when they map; tests cite `#82`–`#90` when they map
- Do not invent APIs or packages not in the code
- Huge scope → prioritize changed files; list out-of-scope explicitly
- Never auto-invoke
- Specialists in **parallel** unless the user asks otherwise or Task is unavailable

## Common failure modes

| Rationalization | Counter |
|-----------------|---------|
| Review from memory without the diff | Obtain the diff and pass it to every specialist |
| Skip empty-lens checklist | Reject; re-ask that lens once |
| Architecture demands full DDD on a tiny fix | Follow architecture-ddd "When NOT" |
| Thin finding, fix later | Rubric reject — no entry without example |
| Task tool missing, so skip lenses | Sequential in-process fallback |
| Missing test is always "nit" | Behavior change without test → at least **medium** |
| Quality agent also dumps test nits | Hand off to `tests` lens |

## Additional resources

- [references/go-100-mistakes.md](references/go-100-mistakes.md)
- [references/go-100-priority.md](references/go-100-priority.md)
- [references/testing.md](references/testing.md)
- [references/concurrency.md](references/concurrency.md)
- [references/security.md](references/security.md)
- [references/architecture-ddd.md](references/architecture-ddd.md)
- [references/dave-cheney.md](references/dave-cheney.md)
- [references/finding-rubric.md](references/finding-rubric.md)
- [references/sources.md](references/sources.md)
- [templates/code-review.md](templates/code-review.md)
