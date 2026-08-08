# Context brain — index

> Lives at the **workspace root** only (`./context-brain/`), beside service folders — never inside a microservice. Agents: start here, then `map.md`, then only the needed `##` sections in `services.md`.

## Workspace

| Field | Value |
|-------|-------|
| Root | _workspace root path_ |
| Folder count (N) | _catalog size; not fixed_ |
| Last full refresh | _YYYY-MM-DD_ |
| Notes | _Go microservices + infra, etc._ |

## Catalog (first-level folders)

One row per sibling folder of `context-brain/`. Link jumps to that folder’s section in `services.md`.

| Folder | Kind | Role (one line) | Section |
|--------|------|-----------------|---------|
| serviceA | service | _…_ | [services.md § serviceA](services.md#servicea) |
| serviceB | service | _…_ | [services.md § serviceB](services.md#serviceb) |
| infra-foo | infra | _…_ | [services.md § infra-foo](services.md#infra-foo) |

Kind: `service` | `infra` | `shared` | `ignore`

## How to navigate

1. This index  
2. [map.md](map.md) for plans / cross-service work  
3. In-scope sections in [services.md](services.md)  
4. [findings.md](findings.md) for bugs & drift  

## Hotspots

_Short list of edges/services that break often (link finding IDs)._
