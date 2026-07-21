# Concurrency lens (Go)

Hunt races, leaks, ownership bugs, and context misuse. Prefer evidence (`go test -race`, clear shared state) over vibes.

Public anchors: [Go memory model](https://go.dev/ref/mem), [race detector](https://go.dev/doc/articles/race_detector), [context package](https://pkg.go.dev/context), *100 Go Mistakes* #55–#74.

## Triage order

1. Shared mutable state without sync
2. Goroutine lifetime / leaks
3. Context propagation
4. Channel / select design
5. `sync` API misuse
6. Tests (`-race`, no sleeps)

---

## Data races vs race conditions (#58)

| Concept | Meaning | Detector |
|---------|---------|----------|
| **Data race** | Concurrent access to same memory, ≥1 write, no happens-before | `go test -race` (near-zero false positives) |
| **Race condition** | Behavior depends on uncontrolled timing/order | Design review + stress tests; race detector may be silent |

Treat any `-race` hit as **high/critical**. Logical races (check-then-act on balances, authz) are still **high** even if memory is synchronized wrongly at a higher level.

### Patterns that race

```go
// BAD: concurrent map write
go func() { m[k] = v }()

// BAD: append on shared slice from multiple goroutines (#69)
go func() { s = append(s, x) }()

// BAD: request identity in package global (security + race)
var currentUser string
```

### Fixes

- Confine memory to one goroutine
- `sync.Mutex` / `RWMutex` around critical sections
- Channels to transfer ownership
- `sync/atomic` only for simple scalars/flags — not complex invariants

---

## Goroutine lifetime (#62)

Every `go f()` needs a stop plan: `context`, `errgroup`, `WaitGroup` + done signal, or owned shutdown.

**Look for:**

- Workers started in `init`/`New` without `Close`
- Request handlers spawning work that outlives the request without a detached ctx
- Missing `defer cancel()` after `WithCancel`/`WithTimeout`
- Loops that never select on `ctx.Done()`

```go
// GOOD sketch
ctx, cancel := context.WithCancel(parent)
defer cancel()
g, ctx := errgroup.WithContext(ctx)
g.Go(func() error { return worker(ctx) })
return g.Wait()
```

---

## Context (#60, #61)

Rules of thumb:

- First parameter: `ctx context.Context`
- Derive with timeout for outbound I/O; **always** `defer cancel()`
- Do **not** store contexts in structs long-term
- Values: request-scoped only (trace IDs); not required dependencies
- **Inappropriate propagation (#61):** HTTP request context cancels when the response is written — do not use `r.Context()` for async work that must continue after the handler returns; use `context.WithoutCancel` (Go 1.21+) or a supervised background context with its own timeout

```go
// BAD: publish may abort when handler finishes
go publish(r.Context(), msg)

// BETTER: independent timeout for async side-effect
bg, cancel := context.WithTimeout(context.WithoutCancel(r.Context()), 5*time.Second)
defer cancel()
go func() { _ = publish(bg, msg) }()
```

---

## Channels (#64–#67)

| Topic | Review cue |
|-------|------------|
| Unbuffered | Sync rendezvous; can deadlock if both sides wrong |
| Buffered | Capacity is a design choice — document why; huge buffers hide backpressure |
| Close | Sender closes; never close if multiple senders without coordinator |
| Nil channel | Disable a `select` case intentionally |
| Notification | `chan struct{}` for signal-only (#65) |
| Select | Not fair/deterministic (#64); always consider cancel case |

```go
select {
case job := <-jobs:
    handle(job)
case <-ctx.Done():
    return ctx.Err()
}
```

---

## Mutexes and sync (#57, #70–#74)

- Parallel goroutines sharing state → mutexes; pipelines/ownership handoff → channels (#57)
- Never copy `sync.Mutex` / `WaitGroup` (pass pointers; don't embed in value-copied structs) (#74)
- `WaitGroup.Add` **before** `go`, never inside the goroutine (#71)
- Prefer `golang.org/x/sync/errgroup` when N tasks share cancel-on-first-error (#73)
- Don't hold locks across slow I/O
- Lock ordering: document if multiple mutexes

```go
// BAD
go func() {
    wg.Add(1) // race with Wait
    defer wg.Done()
}()

// GOOD
wg.Add(1)
go func() {
    defer wg.Done()
}()
```

---

## Workload sizing (#56, #59)

- CPU-bound: worker count near `runtime.GOMAXPROCS(0)`
- I/O-bound: bound by external limits + semaphores/`errgroup` + context
- "More goroutines" is not automatically faster (#56) — ask for benchmarks on hot paths

---

## HTTP / stdlib concurrency interactions

- Default `http.Client` / `Server` without timeouts (#81) interact badly under load
- Always drain/close response bodies (#79)
- After `http.Error` / write failure paths, `return` (#80)

---

## Testing concurrent code (#83, #86)

- Require `-race` for packages that start goroutines
- Ban `time.Sleep` as synchronization (#86); use channels, barriers, or `goleak`
- Consider [goleak](https://github.com/uber-go/goleak) for leak assertions in tests

---

## Finding format

State: **shared resource** → **concurrent accessors** → **failure mode** (race | leak | deadlock | lost update | cancel bug) → **fix**. Map to `#N` when possible.
