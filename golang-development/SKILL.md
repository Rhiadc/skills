---
name: golang-development
description: >-
  Use whenever developing, implementing, coding, fixing, refactoring, or
  extending Go/Golang — including executing an implementation plan that touches
  Go, shipping features, handlers, domain logic, concurrency, HTTP/SQL, tests,
  or packages. Always apply this skill for Go implementation work (not only
  reviews). Choose light mode for small Go changes and full mode when boundaries,
  concurrency, or exploitable surfaces are involved. Skip only for non-Go tasks
  or when the user only wants a code-review deliverable (use golang-code-review).
---

# Golang Development

Write idiomatic, safe Go. **SKILL.md is the always-on core.** Pick **light** or **full** mode first, then load references only as gates require — except [go-100-mistakes.md](references/go-100-mistakes.md), which is always required (depth differs by mode).

## Progressive disclosure + light mode

They work together:

| Layer | What it does |
|-------|----------------|
| **Light / full mode** | How much process and evidence to run |
| **Progressive disclosure** | Which reference files enter context |

Light mode still uses gates (usually none fire). Full mode still must **not** preload every ref — only matched gates.

Advisors / parallel Task reviewers: **not used**.

## Discoveries (self-improvement)

The skill improves when real work teaches something **reusable**. Capture that in [discoveries.md](references/discoveries.md), then promote proven items into always-on standards or a lens ref.

### Timing

Propose discoveries **only after the job is finished** (implementation + evidence done, or the user ends the task). Do not interrupt coding with discovery proposals. You may note candidates mentally (or briefly) while working; the proposal step runs at the end.

If nothing reusable was learned, say so in one line (“No discoveries this session”) — do not invent filler.

### What counts

Keep:

- Reusable Go practice (idioms, pitfalls, tooling, API shapes)
- Recurring corrections the user makes
- Clarifications of `#N` / go.dev / Cheney that changed how you should build next time

Skip:

- One-off ticket facts, secrets, proprietary business rules
- Things already clear in SKILL.md or an existing reference (link instead of duplicating)
- Speculative tips with no evidence from this session

Cap: **at most 3** proposals per session (light: usually 0–1). Rank by importance; drop the rest.

Do **not** open `discoveries.md` at task start. Open it only to dedupe before append, or when promoting.

### Proposal format (required)

Each proposal must **explain the finding** and **why it matters** — not just a title. Use this shape in chat:

```markdown
### Discovery: <short title>
- **Finding:** What happened or what we learned (concrete, from this job)
- **Why it matters:** Risk or cost if ignored next time (bug class, review fail, wasted time, security, etc.)
- **Importance:** high | medium | low — one clause justifying the rating
- **Rule for next time:** Prefer / avoid … (generalized)
- **Target:** always-on | security | concurrency | architecture | testing | quality | tooling
- **Tags:** optional `#N`, `repo:`
```

Sort proposals **high → low** importance. High = would likely cause a real bug, security issue, or repeated user correction; medium = solid maintainability/idiom; low = nice clarity only.

### Write policy

1. **Propose** after the job finishes, using the format above.
2. **Append** to [discoveries.md](references/discoveries.md) only after the user confirms (or says “log it” / “log all”).
3. **Promote** into SKILL.md or a lens file only when they ask, or when the same discovery is reinforced a second time and they agree — then set status to `promoted` and keep the log entry as history.

Prefer generalizing (“prefer X when Y”) over pasting project paths. Project-specific conventions go under a `repo:` tag and stay in discoveries until the user wants them always-on.

### Entry template (prepend newest at top of discoveries.md)

```markdown
## YYYY-MM-DD — <short title>

| | |
|--|--|
| Status | logged |
| Importance | high \| medium \| low |
| Target | always-on \| security \| concurrency \| architecture \| testing \| quality \| tooling |
| Tags | `#N` optional; `repo:` optional |
| Source | user-correction \| bug \| evidence-failure \| design-choice |

**Finding:** <what we learned from this job>

**Why it matters:** <risk/cost if ignored>

