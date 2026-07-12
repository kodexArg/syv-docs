#!/usr/bin/env python3
"""Engine for /syv-highlight-marks — scan & apply <mark> spans (any mark).

The corpus is marked live in Obsidian, usually with the Highlightr plugin,
but this engine resolves **any** `<mark>…</mark>`:

    <mark style="background: #RRGGBBAA;">TEXTO {nota de kodex}</mark>
    <mark class="hltr-red">TEXTO {nota de kodex}</mark>
    <mark>TEXTO {nota de kodex}</mark>

Two protocols, combined:
  * the COLOR (hex, alpha ignored), when present, encodes the SEVERITY /
    action via **nearest palette colour** (robust to unknown/custom hex —
    general behaviour, not an exception path); and
  * an optional `{...}` brace inside encodes the SPECIFIC instruction, which
    always wins over the color-derived default.

A bare `<mark>` or a `class`-only mark (no resolvable hex) has no color to
classify, so it defaults to **medium severity** (`yellow` / refactor
moderado) unless the `{nota}` says otherwise.

Closed marks are pending work; an UNCLOSED `<mark>` means kodex is still
typing — this engine never sees it (the regex requires `</mark>`).

This file does the two deterministic halves of the loop:

  scan  <folder>   walk *.md recursively, emit a JSON worklist of every
                   CLOSED mark span (file, color, action, span, notes...).
  apply            read a JSON list of {file, old, new} from stdin and do a
                   literal in-place single replace of each `old` span by
                   `new` (the filesystem write path — sed -i in spirit, but
                   literal, count=1, UTF-8 safe). Avoids the MCP etag
                   collision that Obsidian Git auto-commits cause on live
                   writing.

The REASONING half (what `new` should be, per color + note) is the caller's
job (Opus, house prose voice). The MCP write path is the caller's job too
(mcp__markdown-vault-syv__edit) — this engine is the filesystem backend.

Python 3.13, stdlib only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Mark palette (RGB; alpha = last 2 hex digits, ignored). Three axes:
#   fidelity  — how much the MEANING may move: yellow < orange < red
#   lyric+    — add lyricism: purple (a lot, any register) ·
#               pink 🩷 (more creative in a TENDER key: sensual/calm/peace/love, no violence)
#   calm      — lower the temperature: blue (was too purple/pompous → sober) ·
#               cyan 🩵 (calmer & INTROSPECTIVE: inner quiet, a small pleasure)
# Plus the two loop-structural colours: green (approve→canon), gray (flow/typo).
PALETTE: dict[str, tuple[int, int, int]] = {
    "red": (0xFF, 0x55, 0x82),
    "orange": (0xFF, 0xB8, 0x6C),
    "yellow": (0xFF, 0xF3, 0xA3),
    "green": (0xBB, 0xFA, 0xBB),
    "gray": (0xCA, 0xCF, 0xD9),
    "purple": (0xBE, 0x9F, 0xFF),   # Highlightr lavender — add MUCH more lyric
    "pink": (0xFF, 0x8A, 0xD8),     # 🩷 rose — more creative, TENDER register: sensual/calm/peace/love, no violence
    "blue": (0x4C, 0x6E, 0xF5),     # strong blue — too purple/pompous → calm it
    "cyan": (0x6C, 0xE0, 0xE8),     # 🩵 celeste heart — calmer, INTROSPECTIVE: inner quiet, a small pleasure
}
ACTION: dict[str, str] = {
    "red": "negate",              # negar lo que se dice → reescribir el contenido
    "orange": "paraphrase",       # decir LO MISMO con otras palabras
    "yellow": "light-touch",      # retoque muy suave (typo/ritmo mínimo, sentido intacto)
    "gray": "flow",               # flujo / typo (lo nombra el brace)
    "green": "approve",           # aprobado → solo quitar la marca
    "purple": "lyric-more",       # agregar MUCHA más lírica
    "pink": "tender",             # más creativo, registro tierno: sensual/calmo/paz/amor, sin violencia
    "blue": "de-purple",          # demasiado cursi/rimbombante → tranquilizar
    "cyan": "introspective",      # más tranquilo e introspectivo: quietud interior, algún placer
}
# Higher = touch first. Meaning-moving reds/oranges rank above enhancers so
# corrections land before embellishment; light-touch/flow/approve at the floor.
SEVERITY = {
    "red": 8, "orange": 7, "blue": 6, "purple": 5, "cyan": 4,
    "pink": 3, "yellow": 2, "gray": 1, "green": 0,
}
DEFAULT_COLOR = "yellow"  # bare/class-only <mark>, no resolvable hex → light touch

# Matches ANY closed <mark>, capturing an optional hex from `background:#…`
# if present. Tolerant to spacing, 6- or 8-digit hex, and to marks with no
# style at all (bare `<mark>` or `class="..."` only — group(1) is None).
MARK_RE = re.compile(
    r"<mark\b(?:[^>]*?background\s*:\s*#([0-9A-Fa-f]{6})(?:[0-9A-Fa-f]{2})?)?[^>]*>(.*?)</mark>",
    re.DOTALL,
)
BRACE_RE = re.compile(r"\{([^{}]*)\}")

SKIP_DIRS = {".git", ".obsidian", ".claude", "_tools", "node_modules",
             ".venv", ".mvmcp", "__pycache__", ".pytest_cache"}


def classify(hex6: str) -> str:
    """Nearest palette colour by Euclidean distance in RGB."""
    r, g, b = int(hex6[0:2], 16), int(hex6[2:4], 16), int(hex6[4:6], 16)
    return min(
        PALETTE,
        key=lambda name: sum(
            (c - v) ** 2 for c, v in zip((r, g, b), PALETTE[name])
        ),
    )


def iter_md(target: Path):
    """Yield *.md under a folder, or the single file if target is one .md."""
    if target.is_file():
        if target.suffix == ".md":
            yield target
        return
    for p in sorted(target.rglob("*.md")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def scan(folder: Path, root: Path) -> list[dict]:
    work: list[dict] = []
    for path in iter_md(folder):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for m in MARK_RE.finditer(text):
            hex6, inner = m.group(1), m.group(2)
            if hex6:
                hex6 = hex6.upper()
                color = classify(hex6)
            else:
                color = DEFAULT_COLOR  # bare/class-only mark → medium default
            notes = [n.strip() for n in BRACE_RE.findall(inner)]
            prose = BRACE_RE.sub("", inner).strip()
            work.append(
                {
                    "file": str(path.relative_to(root)),
                    "color": color,
                    "action": ACTION[color],
                    "severity": SEVERITY[color],
                    "hex": hex6,
                    "line": text.count("\n", 0, m.start()) + 1,
                    "span": m.group(0),   # exact bytes to replace
                    "inner": inner,
                    "prose": prose,        # inner minus {notes}
                    "notes": notes,        # kodex's {...} instructions
                }
            )
    work.sort(key=lambda w: (-w["severity"], w["file"], w["line"]))
    return work


def apply(items: list[dict], root: Path) -> dict:
    """items: [{file, old, new}]. Literal single replace, in place."""
    done, failed = [], []
    by_file: dict[str, list[dict]] = {}
    for it in items:
        by_file.setdefault(it["file"], []).append(it)
    for rel, edits in by_file.items():
        path = (root / rel)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            failed += [{"file": rel, "old": e_["old"], "error": str(e)} for e_ in edits]
            continue
        for e in edits:
            old, new = e["old"], e["new"]
            n = text.count(old)
            if n == 0:
                failed.append({"file": rel, "old": old, "error": "span not found"})
                continue
            text = text.replace(old, new, 1)  # first occurrence only
            done.append({"file": rel, "old": old[:60], "replaced": True, "ambiguous": n > 1})
        path.write_text(text, encoding="utf-8")
    return {"applied": len(done), "failed": len(failed), "done": done, "errors": failed}


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parents[2]  # syv-docs/
    if not argv:
        print(__doc__)
        return 2
    cmd = argv[0]
    if cmd == "scan":
        if len(argv) > 1:
            arg = Path(argv[1])
            target = arg if arg.is_absolute() else (root / arg)
            target = target.resolve()
        else:
            target = root
        work = scan(target, root)
        print(json.dumps(work, ensure_ascii=False, indent=2))
        return 0
    if cmd == "apply":
        payload = json.load(sys.stdin)
        items = payload if isinstance(payload, list) else payload.get("items", [])
        result = apply(items, root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["failed"] == 0 else 1
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
