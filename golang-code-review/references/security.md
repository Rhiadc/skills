# Security lens (Go)

Focus on exploitability and blast radius in the reviewed change. Cross-check official guidance: [Go security best practices](https://go.dev/doc/security/best-practices).

## Tooling (mention in findings if missing on risky changes)

| Tool | Why |
|------|-----|
| `govulncheck ./...` | Module CVEs that actually reach the code |
| `go test -race` | Data races that become authz/data leaks under load |
| `go vet ./...` | Suspicious constructs |
| Fuzz tests | Parsers, decoders, validators — edge exploits |

---

## Authn / authz

- [ ] Missing auth on new handlers / RPC methods
- [ ] IDOR: trusting client IDs without ownership checks
- [ ] **Request-scoped identity in package globals** — classic concurrent auth bypass
- [ ] JWT/session: alg confusion, missing exp/aud/iss checks, accept `none`
- [ ] TOCTOU: check-then-act without transaction/lock

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
| SQL injection | String concat / `fmt.Sprintf` into query; use drivers + placeholders |
| Command injection | `exec.Command` with user-controlled args via shell |
| Path traversal | `filepath.Join(base, user)` without confinement; prefer `os.Root` (Go 1.24+) or careful `Clean` + prefix check |
| SSRF | User-controlled URLs to `http.Get` without allowlist |
| XSS | `text/template` for HTML; `template.HTML(userInput)` disabling escape |
| Log injection | Unsanitized user input in log lines consumed by systems |

---

## HTTP server / client defaults (#81 and friends)

Default `http.Server` timeouts are zero (unbounded) — Slowloris / resource exhaustion.

```go
srv := &http.Server{
    Addr:              ":8080",
    ReadHeaderTimeout: 5 * time.Second,
    ReadTimeout:       15 * time.Second,
    WriteTimeout:      15 * time.Second,
    IdleTimeout:       60 * time.Second,
}
```

Also check:

- [ ] `http.MaxBytesReader` / body size limits
- [ ] Client: custom `http.Client{Timeout: ...}` or Transport deadlines — never bare `http.Get` in production paths
- [ ] TLS: `InsecureSkipVerify` only with documented temporary reason
- [ ] CORS `*` + credentials
- [ ] Open redirects from user-supplied URLs
- [ ] Security headers where the app serves browsers (CSP, nosniff, HSTS as appropriate)

---

## Secrets & crypto

- [ ] Hardcoded tokens/keys; secrets in tests committed
- [ ] Secrets in logs/errors
- [ ] `math/rand` for security tokens → `crypto/rand`
- [ ] Password storage: suitable KDF (bcrypt/argon2/scrypt), not plaintext/SHA-only
- [ ] Homegrown crypto; deprecated ciphers; weak TLS config

---

## Data / privacy

- [ ] PII in logs
- [ ] Cross-tenant cache keys missing tenant id
- [ ] Verbose errors returned to clients (`err.Error()` with internals)

---

## Dependencies / supply chain

- [ ] New deps: necessity, license, maintenance; run `govulncheck`
- [ ] `replace` to odd paths
- [ ] Deserializing untrusted `gob` / gadget-rich JSON into powerful types

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

## Finding format

Prefer: **attacker action** → **affected code** → **impact** → **fix**. Link CWE when obvious (e.g. CWE-89 SQL, CWE-362 race, CWE-400 exhaustion).
