#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes the Cursor agent to trigger
(read the skill) for a set of queries. Outputs results as JSON.

Uses the Cursor Agent CLI (`agent -p`) and installs a temporary skill under
`.cursor/skills/` so it appears in the agent's discovered skills list.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import parse_skill_md


def find_project_root() -> Path:
    """Find the project root by walking up from cwd looking for .cursor/ or .git/.

    Prefers a directory that already has `.cursor/` so temp skills land where
    Cursor will discover them; falls back to the nearest git root, then cwd.
    """
    current = Path.cwd()
    cursor_root = None
    git_root = None
    for parent in [current, *current.parents]:
        if cursor_root is None and (parent / ".cursor").is_dir():
            cursor_root = parent
        if git_root is None and (parent / ".git").exists():
            git_root = parent
        if cursor_root and git_root:
            break
    return cursor_root or git_root or current


def _path_mentions_skill(path: str, clean_name: str) -> bool:
    normalized = path.replace("\\", "/")
    return bool(clean_name) and clean_name in normalized and "SKILL.md" in normalized


def _skill_triggered_from_event(event: dict, clean_name: str) -> bool | None:
    """Return True if the event clearly indicates the skill was read, else None."""
    event_type = event.get("type")

    if event_type == "tool_call":
        tool_call = event.get("tool_call") or {}
        for _key, payload in tool_call.items():
            if not isinstance(payload, dict):
                continue
            args = payload.get("args") or {}
            path = str(args.get("path") or args.get("file_path") or args.get("target_file") or "")
            if _path_mentions_skill(path, clean_name):
                return True
            skill = str(args.get("skill") or args.get("name") or "")
            if clean_name and clean_name in skill:
                return True
        return None

    if event_type == "assistant":
        message = event.get("message") or {}
        for content_item in message.get("content") or []:
            if content_item.get("type") != "tool_use":
                continue
            tool_input = content_item.get("input") or {}
            path = str(tool_input.get("path") or tool_input.get("file_path") or "")
            skill = str(tool_input.get("skill") or "")
            if _path_mentions_skill(path, clean_name) or (clean_name and clean_name in skill):
                return True

    return None


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Creates a temporary skill under `.cursor/skills/` so it appears in Cursor's
    discovered skills list, then runs `agent -p` with stream-json and watches
    for a Read (or equivalent) of that skill's SKILL.md.
    """
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    skills_dir = Path(project_root) / ".cursor" / "skills"
    skill_dir = skills_dir / clean_name
    skill_md = skill_dir / "SKILL.md"

    try:
        skills_dir.mkdir(parents=True, exist_ok=True)
        skill_dir.mkdir(parents=True, exist_ok=True)
        indented_desc = "\n  ".join(skill_description.split("\n"))
        skill_content = (
            f"---\n"
            f"name: {clean_name}\n"
            f"description: |\n"
            f"  {indented_desc}\n"
            f"---\n\n"
            f"# {skill_name}\n\n"
            f"This skill handles: {skill_description}\n"
        )
        skill_md.write_text(skill_content, encoding="utf-8")

        cmd = [
            "agent",
            "-p", query,
            "--output-format", "stream-json",
            "--workspace", project_root,
            "--trust",
        ]
        if model:
            cmd.extend(["--model", model])

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=project_root,
            env=os.environ.copy(),
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        triggered = False
        start_time = time.time()
        buffer_lines: list[str] = []
        done = threading.Event()

        def _reader():
            assert process.stdout is not None
            for line in process.stdout:
                buffer_lines.append(line)
            done.set()

        reader = threading.Thread(target=_reader, daemon=True)
        reader.start()

        try:
            while time.time() - start_time < timeout:
                while buffer_lines:
                    line = buffer_lines.pop(0).strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    result = _skill_triggered_from_event(event, clean_name)
                    if result is True:
                        return True
                    if event.get("type") == "result":
                        return triggered

                if process.poll() is not None and done.is_set():
                    break
                time.sleep(0.05)

            # Drain any remaining lines
            while buffer_lines:
                line = buffer_lines.pop(0).strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                result = _skill_triggered_from_event(event, clean_name)
                if result is True:
                    return True
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()

        return triggered
    finally:
        if skill_dir.exists():
            shutil.rmtree(skill_dir, ignore_errors=True)


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=4, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=90, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model to use for agent -p (default: user's configured model)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)
        print(f"Project root: {project_root}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
