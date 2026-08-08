# Context brain — findings

> Bugs and drift that future plans/agents should see. Newest at top. Do not delete; set Status to resolved/mitigated.

---

### F-20260115-01 — example: order create vs billing client drift

| | |
|--|--|
| Type | drift |
| Status | open |
| Services | serviceA, serviceB |
| Edge | E1 |
| Severity | high |
| Date | 2026-01-15 |

**What:** `serviceA` made `priority` required on `POST /v1/orders`; `serviceB` billing client still omits the field.

**Impact:** `serviceB` requests fail validation or billing runs with wrong defaults.

**Evidence:** `serviceA/internal/api/order.go`; `serviceB/internal/client/orders.go`

**Follow-up:** Update `serviceB` client + tests; mark mitigated when merged.

---

<!-- Copy the block above for new findings. Prefer real IDs: F-YYYYMMDD-NN -->
