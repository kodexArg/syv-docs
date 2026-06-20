#!/usr/bin/env python3
"""Idempotently install the pre-push hook that triggers syv-kodex-style, seed the
cursor at HEAD (so the process only learns from work done from now on), and clean
up the legacy post-commit hook block if a previous version installed it.

Trigger = push, not commit: pushes consolidate a session's worth of Obsidian
auto-commits, a far better learning boundary. The hook only NOTIFIES; the
/syv-kodex-style skill is run by hand.
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
HOOKS = REPO / ".git" / "hooks"
STATE = REPO / "_tools" / "syv-kodex-style" / "state.json"
MARK_OPEN = "# >>> syv-kodex-style >>>"
MARK_CLOSE = "# <<< syv-kodex-style <<<"


def strip_block(text: str) -> str:
    """Remove our managed block from an existing hook, leaving the rest intact."""
    if MARK_OPEN not in text:
        return text
    out, skip = [], False
    for line in text.splitlines():
        if line.strip() == MARK_OPEN:
            skip = True
            continue
        if line.strip() == MARK_CLOSE:
            skip = False
            continue
        if not skip:
            out.append(line)
    return "\n".join(out).strip()


def make_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main() -> None:
    # 1) Remove the legacy post-commit block (trigger moved from commit to push).
    post_commit = HOOKS / "post-commit"
    if post_commit.exists():
        rest = strip_block(post_commit.read_text())
        if rest in ("", "#!/usr/bin/env bash"):
            post_commit.unlink()
            print("removed legacy post-commit hook")
        elif MARK_OPEN in post_commit.read_text():
            post_commit.write_text(rest + "\n")
            print("stripped syv-kodex-style block from post-commit hook")

    # 2) Install the pre-push hook (stdin must reach the worker → no redirect).
    pre_push = HOOKS / "pre-push"
    block = (
        f"{MARK_OPEN}\n"
        'python3 "$(git rev-parse --show-toplevel)/_tools/syv-kodex-style/on_push.py" || true\n'
        f"{MARK_CLOSE}"
    )
    existing = pre_push.read_text() if pre_push.exists() else ""
    if MARK_OPEN in existing:
        print("pre-push hook already installed")
    else:
        if not existing:
            content = "#!/usr/bin/env bash\n" + block + "\n"
        else:
            content = existing.rstrip() + "\n\n" + block + "\n"
        pre_push.write_text(content)
        make_executable(pre_push)
        print(f"installed -> {pre_push}")

    # 3) Seed the cursor at HEAD on first install.
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
