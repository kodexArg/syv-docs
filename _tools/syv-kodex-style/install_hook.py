#!/usr/bin/env python3
"""Idempotently install the post-commit hook that feeds syv-kodex-style, and
seed the cursor at the current HEAD so the process only learns from work done
from now on (no noisy back-scan of history).
"""
from __future__ import annotations

import json
import stat
import subprocess
from pathlib import Path

REPO = Path(
    subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    ).stdout.strip()
)
HOOK = REPO / ".git" / "hooks" / "post-commit"
STATE = REPO / "_tools" / "syv-kodex-style" / "state.json"
WORKER = "_tools/syv-kodex-style/queue_commit.py"
MARK = "# >>> syv-kodex-style >>>"
BLOCK = f"""{MARK}
python3 "$(git rev-parse --show-toplevel)/{WORKER}" >/dev/null 2>&1 || true
# <<< syv-kodex-style <<<"""


def main() -> None:
    existing = HOOK.read_text() if HOOK.exists() else ""
    if MARK in existing:
        print("hook already installed")
    else:
        if not existing:
            content = "#!/usr/bin/env bash\n" + BLOCK + "\n"
        else:
            content = existing.rstrip() + "\n\n" + BLOCK + "\n"
        HOOK.write_text(content)
        HOOK.chmod(HOOK.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"installed -> {HOOK}")

    if not STATE.exists():
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True
        ).stdout.strip()
        STATE.write_text(json.dumps({"last_sha": head}, indent=2))
        print(f"cursor seeded at {head[:8]}")
    else:
        print("cursor already present, left untouched")


if __name__ == "__main__":
    main()
