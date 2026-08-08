# Context brain — interaction map

> Who depends on whom. Folder names match workspace-root siblings and `##` headings in `services.md`.

## Graph (summary)

```text
serviceA --HTTP--> serviceB
serviceA --event:order.created--> serviceC
infra-foo --deploys--> serviceA, serviceB
```

## Edges

| ID | From | To | Kind | Contract / address | Env / config keys | Confidence | Last verified |
|----|------|----|------|--------------------|-------------------|------------|---------------|
| E1 | serviceA | serviceB | HTTP | `GET /v1/…` | `SERVICE_B_URL` | high | YYYY-MM-DD |

Kind: `HTTP` | `gRPC` | `event` | `config` | `auth` | `infra` | `other`

## Pairs that must stay in sync

| Pair | Why | Drift symptom |
|------|-----|---------------|
| serviceA ↔ serviceB | _shared contract_ | _…_ |

## Out of scope / unknown

_Edges suspected but not evidenced yet._
