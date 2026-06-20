#!/usr/bin/env python3
"""Generation ledger for syv-kodex-style — the authority on "this text is mine".

Call this RIGHT AFTER Claude writes in-scope narrative prose (via the corpus MCP
or via git), passing the file(s) just written. It snapshots the exact git blob
Claude produced into generations.jsonl.

WHY IT EXISTS: in this repo both Claude's MCP writes and kodex's hand edits in
Obsidian commit as `markdown-vault-mcp <noreply@markdown-vault-mcp>` — they are
indistinguishable by author or message. The only reliable signal that a given
snapshot was Claude's is that Claude recorded it here. pair.py then treats any
LATER, different version of the same file as kodex's modification.

Usage:
    record_generation.py <file.md> [<file.md> ...] [--note "what I wrote"]
"""
from __future__ import annotations

import datetime
import json
import subprocess
import sys
from pathlib import Path

SCOPE = ("1_trasfondo/", "4_diegesis/", "5_aventuras/")
HERE = Path(__file__).resolve().parent
LEDGER = HERE / "generations.jsonl"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], capture_output=True, text=True
    ).stdout.strip()


def main(argv: list[str]) -> None:
    note = ""
    if "--note" in argv:
        i = argv.index("--note")
        note = " ".join(argv[i + 1 :])
        argv = argv[:i]
    paths = [p for p in argv if p.endswith(".md")]
    if not paths:
        print("usage: record_generation.py <file.md> ... [--note '...']", file=sys.stderr)
        sys.exit(1)
    sha = git("rev-parse", "HEAD")
    recorded: list[str] = []
    for p in paths:
        if not p.startswith(SCOPE):
            print(f"skip (out of scope): {p}", file=sys.stderr)
            continue
        blob = git("rev-parse", f"HEAD:{p}") or git("hash-object", p)
        rec = {
            "ts": datetime.datetime.now().isoformat(timespec="seconds"),
            "file": p,
            "blob": blob,
            "sha": sha,
            "by": "claude",
            "note": note,
        }
        with LEDGER.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        recorded.append(p)
    print(f"recorded {len(recorded)} generation(s): {', '.join(recorded)}")


if __name__ == "__main__":
    main(sys.argv[1:])
