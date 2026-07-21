# 100 Go Mistakes — Review Catalog

Primary public index: [100go.co](https://100go.co/) (Teiva Harsanyi, *100 Go Mistakes and How to Avoid Them*). Use `#N` in findings. This file is a **review cue sheet**, not a substitute for the book.

**How to use:** Scan the sections that match the diff. For each hit, cite `#N`, state evidence, and give a concrete fix. Prefer mistakes that cause bugs/leaks over pure style.

---

## Code and project organization (#1–#16)

| # | Mistake | Look for / ask |
|---|---------|----------------|
| 1 | Unintended variable shadowing | `err :=` / `:=` inside nested blocks hiding outer vars |
| 2 | Unnecessary nested code | Happy-path nesting; prefer early return |
| 3 | Misusing `init` | Side effects, hidden ordering, hard-to-test setup in `init` |
| 4 | Overusing getters/setters | Java-style accessors with no invariant |
| 5 | Interface pollution | Tiny interfaces invented with one impl, no consumers yet |
| 6 | Interface on the producer side | Interfaces defined next to impl instead of consumer |
| 7 | Returning interfaces | Returning `io.Reader`/`interface` when concrete type is fine |
| 8 | `any` says nothing | `any`/`interface{}` where a real type or constraint fits |
| 9 | Confused about generics | Generics for one type; or copy-paste where generics help |
| 10 | Type embedding pitfalls | Promoted methods leaking API; ambiguous promotion |
| 11 | Not using functional options | Brittle constructors with many bool/config params |
| 12 | Project misorganization | Unclear packages; everything in `main` or random folders |
| 13 | Utility packages | Growing `utils`/`common` with no domain meaning |
| 14 | Package name collisions | Import rename wars; package name = language keyword/stdlib |
| 15 | Missing documentation | Exported APIs with no doc comments |
| 16 | Not using linters | No `staticcheck`/`golangci-lint` where team expects it |

## Data types (#17–#29)

| # | Mistake | Look for / ask |
|---|---------|----------------|
| 17 | Octal literals confusion | `0644`-style ints misread; prefer `0o` where clear |
| 18 | Integer overflows | Unchecked casts; `int` size assumptions; money as `float` |
| 19 | Floating-point misunderstanding | `==` on floats; decimals for currency |
| 20 | Slice length vs capacity | Logic using `cap` wrongly; unclear growth |
| 21 | Inefficient slice init | Append in loop without `make([]T, 0, n)` when `n` known |
| 22 | Nil vs empty slice | JSON/`omitempty`/API contracts broken by nil vs `[]` |
| 23 | Checking slice empty wrong | Prefer `len(s) == 0` over nil-only checks when both empty |
| 24 | Slice copies incorrect | `copy` length bugs; partial copies |
| 25 | `append` side effects | Append to shared backing array mutating callers |
| 26 | Slice memory leaks | Reslicing huge arrays keeping backing array alive |
| 27 | Inefficient map init | Growing map in loop without size hint when known |
| 28 | Map memory leaks | Pointers/refs kept in maps forever |
| 29 | Comparing values incorrectly | Comparing structs with slices/maps; `==` on incomparable |

## Control structures (#30–#35)

| # | Mistake | Look for / ask |
|---|---------|----------------|
| 30 | Range copies elements | Mutating range var expecting to change slice elements |
| 31 | Range arg evaluation | Channel/array evaluated once — surprising lifetimes |
| 32 | Pointers in range | Taking `&v` of range variable (pre-1.22 especially) |
| 33 | Map iteration assumptions | Relying on order; insert-during-range surprises |
| 34 | `break` targets wrong loop | `break` from `switch`/`select` not outer `for` |
| 35 | `defer` inside loop | Defers pile up until function end — leaks/handles |

## Strings (#36–#41)

| # | Mistake | Look for / ask |
|---|---------|----------------|
| 36 | Not understanding runes | Indexing string as bytes for Unicode |
| 37 | Inaccurate string iteration | `for i := range s` vs `for i, r := range s` |
| 38 | Misusing trim | `TrimRight`/`TrimLeft` charset vs `TrimSuffix`/`TrimPrefix` |
| 39 | String concat under-optimized | `+` in hot loops; prefer `Builder` |
| 40 | Useless string conversions | Repeated `string([]byte)` / `[]byte(string)` |
| 41 | Substring memory leaks | Large string kept alive by small substring |

## Functions and methods (#42–#47)

| # | Mistake | Look for / ask |
|---|---------|----------------|
| 42 | Wrong receiver type | Value receiver mutating copy; huge structs by value |
| 43 | Never named results | Missed clarity in multi-return; or overuse |
| 44 | Named result side effects | Naked returns + shadowing bugs |
| 45 | Returning nil receiver | `var p *T; return p` → typed nil interface pitfalls |
| 46 | Filename as function input | Prefer `io.Reader`/`fs.File` for testability |
| 47 | `defer` arg evaluation | Defer captures args/receivers at defer time |

## Error management (#48–#54)

| # | Mistake | Look for / ask |
|---|---------|----------------|
| 48 | Panicking | Panic for expected failures; unrecovered in libraries |
| 49 | When to wrap | Lost context; or wrap without `%w` when `Is`/`As` needed |
| 50 | Error type compare wrong | Type assert instead of `errors.As` |
| 51 | Error value compare wrong | `==` instead of `errors.Is` |
| 52 | Handling error twice | Log + return same err causing duplicate handling |
| 53 | Not handling error | `_ =` / ignored `err` |
| 54 | Not handling defer errors | `Close()`/`Rollback()` errors ignored |

## Concurrency foundations (#55–#61)

| # | Mistake | Look for / ask |
|---|---------|----------------|
| 55 | Concurrency vs parallelism | Structural confusion in design discussions/code comments |
| 56 | Concurrency always faster | Goroutine spam for tiny CPU work without benchmarks |
| 57 | Channels vs mutexes | Channels forced for simple shared-state sync (or reverse) |
| 58 | Data race vs race condition | Unsynchronized access; or sync'd but order-dependent bugs |
| 59 | Workload type impacts | Unbounded CPU workers; ignore `GOMAXPROCS` for CPU-bound |
| 60 | Misunderstanding contexts | Wrong use of values; ignore cancel/deadline |
| 61 | Inappropriate context propagation | Request ctx into async work after handler returns |

## Concurrency practice (#62–#74)

| # | Mistake | Look for / ask |
|---|---------|----------------|
| 62 | Goroutine with no stop plan | Leaked workers; no ctx/Done |
| 63 | Goroutines + loop variables | Classic loop capture (audit pre-1.22 and still suspicious patterns) |
| 64 | `select` determinism | Assuming fair/deterministic select choice |
| 65 | Notification channels | Need signal without data → `chan struct{}` |
| 66 | Nil channels | Not using nil chan to disable select cases |
| 67 | Channel size confusion | Magic buffer sizes; unbounded growth via huge buffers |
| 68 | String formatting side effects | `fmt` on types that take locks / mutate |
| 69 | Data races with `append` | Concurrent append same slice |
| 70 | Mutex + slices/maps | Copying maps/slices under inadequate locking |
| 71 | Misusing `WaitGroup` | `Add` inside goroutine; missing `Done`; reuse bugs |
| 72 | Forgetting `sync.Cond` | Complex wait/signal reinvented poorly (rare — only when Cond fits) |
| 73 | Not using `errgroup` | Manual WG+err mutex when errgroup fits |
| 74 | Copying a `sync` type | Mutex/WaitGroup by value; passed in structs by value |

## Standard library (#75–#81)

| # | Mistake | Look for / ask |
|---|---------|----------------|
| 75 | Wrong time duration | `time.Sleep(5)` meaning 5ns; bare integers |
| 76 | `time.After` leaks | `time.After` in loops without reset patterns |
| 77 | JSON mistakes | `Marshal` surprises; `omitempty`; case; embedded pointers |
| 78 | SQL mistakes | No context; bad pooling; expandable `IN` unsafely |
| 79 | Not closing resources | HTTP body, `sql.Rows`, files |
| 80 | No `return` after HTTP error write | Double WriteHeader / continued logic |
| 81 | Default HTTP client/server | No timeouts → connection leaks / Slowloris |

## Testing (#82–#90)

| # | Mistake | Look for / ask |
|---|---------|----------------|
| 82 | Not categorizing tests | Heavy tests always run; no short/tags |
| 83 | Not enabling race flag | Concurrent code without `-race` in CI/dev |
| 84 | Parallel/shuffle modes | Flaky hidden order deps; not using `-parallel`/`-shuffle` wisely |
| 85 | Not table-driven | Copy-paste cases |
| 86 | Sleeping in unit tests | `time.Sleep` for sync |
| 87 | Time API in tests | Hard-coded `time.Now` without seams |
| 88 | Not using httptest/iotest | Manual HTTP/IO test fakes |
| 89 | Inaccurate benchmarks | Missing `b.N` discipline; dead-code elimination pitfalls |
| 90 | Missing testing features | Subtests, helpers, cleanup unused |

## Optimizations (#91–#100)

Only raise when hot path, alloc-sensitive, or author claims performance.

| # | Mistake | Look for / ask |
|---|---------|----------------|
| 91 | CPU caches | False assumptions without profiles |
| 92 | False sharing | Contended adjacent atomics/hot fields |
| 93 | Instruction-level parallelism | Micro-opt claims without measurement |
| 94 | Data alignment | Unusual struct packing concerns |
| 95 | Stack vs heap | Escape analysis surprises in hot paths |
| 96 | Reducing allocations | Needless copies; missed `sync.Pool` where proven |
| 97 | Inlining | Over-split tiny funcs on hot paths (nit unless profiled) |
| 98 | Diagnostics tooling | Perf debate without pprof/trace |
| 99 | GC impacts | Alloc storms; huge pointer graphs |
| 100 | Go in Docker/K8s | GOMAXPROCS/container CPU limits mismatch |

---

## Priority when time-boxing

1. Errors (#48–#54), resources (#79), HTTP defaults (#81)
2. Concurrency (#58–#74), slice/map sharing (#25–#28, #69–#70)
3. Interfaces/organization (#5–#7, #12–#13)
4. Tests for concurrent/IO changes (#83–#86)
5. Optimizations (#91–#100) only with evidence

## Citation format

```
mistake_id: #62
issue: goroutine started in constructor with no cancellation path
recommendation: accept context (or expose Close) and exit on ctx.Done()
```