**Do instead:** <concrete preference or snippet cue>
```

### Promotion

When promoting: merge into the thinnest place that will work (always-on bullet vs gated ref). Prefer promoting **high** importance items first. Do not bloat SKILL.md — if it only matters for concurrency/security/tests, put it in that reference and mention the gate. Update [sources.md](references/sources.md) only if authority order changes.

## When this skill applies

- Any Go develop / implement / fix / refactor / “build this” ask
- Executing a plan (or plan step) that changes Go — load this skill **before** that step; pick light/full for that step
- Not for pure review markdown deliverables → `golang-code-review`
- Not for non-Go work

## Choose mode (do this first)

**Light** when **all** are true:

- Roughly ≤1 package and ≤~100 LOC changed (or a focused bugfix)
- No new goroutines / shared mutable state / channel designs
- No new HTTP/SQL/authz/public surface and no security-sensitive **config**
- No new packages, ports/adapters, or domain boundary moves

**Full** when any light condition fails, or when unsure → default **full**.

**Escalate** light → full mid-flight if you add concurrency, exploitable/config surface, or boundary changes. Then open the matching refs.

| | Light | Full |
|---|--------|------|
| Read SKILL.md | yes | yes |
| [go-100-mistakes.md](references/go-100-mistakes.md) | yes — **priority scan** (see below) | yes — scan all sections that match the work |
| Other refs | only if a gate unexpectedly matches | open every matching gate |
| Always-on standards | yes | yes |
| Tests for behavior change | yes | yes |
| Evidence | lint + vet + tests on touched pkgs; `-race` if any concurrent code exists in those pkgs | lint + vet + `test -race`; `govulncheck` if new deps or security surface |
| Rubric / DoD template | skip | rubric only if large/risky; DoD only if user asks |

### Priority scan (light mode — go-100-mistakes)

In light mode, read the catalog’s **Priority when time-boxing** section and the mistake rows for what you’re touching (usually errors #48–#54, resources #79, HTTP #80–#81, shadowing/nesting #1–#2). Do not study unrelated optimization chapters (#91–#100).

## Always-on standards (both modes)

- Match existing package layout, names, error/logging style in the repo
- Errors: handle them; wrap with `%w` when callers need `Is`/`As`; don’t panic for expected failure
- Close resources (HTTP bodies, `sql.Rows`, files); `return` after `http.Error` / failed writes
- `context.Context` as first param on IO/RPC boundaries; `defer cancel()` on derived contexts
- Every `go` has a stop plan — or don’t start it (if you need `go`, you’re probably in **full**)
- No request identity in package globals; no string-built SQL; timeouts on new HTTP servers/clients
- Interfaces at the **consumer**; return concrete types; avoid new `utils`/`common` packages
- Every behavior change gets a test that would fail if reverted (table-driven + `t.Run` when ≥2 cases)
- Smallest change that solves the ask; don’t invent APIs/packages not needed
- Map decisions to `#N` when they apply
- Prefer [go.dev](https://go.dev/doc/) / Effective Go / [Code Review Comments](https://go.dev/wiki/CodeReviewComments); repo style wins for formatting/naming

## Workflow

```
Development Progress:
- [ ] Pick mode: light | full (escalate if needed)
- [ ] Read go-100-mistakes.md (priority scan if light)
- [ ] Orient: go.mod + neighboring code
- [ ] Open gated refs only if mode/gates require
- [ ] Implement + tests
- [ ] Evidence for this mode
- [ ] Job finished → propose discoveries (explain finding + importance; ask before append)
- [ ] Done
```

### Orient

Read `go.mod`, touched packages, nearby patterns — enough to match the repo, not the whole module.

### Implement

Follow always-on standards + mistakes guidance. If a new concern appears, escalate mode and open that gate before continuing.

### Evidence before “done”

```bash
# Prefer repo lint entrypoint when present
golangci-lint run ./<changed>/...   # or: staticcheck ./<changed>/...
go vet ./<changed>/...
go test ./<changed>/...             # light default
go test -race ./<changed>/...       # full, or light if package already concurrent
govulncheck ./<changed>/...         # full + (new deps or security surface)
```

Do not claim done with failing lint, vet, or tests. Note tool skips honestly.

## Reference gates (full mode — and light only if escalated)

| Reference | Open when |
|-----------|-----------|
| [go-100-mistakes.md](references/go-100-mistakes.md) | **Always** (depth: light priority scan vs full matched sections) |
| [security.md](references/security.md) | Config that can weaken the system, or **exploitable** implementation (HTTP/authz/SQL/SSRF/path/secrets/crypto) |
| [concurrency.md](references/concurrency.md) | Goroutines, channels, shared mutable state, `sync`, cancel design |
| [architecture-ddd.md](references/architecture-ddd.md) | New packages, ports/adapters, domain boundaries |
| [testing.md](references/testing.md) | Non-trivial tests, hermeticity/fuzz/bench/`TestMain`, concurrent tests |
| [dave-cheney.md](references/dave-cheney.md) | API shape, package naming, functional options, library goroutine policy |
| [implementation-rubric.md](references/implementation-rubric.md) | Large/risky full-mode self-check |
| [sources.md](references/sources.md) | Authority conflict |
| [discoveries.md](references/discoveries.md) | Logging, deduping, or promoting a discovery — never at cold start |
| [templates/definition-of-done.md](templates/definition-of-done.md) | User asks for written DoD / handoff |

## Lens ownership (when multiple concerns apply)

| Topic | Prefer |
|-------|--------|
| HTTP timeouts / body limits (#81) | `security` if gate open; else always-on |
| WaitGroup / channels / ctx | `concurrency` |
| Interface-at-consumer / utils (#5–#7, #13) | `architecture` if boundaries move; else mistakes catalog |
| Table-driven / hermetic tests | `testing` |
| Data races in app code | `concurrency` |

## Done means

- Mode chosen deliberately (and escalated if needed)
- Always-on standards held; relevant `#N` avoided
- Only necessary refs loaded
- Evidence for that mode is green (or skips noted)
- Behavior change covered by tests
- After finish: discoveries proposed with finding + why it matters + importance (or explicitly none)

## Common failure modes

| Rationalization | Counter |
|-----------------|---------|
| Skip mistakes catalog in light mode | Still required — use priority scan |
| Stay in light after adding a worker/API | Escalate to full + open gates |
| Preload every reference in full | Gates only |
| “It compiles” = done | Lint + vet + tests required |
| Full DDD on a tiny fix | Stay light; don’t open architecture |
| Missing test is a nit | Behavior change without test → not done |
| Silent skill edits | Ask before append/promote discoveries |
| Dump session notes into SKILL.md | Log first; promote only when reinforced or requested |
| Preload discoveries.md every run | Open only to log/dedupe/promote |
