# Context brain — services

> One **`##` section per first-level folder** at the workspace root. Heading must match the directory name. Keep sections short; use paths into that folder, do not paste large code.

---

## serviceA

| Field | Value |
|-------|-------|
| Kind | service |
| Path | `./serviceA/` |
| Stack | Go |
| Module | _go.mod path_ |
| Last reviewed | YYYY-MM-DD |
| Confidence | high \| medium \| low |

### Purpose

_One short paragraph._

### Owns (contracts)

- HTTP/gRPC it **exposes**
- Events it **publishes**
- Config keys others rely on

### Depends on (outbound)

| Neighbor | Kind | How | Config key |
|----------|------|-----|------------|
| | | | |

### Key entrypoints

| Path | Role |
|------|------|
| `serviceA/cmd/…` | |

### Gotchas

-_link findings IDs when known_

---

## serviceB

| Field | Value |
|-------|-------|
| Kind | service |
| Path | `./serviceB/` |
| Stack | Go |
| Module | |
| Last reviewed | YYYY-MM-DD |
| Confidence | medium |

### Purpose

_

### Owns (contracts)

-

### Depends on (outbound)

| Neighbor | Kind | How | Config key |
|----------|------|-----|------------|
| | | | |

### Key entrypoints

| Path | Role |
|------|------|
| | |

### Gotchas

-

---

## infra-foo

| Field | Value |
|-------|-------|
| Kind | infra |
| Path | `./infra-foo/` |
| Stack | _terraform / helm / …_ |
| Last reviewed | YYYY-MM-DD |
| Confidence | medium |

### Purpose

_What this infra folder wires or deploys._

### Couples

| Service | How |
|---------|-----|
| | |

### Gotchas

-

<!-- Duplicate the section pattern for every first-level folder. Remove the examples when seeding a real workspace. -->
