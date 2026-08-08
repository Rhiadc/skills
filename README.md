# goskills

Cursor Agent skills for Go development, Go code review, and multi-service workspace context.

Install a skill once under `~/.cursor/skills/`; Cursor can then use it in any project. Skill **definitions** live in this repo. For context-discovery, the **brain data** lives at the **workspace root** (beside the service folders), never inside an individual microservice.

---

## Skills

### [golang-development](skills/golang-development/)

Teaches the agent how to **write and change Go code** well.

- Light vs full mode depending on change size/risk
- Always-on Go practices + *100 Go Mistakes* catalog
- Progressive disclosure: extra refs (security, concurrency, architecture, tests) only when needed
- Lint / vet / tests before calling work done
- End-of-job **discoveries** so the skill can improve over time (with your OK to log)

Use when implementing features, fixing bugs, refactoring, or executing a plan that touches Go.

### [golang-code-review](skills/golang-code-review/)

Runs a structured **Go code review** (quality, tests, security, architecture, concurrency) and writes a review markdown deliverable.

- Multi-lens review grounded in *100 Go Mistakes*, go.dev, and related cues
- Explicit attach/name only (`disable-model-invocation`) — not for day-to-day coding

Use when you ask for a PR/diff/code review of Go, not when you want code written.

### [context-discovery](skills/context-discovery/)

Maintains a **context brain** at the **workspace root** for any number of sibling folders (Go microservices, infra, etc. — N is not fixed).

- One `services.md` with a **`##` section per service/folder**
- Maps how they interact (HTTP, gRPC, events, config, …)
- Agent reads the brain before plans / cross-service work instead of scanning every repo
- Updates as work reveals new edges; logs **bugs** and **drift** in findings
- Progressive disclosure: index → map → only the in-scope service sections

Use in multi-service workspace roots for planning, development context, and cross-service awareness.

---

## Install (macOS / Linux)

Cursor loads personal skills from `~/.cursor/skills/<skill-name>/`.

From **this repo’s root**, symlink (recommended — `git pull` keeps skills updated):

```bash
mkdir -p ~/.cursor/skills

ln -sfn "$(pwd)/skills/golang-development" ~/.cursor/skills/golang-development
ln -sfn "$(pwd)/skills/golang-code-review" ~/.cursor/skills/golang-code-review
ln -sfn "$(pwd)/skills/context-discovery" ~/.cursor/skills/context-discovery
```

Verify:

```bash
ls ~/.cursor/skills/golang-development/SKILL.md
ls ~/.cursor/skills/golang-code-review/SKILL.md
ls ~/.cursor/skills/context-discovery/SKILL.md
```

Restart Cursor or open a new Agent chat.

### Install only one skill

```bash
ln -sfn "$(pwd)/skills/context-discovery" ~/.cursor/skills/context-discovery
```

### Copy instead of symlink

Snapshot that does not track the repo:

```bash
mkdir -p ~/.cursor/skills
cp -R skills/golang-development ~/.cursor/skills/
cp -R skills/golang-code-review ~/.cursor/skills/
cp -R skills/context-discovery ~/.cursor/skills/
```

Re-run `cp` after you pull changes you want locally.

### One project only (not global)

```bash
mkdir -p /path/to/your-app/.cursor/skills
cp -R skills/golang-development /path/to/your-app/.cursor/skills/
# repeat for other skills as needed
```

---

## context-discovery brain (workspace root only)

The skill installs globally. Brain **files** go only at the Cursor **workspace root**, next to the service folders — **not** inside `serviceA/`, `serviceB/`, etc.

```text
workspace-root/
  serviceA/                 # microservice code
  serviceB/
  infra-foo/
  context-brain/            # brain — only here
    index.md                # catalog of all sibling folders
    map.md                  # how they interact
    services.md             # ## section per service / infra folder
    findings.md             # bugs + drift
```

On first use, the agent seeds `context-brain/` from `skills/context-discovery/templates/`. Commit that folder at the workspace root so sessions share the same map.

---

## Notes

- Install into `~/.cursor/skills/`, never `~/.cursor/skills-cursor/` (Cursor built-ins).
- Windows: `%USERPROFILE%\.cursor\skills\` (same layout; symlink or copy).
