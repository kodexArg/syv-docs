#!/usr/bin/env python3
"""
strip_framework.py — remove static-site-generator (Astro/Starlight) traces.

The vault is a pure narrative corpus. The only framework residue left in the
.md files are Astro-Starlight-specific frontmatter keys used to drive site
navigation: `sidebar`, `order`, `hidden`, `slug`. This tool strips those keys
from every frontmatter block, leaving the story metadata (title, folder,
description, aliases, tags, relations, spoilers) untouched.

Technique mirrors migrate_metadata.py: ruamel.yaml round-trip with
preserve_quotes, replacing only the frontmatter region; body bytes untouched.

Usage:
    uv run --with ruamel.yaml python _tools/strip_framework.py            # dry-run
    uv run --with ruamel.yaml python _tools/strip_framework.py --apply    # write
"""

from __future__ import annotations

import argparse
import io
import os
import re
from pathlib import Path

from ruamel.yaml import YAML

VAULT_ROOT = Path(__file__).parent.parent
SKIP_DIRS = {".git", ".obsidian", "_tools"}

# Astro/Starlight-only frontmatter keys → remove
FRAMEWORK_KEYS = ["sidebar", "order", "hidden", "slug"]

_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.width = 4096
_yaml.indent(mapping=2, sequence=4, offset=2)

_FM_RE = re.compile(r"^(---\n)(.*?)(\n---)", re.DOTALL)


def split_content(content: str):
    m = _FM_RE.match(content)
    if not m:
        return None
    return m.group(1), m.group(2), content[m.end():]


def dump_yaml(obj) -> str:
    buf = io.StringIO()
    _yaml.dump(obj, buf)
    return buf.getvalue().strip()


def collect_files(root: Path):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".md"):
                out.append(Path(dirpath) / f)
    return sorted(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", default=False)
    args = ap.parse_args()
    dry = not args.apply

    changed = []
    for fp in collect_files(VAULT_ROOT):
        rel = fp.relative_to(VAULT_ROOT).as_posix()
        content = fp.read_text(encoding="utf-8")
        split = split_content(content)
        if split is None:
            continue
        pre, fm_text, rest = split
        try:
            fm = _yaml.load(fm_text)
        except Exception as exc:
            print(f"PARSE-ERROR {rel}: {exc}")
            continue
        if not isinstance(fm, dict):
            continue
        removed = [k for k in FRAMEWORK_KEYS if k in fm]
        if not removed:
            continue
        for k in removed:
            del fm[k]
        changed.append((rel, removed))
        if not dry:
            new = pre + dump_yaml(fm) + "\n---" + rest
            fp.write_text(new, encoding="utf-8")

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== strip_framework — {mode} ===")
    for rel, removed in changed:
        print(f"  {rel}: removed {removed}")
    print(f"\n{len(changed)} file(s) {'written' if args.apply else 'would change'}.")


if __name__ == "__main__":
    main()
