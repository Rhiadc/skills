# goskills

Cursor Agent skills for Go development, Go code review, and multi-service workspace context.

Install a skill once under `~/.cursor/skills/`; Cursor can then use it in any project. Skill **definitions** live in this repo. For context-discovery, the **brain data** lives at the **workspace root** (beside the service folders), never inside an individual microservice.

---

## Skills

### [golang-development](golang-development/)

Teaches the agent how to **write and change Go code** well.

- Light vs full mode depending on change size/risk
- Always-on Go practices + *100 Go Mistakes* catalog
- Progressive disclosure: extra refs (security, concurrency, architecture, tests) only when needed
- Lint / vet / tests before calling work done
- End-of-job **discoveries** so the skill can improve over time (with your OK to log)

Use when implementing features, fixing bugs, refactoring, or executing a plan that touches Go.

### [golang-code-review](golang-code-review/)

Runs a structured **Go code review** (quality, tests, security, architecture, concurrency) and writes a review markdown deliverable.

- Multi-lens review grounded in *100 Go Mistakes*, go.dev, and related cues
- Explicit attach/name only (`disable-model-invocation`) — not for day-to-day coding

Use when you ask for a PR/diff/code review of Go, not when you want code written.

### [context-discovery](context-discovery/)

Maintains a **context brain** at the **workspace root** for any number of sibling folders (Go microservices, infra, etc. — N is not fixed).

- One `services.md` with a **`##` section per service/folder**
- Maps how they interact (HTTP, gRPC, events, config, …)
- Agent reads the brain before plans / cross-service work instead of scanning every repo
- Updates as work reveals new edges; logs **bugs** and **drift** in findings
- Progressive disclosure: index → map → only the in-scope service sections

Use in multi-service workspace roots for planning, development context, and cross-service awareness.

---

## Install

From this repo root, run the install script. Default installs the three skills above into `~/.cursor/skills` via **symlink** (so `git pull` updates them).

### macOS / Linux

```bash
chmod +x install.sh
./install.sh
```

### Windows (PowerShell)

```powershell
.\install.ps1
```

If symlink creation fails without elevation, the script falls back to a directory junction.

### Useful options

```bash
# List skills
./install.sh --list

# One skill only
./install.sh context-discovery

# Copy instead of symlink (snapshot; re-run after pull to refresh)
./install.sh --copy

# Install into a single project instead of global
./install.sh --dest /path/to/your-app/.cursor/skills
```

PowerShell equivalents:

```powershell
.\install.ps1 -List
.\install.ps1 context-discovery
.\install.ps1 -Mode copy
.\install.ps1 -Dest C:\path\to\your-app\.cursor\skills
```

Then restart Cursor or open a new Agent chat.

Verify:

```bash
ls ~/.cursor/skills/golang-development/SKILL.md
ls ~/.cursor/skills/golang-code-review/SKILL.md
ls ~/.cursor/skills/context-discovery/SKILL.md
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

On first use, the agent seeds `context-brain/` from `context-discovery/templates/`. Commit that folder at the workspace root so sessions share the same map.

---

## Notes

- Install into `~/.cursor/skills/`, never `~/.cursor/skills-cursor/` (Cursor built-ins).
- Override destination with `--dest` / `-Dest` or env `CURSOR_SKILLS_DIR`.
