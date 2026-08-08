# goskills

Cursor Agent skills for Go development, Go code review, and multi-service workspace context.

Each skill is **self-contained**: its own `SKILL.md` plus its own `references/` and `templates/`. Install under `~/.cursor/skills/` and it works on its own.

Runtime data always lives in your project, never inside a skill:

- **context-discovery** brain → workspace-root `context-brain/`
- **golang-development** discoveries → project `.cursor/golang-discoveries.md`

---

## Skills

### [golang-development](golang-development/)

Teaches the agent how to **write and change Go code** well.

- Light vs full mode based on change size and risk
- Always-on standards in `SKILL.md`; deeper references load only when a gate matches
- Light mode reads a short *100 Go Mistakes* priority slice instead of the full catalog
- Lint / vet / tests before calling work done
- End-of-job discoveries, logged in the project with your OK

Use when implementing features, fixing bugs, refactoring, or executing a plan that touches Go.

### [golang-code-review](golang-code-review/)

Structured **Go code review** (quality, tests, security, architecture, concurrency) producing a review markdown deliverable.

- Specialists read the actual diff; parallel via Task, sequential fallback otherwise
- Lite mode for small diffs; optional context-brain check on multi-service PRs
- Explicit attach or name only (`disable-model-invocation`)

Use for PR/diff/code review of Go, not for writing code.

### [context-discovery](context-discovery/)

**Context brain** at the workspace root for any number of sibling service and infra folders.

- `services.md` with a `##` section per folder, interaction `map.md`, `findings.md` for bugs and drift
- Read the brain before plans and cross-service work instead of scanning every repo

---

## Install

From this repo root. Default: symlink all three skills into `~/.cursor/skills` so `git pull` keeps them current.

### macOS / Linux

```bash
chmod +x install.sh
./install.sh
```

### Windows (PowerShell)

```powershell
.\install.ps1
```

If symlink creation needs elevation, the script falls back to a directory junction.

### Useful options

```bash
./install.sh --list
./install.sh context-discovery
./install.sh --copy
./install.sh --dest /path/to/your-app/.cursor/skills
```

```powershell
.\install.ps1 -List
.\install.ps1 context-discovery
.\install.ps1 -Mode copy
.\install.ps1 -Dest C:\path\to\your-app\.cursor\skills
```

Restart Cursor or open a new Agent chat, then verify:

```bash
ls ~/.cursor/skills/golang-development/SKILL.md
ls ~/.cursor/skills/golang-code-review/SKILL.md
ls ~/.cursor/skills/context-discovery/SKILL.md
```

---

## context-discovery brain (workspace root only)

```text
workspace-root/
  serviceA/                 # microservice code
  serviceB/
  infra-foo/
  context-brain/            # brain — only here, never inside a service
    index.md                # catalog of sibling folders
    map.md                  # how they interact
    services.md             # ## section per service / infra folder
    findings.md             # bugs + drift
```

On first use the agent seeds `context-brain/` from `context-discovery/templates/`. Commit it at the workspace root so every session shares the same map.

---

## Notes

- Install into `~/.cursor/skills/`, never `~/.cursor/skills-cursor/` (Cursor built-ins).
- Override the destination with `--dest` / `-Dest` or `CURSOR_SKILLS_DIR`.
- The Go skills each keep their own copy of the shared catalogs; if you edit one (for example `go-100-mistakes.md`), consider whether the other skill needs the same edit.
