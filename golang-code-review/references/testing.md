# Tests lens (Go)

Own **test design, coverage of the change, hermeticity, and CI-relevant flags**. Production concurrency bugs stay with the concurrency lens; you flag missing `-race` / sleep-as-sync / leak tests.

Authorities: [testing package](https://pkg.go.dev/testing), [go.dev Code Review Comments](https://go.dev/wiki/CodeReviewComments), [Prefer table driven tests](https://dave.cheney.net/2019/05/07/prefer-table-driven-tests) (Dave Cheney), *100 Go Mistakes* #82–#90, [fuzz tutorial](https://go.dev/doc/tutorial/fuzz).

## Triage order

1. Behavior change with no/weak tests for the new path
2. Table-driven / subtest shape (names, isolation, failure messages)
3. Hermeticity (time, network, FS, globals, order dependence)
4. Concurrent code: `-race`, no `Sleep` sync, goleak where workers exist
5. `TestMain`, fuzz, benchmarks only when relevant
6. Categorization (`testing.Short`, build tags) for heavy tests

---

## Must-cover the diff (#85 spirit + Cheney)

For each changed behavior in scope, ask:

- [ ] Is there a test that would fail if this change were reverted?
- [ ] Happy path **and** at least one error / boundary case?
- [ ] Table-driven when ≥2 cases share harness ([Cheney](https://dave.cheney.net/2019/05/07/prefer-table-driven-tests))?
- [ ] Subtests via `t.Run` so one failure doesn’t hide siblings?

```go
// GOOD: named table + subtests + clear diff (prefer go-cmp for structs)
func TestSplit(t *testing.T) {
    tests := map[string]struct {
        input, sep string
        want       []string
    }{
        "simple":       {input: "a/b/c", sep: "/", want: []string{"a", "b", "c"}},
        "trailing sep": {input: "a/b/c/", sep: "/", want: []string{"a", "b", "c"}},
    }
    for name, tc := range tests {
        t.Run(name, func(t *testing.T) {
            got := Split(tc.input, tc.sep)
            if diff := cmp.Diff(tc.want, got); diff != "" {
                t.Fatalf("mismatch (-want +got):\n%s", diff)
            }
        })
    }
}
```

**Severity:** production behavior change with no test for the new path → **medium** (or **high** if authz/money/data integrity). Style-only table-driven nits → **nit**.

---

## Assertions and helpers

Go stdlib has no assertion library on purpose ([FAQ](https://go.dev/doc/faq#testing_framework)) — prefer clear `t.Fatalf` / `t.Errorf` and keep running sibling cases via subtests.

- [ ] `t.Helper()` on test helpers so failures point at the caller
- [ ] Prefer `cmp.Diff` / `%#v` over opaque `DeepEqual` failures on nested structs
- [ ] Avoid third-party assert libs that abort the whole table on first failure unless team standard

---

## Hermeticity (#86, #87)

| Smell | Prefer |
|-------|--------|
| `time.Sleep` to “wait for goroutine” | channel, `sync`, or fake clock / ready signal (#86) |
| Hard-coded `time.Now` in logic under test | inject clock / `func() time.Time` seam (#87) |
| Real network/DB in unit tests | `httptest`, `iotest`, interfaces + fakes (#88) |
| Order-dependent package state | isolate; map-iterated tables help surface this (Cheney) |
| Shared mutable globals across tests | reset in `t.Cleanup` or avoid |

---

## Concurrency in tests (#83, #86)

Own these; leave production race *fixes* to concurrency lens:

- [ ] Packages that start goroutines: reviewed under `go test -race` (or note CI gap) (#83)
- [ ] Leak checks: [goleak](https://github.com/uber-go/goleak) for worker packages
- [ ] No `Sleep` as synchronization (#86)

---

## TestMain traps (Cheney)

`TestMain` **must** call `m.Run()` (directly or via a helper that does). Commenting out `goleak.VerifyTestMain(m)` and leaving an empty `TestMain` means **no tests run** — silent green.

```go
// BAD: tests never execute
func TestMain(m *testing.M) {
    // goleak.VerifyTestMain(m)
}

// GOOD
func TestMain(m *testing.M) {
    goleak.VerifyTestMain(m) // calls m.Run internally
}
```

Cite: [TestMain can cause one to question reality](https://dave.cheney.net/2024/02/22/microblog-testmain-can-cause-one-to-question-reality).

---

## Categorization & CI (#82, #84)

- [ ] Slow/integration tests gated with `testing.Short()` or build tags (#82)
- [ ] Flakes from hidden order deps — consider `-shuffle` awareness (#84)
- [ ] Parallel: `t.Parallel()` only when safe (no shared mutable fixtures)

---

## Fuzz & benchmarks

- **Fuzz:** parsers, codecs, validators, anything taking untrusted bytes — seed with `f.Add`, assert invariants ([tutorial](https://go.dev/doc/tutorial/fuzz))
- **Benchmarks (#89):** only when PR claims performance or touches hot path; require `b.N` discipline, `ReportAllocs` when allocs matter; flag dead-code elimination / wrong timer placement

---

## What not to demand

- 100% line coverage as a goal (Cheney: coverage ≠ case coverage)
- Full DDD test pyramid on tiny CLIs
- Rewriting green, readable one-off tests into tables “for purity” unless adding cases

---

## Finding format

State: **behavior/risk under test** → **gap or anti-pattern** → **concrete test sketch** (table row or `t.Run` name). Map `#82`–`#90` when applicable. Link Cheney posts when the fix is idiomatic table/subtest/`TestMain` guidance.
