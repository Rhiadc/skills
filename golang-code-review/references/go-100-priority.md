# 100 Go Mistakes - priority slice (lite reviews)

Use this in **lite** mode instead of loading the full [go-100-mistakes.md](go-100-mistakes.md) catalog. Open the full catalog in **full** mode, or when a priority item points at a deeper section.

Voice: hunt cues. Report findings with evidence from the diff (severity, location, recommendation, example).

## Priority when time-boxing

1. Errors (#48-#54), resources (#79), HTTP defaults (#81)
2. Concurrency (#58-#74), slice/map sharing (#25-#28, #69-#70) - only if the diff touches them
3. Interfaces/organization (#5-#7, #12-#13) - only if boundaries/packages move
4. Tests for concurrent/IO changes (#83-#86) - `tests` lens
5. Optimizations (#91-#100) - only when the author claims performance

## Must-scan rows

| # | Mistake | Look for in the diff |
|---|---------|----------------------|
| 1 | Unintended variable shadowing | `:=` in nested blocks hiding outer `err` |
| 2 | Unnecessary nested code | Deep nesting where early return fits |
| 48 | Panicking | Panic on expected failure paths |
| 49 | When to wrap | Lost context, or wrap without `%w` |
| 50 | Error type compare wrong | Type assert instead of `errors.As` |
| 51 | Error value compare wrong | `==` instead of `errors.Is` |
| 52 | Handling error twice | Log + return the same error |
| 53 | Not handling error | `_ =` or ignored `err` |
| 54 | Not handling defer errors | Ignored `Close()` / `Rollback()` |
| 79 | Not closing resources | HTTP bodies, `sql.Rows`, files |
| 80 | No `return` after HTTP error write | Continued logic after `http.Error` |
| 81 | Default HTTP client/server | Missing timeouts on new servers/clients |

## If the diff touches concurrency

Skim #58-#62, #69, #71, #74 in the full catalog, or open [concurrency.md](concurrency.md) when the concurrency lens runs.

## Citation format

```
mistake_id: #80
issue: handler writes http.Error then continues
recommendation: return immediately after http.Error
```
