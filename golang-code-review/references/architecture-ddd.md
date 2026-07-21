# Architecture & DDD lens (Go)

Evaluate structure and domain clarity for the **reviewed change**. Prefer smallest fix that restores boundaries. Do not demand full DDD ceremony on tiny CLIs or pure adapters.

Related mistakes: #5–#7, #12–#15 (*100 Go Mistakes*).

---

## Dependency direction (hexagonal / clean)

Ideal flow:

```text
cmd/ (composition root)
  → adapters (HTTP, gRPC, SQL, brokers)
    → application (use cases / orchestration)
      → domain (entities, VOs, domain services, ports)
```

**Hard rules to check:**

- [ ] Domain does **not** import `net/http`, `database/sql`, drivers, or framework kits
- [ ] Adapters depend inward; domain does not depend on adapters
- [ ] Composition/wiring lives at the edge (`main` / `cmd`), not in domain
- [ ] `internal/` used to prevent accidental cross-module imports when appropriate

```go
// BAD: domain knows SQL
func (o *Order) Save(db *sql.DB) error { ... }

// GOOD: port in domain/application, impl in adapter
type OrderRepository interface {
    Save(ctx context.Context, o Order) error
}
```

---

## Go interface idiom (#5–#7)

| Practice | Review cue |
|----------|------------|
| Define interfaces at **consumer** | Small interface next to use case that needs it |
| Avoid producer-side interfaces | Huge `Repository` iface beside Postgres impl with one consumer |
| Accept interfaces, return structs | Handlers/services take deps as interfaces; constructors return concrete types |
| No premature abstraction | First impl → concrete; extract iface when second impl or test double needs it |
| `any` says nothing (#8) | Replace with real types/constraints |

---

## DDD mapping in Go

| DDD concept | Go shape | Review checks |
|-------------|----------|---------------|
| Entity | Struct with ID; pointer receivers for mutation | Identity equality; invariants on methods |
| Value object | Immutable; compared by value | No accidental identity; validation on creation |
| Aggregate | Root controls invariants | Mutations only via root; clear consistency boundary |
| Domain service | Func/struct in domain when logic spans entities | Not a dumping ground for all app logic |
| Repository | Interface (port); adapter implements | No `*sql.Rows` / ORM types leaking upward |
| Application service | Orchestrates transactions, ports | Thin vs fat handlers |
| Domain event | Fact struct | Cross-context via events/ACL, not reaching into another context's internals |
| Bounded context | Package/module boundary | No shared mutable models across contexts |
| Anti-corruption layer | Translator at boundary | External DTOs not used as domain |

**Anemic domain smell:** exported structs with only fields + all rules in `*Service`. Prefer behavior on types when invariants are real.

**When NOT to push DDD:** trivial CRUD, generated clients, one-off scripts — note as out-of-scope rather than over-engineering.

---

## Package organization (#12–#14)

Prefer:

- Packages named by **domain capability** (`billing`, `shipment`) over catch-all `models`/`utils` (#13) — Cheney: [Avoid package names like base, util, or common](https://dave.cheney.net/2019/01/08/avoid-package-names-like-base-util-or-common)
- Clear ownership; avoid circular imports (symptom of blurred boundaries)
- Exported surface minimal; doc comments on exports (#15)

Layout patterns (any is fine if consistent):

```text
# Vertical (modular monolith / by context)
internal/ordering/
  domain/
  application/
  adapter/http/
  adapter/postgres/

# Hex ports/adapters
internal/domain/
internal/app/
internal/adapters/...
cmd/api/
```

Flag **churn** when a change spreads across many unrelated packages without a facade — possible missing aggregate/ACL.

---

## Application vs domain vs adapter

| Layer | Should | Should not |
|-------|--------|------------|
| Handler/adapter | Parse/validate input shapes, map DTOs, map errors to HTTP codes | Business invariants, SQL, multi-step policies inline |
| Application | Transaction boundary, call ports, orchestrate | Low-level SQL, HTML rendering |
| Domain | Invariants, language of the business | Framework types, env vars, global config reads |

---

## Error and API boundaries

- Domain errors are meaningful types/sentinels; adapters map to protocol codes once
- Don't leak SQL/`pq` errors straight to clients
- Context passed from adapter → app → ports for cancel/timeout

---

## Finding format

State: **boundary violated** (what depended on what) → **why it hurts** (testing, change cost, invariant risk) → **minimal structural fix**. Cite `#5`/`#6`/`#7`/`#12` when relevant.

Severity: broken domain invariant on write path → **critical/high**; dependency direction leak without immediate bug → **medium**; naming-only → **low/nit**.
