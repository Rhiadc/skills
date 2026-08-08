# Drift detection

**Drift** = one side of a paired contract moved; the other side (or the brain’s expected pair) did not.

## When to check

- Changing request/response JSON, proto, event payload, status codes, auth requirements
- Renaming/removing routes, topics, env keys consumers use
- Plan that touches a service listed in map “Pairs that must stay in sync”
- Bug that smells like version skew between services

## How

1. Identify the edge in `map.md` (or add it if missing).
2. List consumers (`From` services) and provider (`To` or publisher/consumer roles).
3. Ask: did this job update **all** sides that must stay paired? If the brain says B consumes A’s `/v1/x` and only A changed the shape → drift.
4. **Warn** in chat with edge id, services, and mismatch.
5. **Append** a `type: drift` finding in `findings.md`.
6. Continue only with user ack or with the paired fix in scope.

## Finding snippet

```markdown
### F-YYYYMMDD-01 — drift: serviceA /v1/order vs serviceB client

| | |
|--|--|
| Type | drift |
| Status | open |
| Services | serviceA, serviceB |
| Edge | E1 |
| Severity | high |
| Date | YYYY-MM-DD |

**What:** serviceA added required field `priority`; serviceB client/omitted handling unchanged.

**Impact:** serviceB may fail decode or send invalid requests.

**Evidence:** serviceA/api/... ; serviceB/internal/client/...

**Follow-up:** update serviceB client + tests; then mark mitigated/resolved.
```

## Not drift

- Purely internal refactors with stable public contract
- Infra-only comment changes
- Low-confidence edges — verify first, then warn if confirmed
