#!/usr/bin/env python3
"""pre-push hook worker for syv-kodex-style.

The push is the trigger moment — pushes consolidate a session's worth of
Obsidian auto-commits, a far better learning boundary than every single commit.
This worker does NOT run the analysis: it records the pushed tip (audit) and
prints a reminder so kodex runs the /syv-kodex-style skill BY HAND.

It must NEVER block a push (a non-zero exit aborts the push), so it swallows all
errors and exits 0. Git feeds the pre-push hook on stdin, one line per ref:
    <local ref> <local oid> <remote ref> <remote oid>
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUSHES = HERE / "pushes.jsonl"
ZERO = "0" * 40


def main() -> None:
    pushed = []
    for line in sys.stdin:
        parts = line.split()
        if len(parts) != 4:
            continue
        local_ref, local_oid, remote_ref, _remote_oid = parts
        if local_oid == ZERO:  # branch deletion, nothing to learn from
            continue
        pushed.append(
            {"local_ref": local_ref, "local_oid": local_oid, "remote_ref": remote_ref}
        )
    if not pushed:
        return
    rec = {
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "pushed": pushed,
    }
    with PUSHES.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    sys.stderr.write(
        "\n✍️  syv-kodex-style: push detectado — corré "
        "/syv-kodex-style para aprender del lápiz rojo de kodex.\n\n"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
