#!/usr/bin/env python3
"""Pairing engine for syv-kodex-style.

Reads the generation ledger (what Claude produced) and git history, finds every
in-scope file that kodex modified AFTER a known Claude generation, and emits
JSON pairs <mine -> kodex's revision> with unified diffs — ready for the LLM in
/syv-kodex-style to judge into the three learnings.

Source of truth is git history (not queue.jsonl), so it works even if the
post-commit hook never fired. CONSERVATIVE: a file is only paired when "mine"
can be attributed (ledger entry, or a Co-Authored-By: Claude commit). If neither
exists, the file is skipped — we never invent a learning from text we can't
prove was ours.

    pair.py            # dry run: print pending pairs, do not move the cursor
    pair.py --commit   # print pairs AND advance the cursor to HEAD
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCOPE = ("1_trasfondo/", "4_diegesis/", "5_aventuras/")
HERE = Path(__file__).resolve().parent
LEDGER = HERE / "generations.jsonl"
STATE = HERE / "state.json"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def gits(*args: str) -> str:
    return git(*args).strip()


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def is_ancestor(a: str, b: str) -> bool:
    if not a or not b:
        return False
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", a, b]
    ).returncode == 0


def main(argv: list[str]) -> None:
    advance = "--commit" in argv
    ledger = load_jsonl(LEDGER)
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    last = state.get("last_sha", "")
    head = gits("rev-parse", "HEAD")

    if last == head:
        print(json.dumps({"head": head, "from": last, "pairs": [], "note": "nothing new"}, indent=2))
        return

    rng = f"{last}..HEAD" if last else "HEAD"
    shas = gits("rev-list", "--reverse", rng).splitlines()

    # file -> latest non-Claude commit in range that touched it (kodex's revision)
    theirs_by_file: dict[str, str] = {}
    for sha in shas:
        claude = "Co-Authored-By: Claude" in git("log", "-1", "--format=%b", sha)
        if claude:
            continue
        changed = gits(
            "diff-tree", "--no-commit-id", "--name-only", "-r", sha
        ).splitlines()
        for f in changed:
            if f.endswith(".md") and f.startswith(SCOPE):
                theirs_by_file[f] = sha  # keep the most recent

    pairs = []
    for f, theirs_sha in theirs_by_file.items():
        mine_sha = None
        source = None
        # 1) ledger: my latest recorded generation of f that precedes theirs
        for g in reversed(ledger):
            if g.get("file") == f and is_ancestor(g["sha"], theirs_sha) and g["sha"] != theirs_sha:
                mine_sha, source = g["sha"], "ledger"
                break
        # 2) fallback: a Co-Authored-By: Claude commit on f
        if mine_sha is None:
            log = gits("log", "--format=%H", "--grep", "Co-Authored-By: Claude", "--", f).splitlines()
            cand = next((s for s in log if is_ancestor(s, theirs_sha) and s != theirs_sha), None)
            if cand:
                mine_sha, source = cand, "claude-trailer"
        # 3) can't attribute -> skip (never guess)
        if mine_sha is None:
            continue

        diff = git("diff", "--no-color", mine_sha, theirs_sha, "--", f)
        if not diff.strip():
            continue
        my_additions = git("diff", "--no-color", f"{mine_sha}~1", mine_sha, "--", f)
        pairs.append({
            "file": f,
            "source": source,
            "mine_sha": mine_sha,
            "theirs_sha": theirs_sha,
            "diff": diff,
            "my_additions": my_additions,
        })

    if advance:
        STATE.write_text(json.dumps({"last_sha": head}, indent=2))

    print(json.dumps(
        {"head": head, "from": last or None, "advanced": advance, "pairs": pairs},
        ensure_ascii=False, indent=2,
    ))


if __name__ == "__main__":
    main(sys.argv[1:])
