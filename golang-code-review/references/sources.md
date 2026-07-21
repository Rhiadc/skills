# Sources

Use these as authority when resolving disagreements. Prefer primary docs over blogs.

## Go — official

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Go Memory Model](https://go.dev/ref/mem)
- [Data Race Detector](https://go.dev/doc/articles/race_detector)
- [Security Best Practices for Go Developers](https://go.dev/doc/security/best-practices)
- [govulncheck](https://go.dev/security/vulncheck/)
- [context package](https://pkg.go.dev/context)
- [Go 1.22 loop semantics](https://go.dev/blog/loopvar-preview) (loop var capture history)

## 100 Go Mistakes

- Book: Teiva Harsanyi — *100 Go Mistakes and How to Avoid Them* (Manning)
- Public summary index: [https://100go.co/](https://100go.co/)
- GitHub docs mirror: [teivah/100-go-mistakes](https://github.com/teivah/100-go-mistakes)

Mistake titles `#1`–`#100` in this skill align with that public index. Prefer the book for full rationale; do not paste copyrighted book prose into reviews.

## Architecture / DDD (pragmatic)

- Consumer-side interfaces, hexagonal ports/adapters — common Go community practice (accept interfaces, return structs)
- DDD tactical patterns applied lightly: entities, value objects, aggregates, repositories as ports

## Security extras (secondary)

- OWASP classes mapped to Go sinks (SQL, XSS, SSRF, path traversal)
- Go HTTP defaults (timeouts, body limits) as first-class review items
