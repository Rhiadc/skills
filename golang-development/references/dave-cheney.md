# Dave Cheney — Go practice cue sheet

Secondary authority after [go.dev](https://go.dev/doc/) / Effective Go / Code Review Comments. Prefer primary docs for language semantics; use Cheney for **idiomatic design while implementing**.

Hub: [dave.cheney.net](https://dave.cheney.net/) · [Practical Go](https://dave.cheney.net/practical-go) · [Practical Go (GopherCon SG)](https://dave.cheney.net/practical-go/presentations/gophercon-singapore-2019.html) · [Zen of Go](https://dave.cheney.net/2020/02/23/the-zen-of-go)

Do not paste long copyrighted excerpts into code or handoffs — cite the post and apply the rule in your own words.

---

## Quality / API design

| Cue | Prefer when writing | Source |
|-----|---------------------|--------|
| Clarity over cleverness | Clear names, early returns, shallow nesting | Practical Go, Zen of Go |
| Names describe what the package **provides** | Avoid `utils`, `common`, `base`, `helpers` | [Avoid package names like base, util, or common](https://dave.cheney.net/2019/01/08/avoid-package-names-like-base-util-or-common) |
| Functional options for growing constructors | Prefer options over brittle multi-bool constructors | [Functional options](https://dave.cheney.net/2014/10/17/functional-options-for-friendly-apis) |
| Don’t force allocations on callers | Let callers reuse buffers when APIs grow hot | Practical Go → API design |
| Same-type parameter lists | Avoid `foo(a, b, c int)` swaps — named types / options | Practical Go |
| Receiver on `T` vs `*T` | Consistent mutability; avoid huge structs by value | Practical Go fundamentals |
| Errors are values | Return errors for expected failure; panic only for truly unrecoverable | Practical Go / Zen of Go |

Align with *100 Go Mistakes* `#5`–`#7`, `#11`–`#13`, `#48`–`#54` when both apply — cite both in decisions/comments sparingly.

---

## Concurrency

| Cue | Prefer when writing | Source |
|-----|---------------------|--------|
| Never start a goroutine without knowing how it stops | `go f()` with cancel/close/Wait plan | [Never start a goroutine…](https://dave.cheney.net/2016/12/22/never-start-a-goroutine-without-knowing-how-it-will-stop), Zen of Go |
| Leave `go` to the caller in libraries | Do not spawn unmanaged workers in `New` | Zen of Go |
| Channel axioms / ownership | Clear closer; one sender role or a coordinator | Practical Go concurrency section |

Map to mistakes `#62`, `#71`, `#73` and the concurrency lens.

---

## Testing

Owned primarily by the **tests** lens — see [testing.md](testing.md).

| Cue | Source |
|-----|--------|
| Prefer table-driven tests + `t.Run` | [Prefer table driven tests](https://dave.cheney.net/2019/05/07/prefer-table-driven-tests) |
| Coverage ≠ sufficient cases | same |
| `TestMain` must still run tests (`m.Run`) | [TestMain microblog](https://dave.cheney.net/2024/02/22/microblog-testmain-can-cause-one-to-question-reality) |
| Benchmarks need discipline | Practical Go → Testing |

---

## When citing in gaps / decisions

```text
severity: medium
location: internal/billing/doc.go (package name)
issue: package "utils" aggregates unrelated helpers (Cheney: name packages by what they provide)
recommendation: move helpers next to callers or split into focused packages (e.g. money, retry)
```
