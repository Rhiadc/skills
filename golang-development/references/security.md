# Security lens (Go) — development

**When to open (gate):** configuration that can weaken the system, or **exploitable** implementation (public HTTP, authn/authz, SQL/command/path/SSRF sinks, secrets/crypto). Skip for pure internal refactors with no config/exploit surface.

Build for exploitability resistance and limited blast radius. Cross-check official guidance: [Go security best practices](https://go.dev/doc/security/best-practices).

## Tooling (run before done on risky changes)

| Tool | Why |
|------|-----|
| `govulncheck ./...` | Module CVEs that actually reach the code |
| `go test -race` | Data races that become authz/data leaks under load |
| `go vet ./...` | Suspicious constructs |
| Fuzz tests | Parsers, decoders, validators — edge exploits |

---

## Authn / authz

- [ ] Auth on new handlers / RPC methods
- [ ] IDOR: never trust client IDs without ownership checks
- [ ] **Never store request-scoped identity in package globals** — classic concurrent auth bypass
- [ ] JWT/session: no alg confusion; check exp/aud/iss; reject `none`
- [ ] TOCTOU: check-then-act under transaction/lock when needed

```go
// BAD under concurrency
var currentUser User
func handler(w http.ResponseWriter, r *http.Request) {
    currentUser = userFrom(r) // leaked across requests
}

// GOOD
func handler(w http.ResponseWriter, r *http.Request) {
    user := userFrom(r)
    ctx := context.WithValue(r.Context(), userKey{}, user)
    // pass ctx / user explicitly
}
```

---

## Injection & input

| Risk | Go-specific cue |
|------|-----------------|
| SQL injection | Never string-concat / `fmt.Sprintf` into query; use drivers + placeholders |
| Command injection | Avoid shell; `exec.Command` with fixed binary + discrete args |
| Path traversal | Do not `filepath.Join(base, user)` without confinement; prefer `os.Root` (Go 1.24+) or careful `Clean` + prefix check |
| SSRF | User-controlled URLs → allowlist before `http.Get` |
| XSS | Use `html/template` for HTML; never `template.HTML(userInput)` without trust |
| Log injection | Sanitize or structure user input in log lines |

---

## HTTP server / client defaults (#81 and friends)

Default `http.Server` timeouts are zero (unbounded) — Slowloris / resource exhaustion. Set timeouts when you create servers.

```go
srv := &http.Server{
    Addr:              ":8080",
    ReadHeaderTimeout: 5 * time.Second,
    ReadTimeout:       15 * time.Second,
    WriteTimeout:      15 * time.Second,
    IdleTimeout:       60 * time.Second,
}
```

Also implement:

- [ ] `http.MaxBytesReader` / body size limits
- [ ] Client: custom `http.Client{Timeout: ...}` or Transport deadlines — never bare `http.Get` in production paths
- [ ] TLS: `InsecureSkipVerify` only with documented temporary reason
- [ ] Avoid CORS `*` + credentials
- [ ] No open redirects from user-supplied URLs
- [ ] Security headers where the app serves browsers (CSP, nosniff, HSTS as appropriate)

---

## Secrets & crypto

- [ ] No hardcoded tokens/keys; no secrets in committed tests
- [ ] No secrets in logs/errors
- [ ] Security tokens from `crypto/rand`, not `math/rand`
- [ ] Password storage: suitable KDF (bcrypt/argon2/scrypt), not plaintext/SHA-only
- [ ] No homegrown crypto; no deprecated ciphers; strong TLS config

---

## Data / privacy

- [ ] No PII in logs unless required and redacted
- [ ] Cross-tenant cache keys include tenant id
- [ ] Clients get safe errors — not raw `err.Error()` with internals

---

## Dependencies / supply chain

- [ ] New deps: necessity, license, maintenance; run `govulncheck`
- [ ] Avoid odd `replace` paths unless justified
- [ ] Do not deserialize untrusted `gob` / gadget-rich JSON into powerful types

---

## Concurrency × security

| Pitfall | Why it matters |
|---------|----------------|
| Shared maps for sessions without sync | Corrupt or cross-user reads |
| Goroutine leak on auth path | DoS (CWE-400 class) |
| Cancel bugs leaving privileged work running | Unexpected continued access |

---

## Severity hints

| Finding | Typical severity |
|---------|------------------|
| Confirmed injection / auth bypass | critical |
| Missing timeouts on public server | high |
| `InsecureSkipVerify` in prod config | high |
| Missing body limit | medium/high |
| Missing security headers only | low/medium (context) |
| Speculative without sink | low + speculative |

## When documenting a security gap

Prefer: **attacker action** → **affected code** → **impact** → **fix**. Link CWE when obvious (e.g. CWE-89 SQL, CWE-362 race, CWE-400 exhaustion).
