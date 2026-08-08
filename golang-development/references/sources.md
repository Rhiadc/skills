# Sources

Use these as authority when choosing designs or resolving disagreements. Prefer primary docs over blogs; Cheney is the preferred secondary for idiomatic Go design.

## Go — official

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Go Memory Model](https://go.dev/ref/mem)
- [Data Race Detector](https://go.dev/doc/articles/race_detector)
- [Security Best Practices for Go Developers](https://go.dev/doc/security/best-practices)
- [govulncheck](https://go.dev/security/vulncheck/)
- [context package](https://pkg.go.dev/context)
- [testing package](https://pkg.go.dev/testing)
- [Fuzzing tutorial](https://go.dev/doc/tutorial/fuzz)
- [Go 1.22 loop semantics](https://go.dev/blog/loopvar-preview) (loop var capture history)

## Dave Cheney

- Hub: [dave.cheney.net](https://dave.cheney.net/)
- [Practical Go](https://dave.cheney.net/practical-go) (index)
- [Practical Go — GopherCon Singapore](https://dave.cheney.net/practical-go/presentations/gophercon-singapore-2019.html)
- [The Zen of Go](https://dave.cheney.net/2020/02/23/the-zen-of-go)
- [Prefer table driven tests](https://dave.cheney.net/2019/05/07/prefer-table-driven-tests)
- [Never start a goroutine without knowing how it will stop](https://dave.cheney.net/2016/12/22/never-start-a-goroutine-without-knowing-how-it-will-stop)
- [Avoid package names like base, util, or common](https://dave.cheney.net/2019/01/08/avoid-package-names-like-base-util-or-common)
- [Functional options for friendly APIs](https://dave.cheney.net/2014/10/17/functional-options-for-friendly-apis)
- Cue sheet in this skill: [dave-cheney.md](dave-cheney.md)

## 100 Go Mistakes

- Book: Teiva Harsanyi — *100 Go Mistakes and How to Avoid Them* (Manning)
- Public summary index: [https://100go.co/](https://100go.co/)
- GitHub docs mirror: [teivah/100-go-mistakes](https://github.com/teivah/100-go-mistakes)

Mistake titles `#1`–`#100` in this skill align with that public index. Prefer the book for full rationale; do not paste copyrighted book prose into code comments or handoffs.

## Architecture / DDD (pragmatic)

- Consumer-side interfaces, hexagonal ports/adapters — common Go community practice (accept interfaces, return structs)
- DDD tactical patterns applied lightly: entities, value objects, aggregates, repositories as ports

## Security extras (secondary)

- OWASP classes mapped to Go sinks (SQL, XSS, SSRF, path traversal)
- Go HTTP defaults (timeouts, body limits) as first-class implementation items

## Conflict order

1. Official Go docs / spec / race detector output
2. Effective Go + Code Review Comments
3. Dave Cheney (design/testing rhetoric)
4. 100 Go Mistakes public index (`#N`)
5. Team/repo conventions (if present, they win for style)
