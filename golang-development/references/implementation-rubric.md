# Implementation rubric

Every gap from a self-check must be **actionable and evidenced**. Thin notes get rejected — fix Must/Should items before claiming done.

## Required fields

| Field | Requirement |
|-------|-------------|
| `severity` | critical \| high \| medium \| low \| nit |
| `location` | `path:line` or `path` + symbol; `diff-hunk` if line unknown |
| `issue` | One sentence: what is wrong **in this code** |
| `recommendation` | Concrete change (not "consider improving") |
| `example` | Short Go before/after or corrected snippet (tests: sketch with `t.Run` / table row OK) |
| `id` | Optional: `#N` (100 Go Mistakes), Cheney post title, CWE-xx, or rule name |

## Quality bar

**Accept:**

```text
severity: high
location: internal/api/order.go:84
issue: handler writes http.Error then continues and writes 200 (#80)
recommendation: return immediately after http.Error
mistake_id: #80
example:
  // before
  if err != nil {
    http.Error(w, err.Error(), 500)
  }
  writeOK(w)
  // after
  if err != nil {
    http.Error(w, err.Error(), 500)
    return
  }
  writeOK(w)
```

**Reject / rewrite:**

- "This could be cleaner" with no location
- "Use best practices" with no fix
- Entire lecture with no link to the code
- Gap outside the agent's lens

## Speculative gaps

Allowed if labeled:

```text
severity: low
issue: (speculative) map may be accessed concurrently if handler is re-entered — no mutex visible
```

Do not mark speculative items critical. Prefer confirming with `-race` or by reading call sites.

## Empty lens (healthy change)

If no gaps:

```text
No gaps.

Checked:
- ...
- ...
```

At least 5 concrete checks tied to the change (files/symbols), not generic slogans.

## Severity calibration

| Question | If yes → at least |
|----------|-------------------|
| Can this corrupt data or leak another tenant? | high/critical |
| Will `-race` or production load likely trip it? | high |
| Behavior change with no/weak test for the new path? | medium (tests lens) — write the test |
| Is it a boundary leak without current exploit? | medium |
| Is it style/docs only? | nit |
| Are you guessing? | low + speculative |

## Ship buckets (parent / merge)

| Severity | Action |
|----------|--------|
| critical, high | Must fix before done |
| medium | Should fix (default: fix in the same change) |
| low, nit | Optional; max 5 nits chased |

## Definition of done (implementation)

- [ ] Engaged lenses self-checked
- [ ] All Must + Should gaps fixed in code
- [ ] Lint / `go vet` / `go test -race` / `govulncheck` run on changed packages (or noted skip reason)
- [ ] Behavior change has a failing-if-reverted test
- [ ] Docs match the code: doc comments on changed exported API, plus README, contract, and config docs when those changed (or "no docs impact" stated)
