# Finding rubric

Every specialist finding must be **actionable and evidenced**. Thin findings get rejected by the parent/final evaluator.

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
- Entire lecture with no link to the diff
- Finding outside the agent's lens

## Speculative findings

Allowed if labeled:

```text
severity: low
issue: (speculative) map may be accessed concurrently if handler is re-entered — no mutex visible
```

Do not mark speculative items critical.

## Empty lens

If no issues:

```text
No issues.

Checked:
- ...
- ...
```

At least 5 concrete checks tied to the diff (files/symbols), not generic slogans.

## Severity calibration

| Question | If yes → at least |
|----------|-------------------|
| Can this corrupt data or leak another tenant? | high/critical |
| Will `-race` or production load likely trip it? | high |
| Behavior change with no/weak test for the new path? | medium (tests lens) |
| Is it a boundary leak without current exploit? | medium |
| Is it style/docs only? | nit |
| Are you guessing? | low + speculative |

## Paste buckets (for evaluator / parent)

| Severity | Paste section |
|----------|----------------|
| critical, high | Must address |
| medium | Should address |
| low, nit | Nits (optional; max 5) |
