#!/usr/bin/env python3
"""post-commit hook worker for syv-kodex-style.

Cheap, no LLM. On every commit it records — into queue.jsonl — any commit that
touches in-scope narrative prose (1_trasfondo / 4_diegesis / 5_aventuras). This
is the "se dispara en cada commit" trigger + audit log. It NEVER blocks or fails
a commit: all errors are swallowed and it always exits 0.

Pairing/analysis does NOT depend on this file existing — pair.py reads git
history directly — so a missed hook (e.g. a commit made by a git library that
skips native hooks) only costs the notification, not the learning.
"""
from __future__ import annotations

import datetime
import json
import subprocess
import sys
from pathlib import Path

SCOPE = ("1_trasfondo/", "4_diegesis/", "5_aventuras/")
HERE = Path(__file__).resolve().parent
QUEUE = HERE / "queue.jsonl"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], capture_output=True, text=True
    ).stdout.strip()


def main() -> None:
    sha = git("rev-parse", "HEAD")
    if not sha:
        return
    parent = git("rev-parse", "HEAD~1")
    if parent:
        changed = git("diff", "--name-only", parent, sha).splitlines()
    else:
        changed = git("show", "--name-only", "--format=", sha).splitlines()
    files = [f for f in changed if f.endswith(".md") and f.startswith(SCOPE)]
    if not files:
        return
    rec = {
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "sha": sha,
        "parent": parent,
        "author": git("log", "-1", "--format=%an"),
        "email": git("log", "-1", "--format=%ae"),
        "message": git("log", "-1", "--format=%s"),
        "claude_trailer": "Co-Authored-By: Claude" in git("log", "-1", "--format=%b"),
        "files": files,
    }
    with QUEUE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
