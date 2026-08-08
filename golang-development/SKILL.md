---
name: golang-development
description: >-
  Use whenever developing, implementing, coding, fixing, refactoring, or
  extending Go/Golang — including executing an implementation plan that touches
  Go, shipping features, handlers, domain logic, concurrency, HTTP/SQL, tests,
  or packages. Always apply for Go implementation work. Skip for non-Go tasks
  or when the user only wants a code-review deliverable (use golang-code-review).
---

# Golang Development

Write idiomatic, safe Go. **This file is the always-on core**; everything else in [references/](references/) loads only when a gate below matches.

## Progressive disclosure

| Load | When |
|------|------|
| This `SKILL.md` | Always when the skill applies |
| [go-100-priority.md](references/go-100-priority.md) | **Light** mode — the short mistakes slice |
| [go-100-mistakes.md](references/go-100-mistakes.md) | **Full** mode — sections matching the work |
| Other references | Only when their gate matches |
| [discoveries-workflow.md](references/discoveries-workflow.md) | After the job, if proposing/logging discoveries |

## When this skill applies

- Go develop / implement / fix / refactor, or a plan step that changes Go
- Not for review markdown deliverables → `golang-code-review`
- Multi-service roots: use `context-discovery` for neighbor context first, then this skill for the Go work

## Choose mode (first)

**Light** when all are true: ≤~1 package / ≤~100 LOC; no new goroutines or shared mutable state; no new HTTP/SQL/authz/public surface and no security-sensitive config; no new packages, ports/adapters, or domain boundary moves.

**Full** when any light condition fails, or when unsure. **Escalate** light → full if those concerns appear mid-change, then open the matching gates.

| | Light | Full |
|---|--------|------|
| Mistakes catalog | [go-100-priority.md](references/go-100-priority.md) | Matching sections of [go-100-mistakes.md](references/go-100-mistakes.md) |
| Other references | Only if a gate fires | Every matching gate |
| Evidence | lint + vet + tests; `-race` if the package is already concurrent | lint + vet + `test -race`; `govulncheck` when new deps or security surface |
| Rubric / DoD | skip | rubric if large/risky; DoD if the user asks |

## Always-on standards

- Match repo package layout, names, error and logging style
- Handle errors; wrap with `%w` when callers need `Is`/`As`; no panic for expected failure
- Close resources; `return` after `http.Error` or a failed write
- `context.Context` first on IO/RPC boundaries; `defer cancel()` on derived contexts
- Every `go` has a stop plan — if you need one, you are probably in **full** mode
- No request identity in package globals; no string-built SQL; timeouts on new HTTP servers and clients
- Interfaces at the consumer; return concrete types; avoid new `utils`/`common` packages
- Behavior change gets a test that fails if reverted (table-driven + `t.Run` when ≥2 cases)
- Smallest change that solves the ask; do not invent APIs; cite `#N` when a catalog row guided the design
- Prefer [go.dev](https://go.dev/doc/) / Effective Go / [Code Review Comments](https://go.dev/wiki/CodeReviewComments); repo style wins for formatting

## Workflow

```
Development Progress:
- [ ] Mode: light | full
- [ ] Mistakes slice (priority or full sections)
- [ ] Orient: go.mod + neighboring code
- [ ] Open gated references if needed
- [ ] Implement + tests
- [ ] Evidence
- [ ] After finish: discoveries (optional)
- [ ] Done
```

### Evidence before "done"

```bash
# Prefer the repo's lint entrypoint when present
golangci-lint run ./<changed>/...   # or: staticcheck ./<changed>/...
go vet ./<changed>/...
go test ./<changed>/...             # light default
go test -race ./<changed>/...       # full, or light if already concurrent
govulncheck ./<changed>/...         # full + (new deps or security surface)
```

Failing lint, vet, or tests means not done. Note tool skips honestly.

## Reference gates

| Reference | Open when |
|-----------|-----------|
| [go-100-priority.md](references/go-100-priority.md) | Light mode, instead of the full catalog |
| [go-100-mistakes.md](references/go-100-mistakes.md) | Full mode — matched sections |
| [security.md](references/security.md) | Config that can weaken the system, or exploitable surfaces (HTTP/authz/SQL/SSRF/path/secrets/crypto) |
| [concurrency.md](references/concurrency.md) | Goroutines, channels, shared mutable state, `sync`, cancel design |
| [architecture-ddd.md](references/architecture-ddd.md) | New packages, ports/adapters, domain boundaries |
| [testing.md](references/testing.md) | Non-trivial tests, hermeticity, fuzz/bench, `TestMain`, concurrent tests |
| [dave-cheney.md](references/dave-cheney.md) | API shape, package naming, functional options, library goroutine policy |
| [sources.md](references/sources.md) | Authority conflict |
| [implementation-rubric.md](references/implementation-rubric.md) | Large or risky change — pre-ship self-check |
| [discoveries-workflow.md](references/discoveries-workflow.md) | After the job — propose or log discoveries |
| [definition-of-done.md](templates/definition-of-done.md) | User asks for a written DoD or handoff |

## Lens ownership

| Topic | Prefer |
|-------|--------|
| HTTP timeouts / body limits (#81) | security gate, else the always-on rule |
| WaitGroup / channels / ctx | concurrency |
| Interface-at-consumer / utils (#5–#7, #13) | architecture if boundaries move, else the mistakes catalog |
| Table-driven / hermetic tests | testing |
| Data races in app code | concurrency |

## Discoveries

After the job, if something reusable was learned, open [discoveries-workflow.md](references/discoveries-workflow.md). Log to the **project** file `.cursor/golang-discoveries.md`, never into this skill folder. Ask before appending.

## Done means

Mode chosen deliberately; always-on standards held; only needed references loaded; evidence green or skips noted; behavior changes covered by tests; discoveries proposed or explicitly none.

## Common failure modes

| Rationalization | Counter |
|-----------------|---------|
| Load the full catalog for a tiny fix | Use go-100-priority.md in light mode |
| Stay light after adding a worker or public API | Escalate and open the gates |
| Preload every reference | Gates only |
| "It compiles" means done | Lint + vet + tests required |
| Log discoveries inside the skill | Use `.cursor/golang-discoveries.md` |
| Skip neighbor context on multi-service work | Use context-discovery first |
