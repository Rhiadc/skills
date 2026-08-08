# 100 Go Mistakes - priority slice (light mode)

Use this in **light** mode instead of loading the full [go-100-mistakes.md](go-100-mistakes.md) catalog. Open the full catalog in **full** mode, or when a priority item points at a deeper section.

Voice: build rules. Fix issues in code before claiming done.

## Priority when time-boxing

1. Errors (#48-#54), resources (#79), HTTP defaults (#81)
2. Concurrency (#58-#74), slice/map sharing (#25-#28, #69-#70) - only if the change touches them
3. Interfaces/organization (#5-#7, #12-#13) - only if boundaries/packages move
4. Tests for concurrent/IO changes (#83-#86)
5. Optimizations (#91-#100) - skip in light mode unless measured

## Must-scan rows

| # | Mistake | Avoid / Prefer |
|---|---------|----------------|
| 1 | Unintended variable shadowing | Prefer `=` over `:=` when updating outer `err` |
| 2 | Unnecessary nested code | Early return; happy path left-aligned |
| 48 | Panicking | Return errors for expected failures |
| 49 | When to wrap | `%w` when `Is`/`As` needed; add context |
| 50 | Error type compare wrong | `errors.As` |
| 51 | Error value compare wrong | `errors.Is` |
| 52 | Handling error twice | Log **or** return, not both without intent |
| 53 | Not handling error | Never ignore a meaningful `err` |
| 54 | Not handling defer errors | Check `Close()` / `Rollback()` |
| 79 | Not closing resources | HTTP bodies, `sql.Rows`, files |
| 80 | No `return` after HTTP error write | Always return after `http.Error` / failed write |
| 81 | Default HTTP client/server | Always set timeouts |

## If the change touches concurrency

Skim #58-#62, #69, #71, #74 in the full catalog, or open [concurrency.md](concurrency.md) when the concurrency gate fires.

## Citation format

```
mistake_id: #53
issue: ignored error from Close
recommendation: check and return/wrap the error
```
