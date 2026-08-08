#!/usr/bin/env bash
# Install Cursor skills from this repo into ~/.cursor/skills (or a custom dest).
# Default: symlink (tracks git pull). Use --copy for a snapshot.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CURSOR_SKILLS_DIR:-$HOME/.cursor/skills}"
MODE="symlink"
SKILLS=()

DEFAULT_SKILLS=(
  golang-development
  golang-code-review
  context-discovery
)

usage() {
  cat <<'EOF'
Usage: ./install.sh [options] [skill...]

Install skills from this repo into Cursor's personal skills directory.

Options:
  --symlink     Create symlinks (default; updates follow git pull)
  --copy        Copy directories instead of symlinking
  --dest DIR    Install target (default: ~/.cursor/skills or $CURSOR_SKILLS_DIR)
  --list        List installable skills and exit
  -h, --help    Show this help

Examples:
  ./install.sh
  ./install.sh context-discovery
  ./install.sh --copy golang-development golang-code-review
  ./install.sh --dest /path/to/project/.cursor/skills
EOF
}

list_skills() {
  echo "Default skills:"
  for s in "${DEFAULT_SKILLS[@]}"; do
    echo "  - $s"
  done
  echo
  echo "Also in repo (pass by name to install):"
  for dir in "$REPO_ROOT"/*/; do
    name="$(basename "$dir")"
    [[ -f "$dir/SKILL.md" ]] || continue
    skip=
    for d in "${DEFAULT_SKILLS[@]}"; do
      [[ "$name" == "$d" ]] && skip=1 && break
    done
    [[ -n "$skip" ]] && continue
    echo "  - $name"
  done
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --symlink) MODE="symlink"; shift ;;
    --copy) MODE="copy"; shift ;;
    --dest)
      DEST="${2:?--dest requires a directory}"
      shift 2
      ;;
    --list) list_skills; exit 0 ;;
    -h|--help) usage; exit 0 ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      SKILLS+=("$1")
      shift
      ;;
  esac
done

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  SKILLS=("${DEFAULT_SKILLS[@]}")
fi

mkdir -p "$DEST"

echo "Repo:  $REPO_ROOT"
echo "Dest:  $DEST"
echo "Mode:  $MODE"
echo

for name in "${SKILLS[@]}"; do
  src="$REPO_ROOT/$name"
  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "error: not a skill (missing SKILL.md): $name" >&2
    exit 1
  fi

  target="$DEST/$name"

  # Remove existing install (symlink or directory) so reinstall is clean
  if [[ -e "$target" || -L "$target" ]]; then
    rm -rf "$target"
  fi

  if [[ "$MODE" == "symlink" ]]; then
    ln -sfn "$src" "$target"
    echo "linked  $name -> $src"
  else
    cp -R "$src" "$target"
    echo "copied  $name -> $target"
  fi

  if [[ ! -f "$target/SKILL.md" ]]; then
    echo "error: install failed for $name (SKILL.md not reachable)" >&2
    exit 1
  fi
done

echo
echo "Done. Restart Cursor or open a new Agent chat."
echo "Verify: ls \"$DEST\""
