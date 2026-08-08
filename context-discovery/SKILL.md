---
name: context-discovery
description: >-
  Use whenever the workspace is a multi-service root (any number of first-level
  Go microservice and/or infra folders) and the agent needs service interaction
  context, cross-service planning, neighbor-aware development, multi-service
  debugging, or contract drift awareness. Prefer the workspace-root
  context-brain over reading every service repo.
---

# Context Discovery

Workspace **brain** for a root that contains **N** first-level folders (microservices and/or infra) — count is whatever the workspace has. It answers: what each folder is, how they talk, what tends to break together, and which bugs/drift we already know — so you do **not** re-read every related project for every task.

## Where the brain lives

**Only** at the **workspace root**, as a sibling of the service folders — never inside a microservice folder.

```text
workspace-root/                 ← Cursor workspace / monorepo root
  serviceA/                     ← microservice code (do NOT put brain here)
  serviceB/
  infra-foo/
  context-brain/                ← YES: brain lives only here
    index.md
    map.md
    services.md                 ← one doc; ## section per service
    findings.md
```

Wrong: `serviceA/context-brain/`, `serviceB/docs/brain/`, etc.

The skill definition installs in Cursor (`~/.cursor/skills/context-discovery`). The brain **data** is created/updated under that workspace root’s `context-brain/`.

## Progressive disclosure

| Load | When |
|------|------|
| This `SKILL.md` | Skill triggers |
| `context-brain/index.md` | **Always** when you need service/plan context |
| `context-brain/map.md` | Before plans, cross-service work, or drift checks |
| `context-brain/services.md` | Only the `## <folder>` **sections** in scope (not necessarily the whole file) |
| `context-brain/findings.md` | Debugging, drift, or plans that touch known hotspots |
| Skill `references/*` | Bootstrapping, scanning, or unsure how to update |

**Rule:** prefer the brain over opening many service trees. Spot-check real code only when the brain is missing, stale, contradictory, or you are about to change a contract. Never load every service section “just in case.”

## When this skill applies

- Before writing or executing an **implementation plan** in this workspace
- Before **development** that may affect or depend on another service
- When the user asks for **context**, how services interact, or “what talks to X”
- After finishing a job that changed APIs, events, shared config, or cross-service behavior → **update brain**
- When debugging something that might span services → read findings + map; **log bugs** in findings

Skip when the task is purely inside one service with zero neighbor contracts **and** that service’s section is already solid (still skim `index.md` if unsure).

## Brain layout

Create on first use from [templates/](templates/):

```text
context-brain/
  index.md       # catalog of all first-level folders + navigation
  map.md         # edges: who calls whom
  services.md    # ## section per service / infra folder
  findings.md    # bugs + drift
```

First-level directories under the workspace root are candidates. Ignore: `.git`, `.cursor`, `context-brain`, `node_modules`, `vendor`, `dist`, `bin`, editor/OS junk.

Classify: `service` | `infra` | `shared` | `ignore`.

### `services.md` — section per folder

One markdown file; **one `## <folder-name>` section per catalog entry** (same name as the first-level directory). Add/remove sections when folders appear or disappear. Keep sections short; link into the service tree with paths like `serviceA/internal/api/...`.

When reading: jump to in-scope headings only (search `## serviceA`), do not ingest unrelated sections.

## Workflow

```
Context Progress:
- [ ] Need context? → context-brain/index.md (+ map if cross-service)
- [ ] Read only in-scope ## sections in services.md
- [ ] If gap/stale → targeted scan of those folders (references/scanning-go.md)
- [ ] Plan / develop using brain for interactions
- [ ] Drift check when contracts change
- [ ] After job: update brain; log bugs/drift in findings
```

### 1. Bootstrap (brain missing or empty)

1. Create `context-brain/` at the **workspace root** (sibling of services). Seed from [templates/](templates/).
2. List first-level folders → `index.md` catalog.
3. Targeted scan — [references/scanning-go.md](references/scanning-go.md).
4. Fill `map.md` and a `##` section per folder in `services.md`.
5. Summaries and contracts only — no codebase dumps.
6. Suggest committing workspace-root `context-brain/` with the workspace.

### 2. Before a plan or cross-service task

1. Read `index.md` + `map.md`.
2. Read only in-scope `##` sections in `services.md`.
3. Skim `findings.md` for open issues on those edges.
4. Only then open service code for gaps.

### 3. During development

- `map.md` + relevant service sections = interaction model.
- New edge/config → update brain when confident.
- A changed, B not aligned → **drift**.

### 4. After the job

Routine updates: apply when confident. **Ask** for large rewrites, weak evidence, or big deletes. Append findings for bugs/drift.

## Edges (how services interact)

| Kind | Record |
|------|--------|
| HTTP/REST | Caller → `path`; env host key |
| gRPC | Proto/service; client vs server folder |
| Async | Topic/queue; publisher → consumer |
| Config/env | Shared URLs, flags, discovery keys |
| Auth | Token/introspect dependencies |
| Infra | Deploy/pipeline coupling |

Mark `confidence: high|medium|low`.

## Drift

One side of a paired contract moved; the other did not.

1. **Warn** in chat (edge, A vs B, mismatch).
2. **Log** in `findings.md` (`type: drift`) — see [references/drift.md](references/drift.md).
3. Continue only with user ack or paired fix in scope.

## Findings

Bugs and drift in `findings.md`. Status: `open` | `mitigated` | `resolved`. Do not delete history.

## Write policy

| Change | Policy |
|--------|--------|
| Routine index/map/section updates with clear evidence | Apply directly |
| Weak evidence | `confidence: low` or ask |
| Large restructure / mass delete | Ask first |
| Findings | Append; warn on drift |

## Coupling with other skills

- Multi-service plan/dev: this skill first → then `golang-development` for Go implementation.
- Multi-service PR review: skim brain, then `golang-code-review`.
- Brain = **what talks to what**. Go skills = **how to implement / review** code.
- Go discoveries log to `.cursor/golang-discoveries.md` (golang-development) — not into `context-brain/`.

## Done means

- Used workspace-root `context-brain` before broad service reads
- In-scope sections + map updated when this job taught something
- Drift warned + logged when applicable
- Bugs worth remembering in findings

## Common failure modes

| Rationalization | Counter |
|-----------------|---------|
| Put brain inside `serviceA/` | Only workspace-root `context-brain/` |
| Read every service folder | index → map → in-scope `##` sections only |
| Skip brain update after API change | Update after contract moves |
| Drift ignored | Warn + findings |
| Paste huge code into sections | Paths + contract summary |
| Load entire `services.md` always | Only needed headings |
