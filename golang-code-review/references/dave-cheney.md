# Dave Cheney — Go practice cue sheet

Secondary authority after [go.dev](https://go.dev/doc/) / Effective Go / Code Review Comments. Prefer primary docs for language semantics; use Cheney for **idiomatic design and review rhetoric**.

Hub: [dave.cheney.net](https://dave.cheney.net/) · [Practical Go](https://dave.cheney.net/practical-go) · [Practical Go (GopherCon SG)](https://dave.cheney.net/practical-go/presentations/gophercon-singapore-2019.html) · [Zen of Go](https://dave.cheney.net/2020/02/23/the-zen-of-go)

Do not paste long copyrighted excerpts into reviews — cite the post and state the rule in your own words.

---

## Quality / API design

| Cue | Look for | Source |
|-----|----------|--------|
| Clarity over cleverness | Cryptic names, nested control flow | Practical Go, Zen of Go |
| Names describe what the package **provides** | `utils`, `common`, `base`, `helpers` | [Avoid package names like base, util, or common](https://dave.cheney.net/2019/01/08/avoid-package-names-like-base-util-or-common) |
| Functional options for growing constructors | Brittle multi-bool constructors; nil config required | [Functional options](https://dave.cheney.net/2014/10/17/functional-options-for-friendly-apis) |
| Don’t force allocations on callers | APIs that allocate when caller could reuse buffers | Practical Go → API design |
| Same-type parameter lists | `foo(a, b, c int)` easy to swap — named types / options | Practical Go |
| Receiver on `T` vs `*T` | Inconsistent mutability; huge structs by value | Practical Go fundamentals |
| Errors are values | Panic for routine failure; unclear error context | Practical Go / Zen of Go |

Align with *100 Go Mistakes* `#5`–`#7`, `#11`–`#13`, `#48`–`#54` when both apply — cite both.

---

## Concurrency

| Cue | Look for | Source |
|-----|----------|--------|
| Never start a goroutine without knowing how it stops | `go f()` with no cancel/close/Wait plan | [Never start a goroutine…](https://dave.cheney.net/2016/12/22/never-start-a-goroutine-without-knowing-how-it-will-stop), Zen of Go |
| Leave `go` to the caller in libraries | Libraries spawning unmanaged workers in `New` | Zen of Go |
| Channel axioms / ownership | Unclear closer; multiple senders without coordinator | Practical Go concurrency section |

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

## When citing in findings

```text
severity: medium
location: internal/billing/doc.go (package name)
issue: package "utils" aggregates unrelated helpers (Cheney: name packages by what they provide)
recommendation: move helpers next to callers or split into focused packages (e.g. money, retry)
```
