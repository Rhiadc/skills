# 100 Go Mistakes — Development Catalog

Primary public index: [100go.co](https://100go.co/) (Teiva Harsanyi, *100 Go Mistakes and How to Avoid Them*). Use `#N` when choosing designs or documenting gaps. This file is a **build cue sheet**, not a substitute for the book.

**Required:** Read this file for **every** Go implementation session (progressive disclosure exception). Other skill references stay gated.

**How to use:** Scan the sections that match what you are writing. Avoid each mistake; prefer patterns that prevent bugs/leaks over pure style.

---

## Code and project organization (#1–#16)

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 1 | Unintended variable shadowing | Prefer `=` over `:=` when updating outer `err`; watch nested blocks |
| 2 | Unnecessary nested code | Happy path left-aligned; early return |
| 3 | Misusing `init` | Prefer explicit setup in `main`/constructors; avoid hidden ordering |
| 4 | Overusing getters/setters | Export fields or methods that enforce invariants — not Java-style accessors |
| 5 | Interface pollution | Extract interfaces when a second consumer/test double needs them |
| 6 | Interface on the producer side | Define small interfaces at the consumer |
| 7 | Returning interfaces | Return concrete types; accept interfaces |
| 8 | `any` says nothing | Prefer real types or constraints |
| 9 | Confused about generics | Use generics for shared algorithms; don’t force them for one type |
| 10 | Type embedding pitfalls | Embed deliberately; watch promoted API surface |
| 11 | Not using functional options | Growing constructors → options pattern |
| 12 | Project misorganization | Domain-shaped packages; composition at `cmd` |
| 13 | Utility packages | Avoid growing `utils`/`common`; name by capability |
| 14 | Package name collisions | Avoid stdlib/keyword package names |
| 15 | Missing documentation | Doc comments on exported APIs |
| 16 | Not using linters | Wire `staticcheck`/`golangci-lint` when the team expects them |

## Data types (#17–#29)

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 17 | Octal literals confusion | Prefer `0o` form where clear |
| 18 | Integer overflows | Check casts; don’t use `float` for money |
| 19 | Floating-point misunderstanding | No `==` on floats; use decimals for currency |
| 20 | Slice length vs capacity | Logic on `len`, not mistaken `cap` |
| 21 | Inefficient slice init | `make([]T, 0, n)` when `n` known |
| 22 | Nil vs empty slice | Be deliberate for JSON/`omitempty`/API contracts |
| 23 | Checking slice empty wrong | Prefer `len(s) == 0` when both nil and empty mean empty |
| 24 | Slice copies incorrect | Mind `copy` lengths; avoid partial surprises |
| 25 | `append` side effects | Don’t append to shared backing arrays callers still own |
| 26 | Slice memory leaks | Copy out small windows from huge arrays when retaining |
| 27 | Inefficient map init | Size hint when known |
| 28 | Map memory leaks | Evict or avoid forever-growing pointer maps |
| 29 | Comparing values incorrectly | Don’t `==` structs with slices/maps; use cmp or custom |

## Control structures (#30–#35)

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 30 | Range copies elements | Index or pointer when mutating slice elements |
| 31 | Range arg evaluation | Know channel/array evaluated once |
| 32 | Pointers in range | Careful with `&v` of range var (pre-1.22 especially) |
| 33 | Map iteration assumptions | Never rely on order |
| 34 | `break` targets wrong loop | Use labels when breaking outer `for` from `switch`/`select` |
| 35 | `defer` inside loop | Defer outside loop or close explicitly each iteration |

## Strings (#36–#41)

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 36 | Not understanding runes | Index/decode Unicode correctly |
| 37 | Inaccurate string iteration | `for i, r := range s` for runes |
| 38 | Misusing trim | `TrimSuffix`/`TrimPrefix` vs charset trim |
| 39 | String concat under-optimized | `strings.Builder` in hot loops |
| 40 | Useless string conversions | Avoid repeated `string([]byte)` churn |
| 41 | Substring memory leaks | Copy when keeping small slice of huge string |

## Functions and methods (#42–#47)

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 42 | Wrong receiver type | Pointer for mutation / large structs; consistent style |
| 43 | Never named results | Name when clarity helps; don’t overuse |
| 44 | Named result side effects | Avoid naked returns with shadowing |
| 45 | Returning nil receiver | Don’t return typed-nil interfaces by accident |
| 46 | Filename as function input | Prefer `io.Reader`/`fs.File` for testability |
| 47 | `defer` arg evaluation | Remember args/receivers captured at defer time |

## Error management (#48–#54)

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 48 | Panicking | Return errors for expected failures |
| 49 | When to wrap | Wrap with `%w` when `Is`/`As` needed; add context |
| 50 | Error type compare wrong | Use `errors.As` |
| 51 | Error value compare wrong | Use `errors.Is` |
| 52 | Handling error twice | Log **or** return — not both without intent |
| 53 | Not handling error | Never `_ =` on meaningful errors |
| 54 | Not handling defer errors | Check `Close()`/`Rollback()` (named return or explicit) |

## Concurrency foundations (#55–#61)

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 55 | Concurrency vs parallelism | Design with clear intent |
| 56 | Concurrency always faster | Measure; don’t spam goroutines for tiny CPU work |
| 57 | Channels vs mutexes | Mutex for shared state; channels for ownership/pipelines |
| 58 | Data race vs race condition | Synchronize memory; design out order bugs |
| 59 | Workload type impacts | Bound workers; respect `GOMAXPROCS` for CPU-bound |
| 60 | Misunderstanding contexts | Cancel/deadline first-class; values sparingly |
| 61 | Inappropriate context propagation | Don’t use request ctx for post-handler async work |

## Concurrency practice (#62–#74)

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 62 | Goroutine with no stop plan | Always ctx/Done/Wait/Close |
| 63 | Goroutines + loop variables | Capture loop vars safely (audit pre-1.22 patterns) |
| 64 | `select` determinism | Don’t assume fair select; include cancel |
| 65 | Notification channels | Prefer `chan struct{}` for signals |
| 66 | Nil channels | Use nil chan to disable select cases |
| 67 | Channel size confusion | Document buffer sizes; avoid unbounded growth |
| 68 | String formatting side effects | Avoid `fmt` on types that lock/mutate |
| 69 | Data races with `append` | No concurrent append on same slice |
| 70 | Mutex + slices/maps | Copy under lock when publishing snapshots |
| 71 | Misusing `WaitGroup` | `Add` before `go`; always `Done` |
| 72 | Forgetting `sync.Cond` | Use Cond only when it truly fits |
| 73 | Not using `errgroup` | Prefer errgroup for N tasks + cancel-on-error |
| 74 | Copying a `sync` type | Pass pointers; don’t value-copy Mutex/WaitGroup |

## Standard library (#75–#81)

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 75 | Wrong time duration | Always use `time.Duration` constants |
| 76 | `time.After` leaks | Prefer timers you can `Stop` in loops |
| 77 | JSON mistakes | Explicit tags; mind `omitempty` and pointers |
| 78 | SQL mistakes | Context-aware APIs; pool correctly; safe `IN` |
| 79 | Not closing resources | Close HTTP bodies, `sql.Rows`, files |
| 80 | No `return` after HTTP error write | Always return after `http.Error` / failed write |
| 81 | Default HTTP client/server | Always set timeouts |

## Testing (#82–#90)

**Primary owner:** `tests` lens — see [testing.md](testing.md) and Cheney [Prefer table driven tests](https://dave.cheney.net/2019/05/07/prefer-table-driven-tests). Quality work should not dump these; implement via tests lens.

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 82 | Not categorizing tests | Gate heavy tests with short/tags |
| 83 | Not enabling race flag | Run concurrent packages under `-race` |
| 84 | Parallel/shuffle modes | Use `-parallel`/`-shuffle` wisely; fix order deps |
| 85 | Not table-driven | Prefer tables + `t.Run` for shared harness |
| 86 | Sleeping in unit tests | Sync with channels/`sync`/fakes |
| 87 | Time API in tests | Inject clock seams |
| 88 | Not using httptest/iotest | Prefer stdlib test helpers |
| 89 | Inaccurate benchmarks | Discipline `b.N`; watch DCE |
| 90 | Missing testing features | Use subtests, helpers, `t.Cleanup` |

## Optimizations (#91–#100)

Only apply when hot path, alloc-sensitive, or claiming performance.

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 91 | CPU caches | Profile before assuming |
| 92 | False sharing | Separate hot atomics/fields when contended |
| 93 | Instruction-level parallelism | Don’t micro-opt without measurement |
| 94 | Data alignment | Unusual packing only with evidence |
| 95 | Stack vs heap | Check escape analysis on hot paths |
| 96 | Reducing allocations | Cut needless copies; `sync.Pool` only when proven |
| 97 | Inlining | Don’t over-split tiny hot funcs without profiles |
| 98 | Diagnostics tooling | Use pprof/trace in perf debates |
| 99 | GC impacts | Avoid alloc storms / huge pointer graphs |
| 100 | Go in Docker/K8s | Align `GOMAXPROCS` with container CPU limits |

---

## Priority when time-boxing

1. Errors (#48–#54), resources (#79), HTTP defaults (#81)
2. Concurrency (#58–#74), slice/map sharing (#25–#28, #69–#70)
3. Interfaces/organization (#5–#7, #12–#13)
4. Tests for concurrent/IO changes (#83–#86) — **tests** lens
5. Optimizations (#91–#100) only with evidence

Quality work: prioritize #1–#54 and #75–#81; leave #82–#90 to **tests** unless a single cross-link helps.

## Citation format

```
mistake_id: #62
issue: goroutine started in constructor with no cancellation path
recommendation: accept context (or expose Close) and exit on ctx.Done()
```
