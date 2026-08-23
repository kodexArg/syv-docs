#!/usr/bin/env bash
# Install graphify CLI + project skills for Cursor / Claude / Agent Skills.
# Safe to re-run. Does not build the graph (run /graphify . in the assistant for that).
#
# Prefer GitHub source (Graphify-Labs/graphify). The CLI is `graphify`; the PyPI
# distribution name is currently `graphifyy` (official double-y — not a typo-squat).
# After upstream installers, re-applies SyV overlays (no PreToolUse read guards,
# soft Cursor rule: secondary index only).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"

GRAPHIFY_GIT_URL="${GRAPHIFY_GIT_URL:-https://github.com/Graphify-Labs/graphify.git}"

ensure_uv() {
  if command -v uv >/dev/null 2>&1; then
    return 0
  fi
  echo "Installing uv…"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # shellcheck disable=SC1091
  source "${HOME}/.local/bin/env" 2>/dev/null || true
  export PATH="${HOME}/.local/bin:${PATH}"
}

install_cli() {
  if command -v graphify >/dev/null 2>&1; then
    echo "graphify already on PATH: $(command -v graphify)"
    graphify --version 2>/dev/null || true
    return 0
  fi

  ensure_uv
  if command -v uv >/dev/null 2>&1; then
    echo "Installing graphify CLI from GitHub (${GRAPHIFY_GIT_URL})…"
    uv tool install "git+${GRAPHIFY_GIT_URL}"
    export PATH="${HOME}/.local/bin:${PATH}"
    return 0
  fi

  echo "uv unavailable — falling back to official PyPI package name graphifyy…"
  python3 -m pip install --user -q graphifyy 2>/dev/null \
    || python3 -m pip install -q graphifyy --break-system-packages
}

install_cli

if ! command -v graphify >/dev/null 2>&1; then
  echo "error: graphify CLI not on PATH after install; add ~/.local/bin to PATH" >&2
  exit 1
fi

echo "graphify OK ($(command -v graphify))"

graphify cursor install
graphify install --platform agents --project
graphify install --platform claude --project

python3 - <<'PY'
from __future__ import annotations

import json
import re
from pathlib import Path

# --- Claude settings: drop PreToolUse hooks (absolute paths + MCP conflict) ---
settings = Path(".claude/settings.json")
data = json.loads(settings.read_text(encoding="utf-8")) if settings.exists() else {}
data.pop("hooks", None)
data.setdefault("env", {})["CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"] = "1"
settings.parent.mkdir(parents=True, exist_ok=True)
settings.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
print("cleared Claude PreToolUse hooks (SyV MCP-first)")

# --- Cursor rule: SyV-softened alwaysApply ---
rule = Path(".cursor/rules/graphify.mdc")
rule.parent.mkdir(parents=True, exist_ok=True)
rule.write_text(
    """\
---
description: graphify knowledge graph (secondary structural index)
alwaysApply: true
---

This project can use graphify (`graphify-out/`) as a **secondary** structural index.

**SyV precedence (do not override):**
1. Corpus note I/O follows `AGENTS.md` (filesystem first in this repo; MCP vault tools are disabled). Graphify never replaces that SSOT.
2. Config/tooling outside the corpus (`.claude/`, `_tools/`, `.cursor/`, etc.) may use graphify freely.

**Install note:** CLI command is `graphify`. Official GitHub is Graphify-Labs/graphify; PyPI package name is currently `graphifyy`. Prefer `_tools/graphify-setup.sh` (GitHub via uv).

When `graphify-out/graph.json` exists and the user asks structural/architecture questions (or types `/graphify`), prefer:
- `graphify query "<question>"` — scoped subgraph
- `graphify path "<A>" "<B>"` — path between concepts
- `graphify explain "<concept>"` — neighborhood of a concept

Also:
- If `graphify-out/wiki/index.md` exists, use it for broad navigation of the graph export
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review
- After modifying tracked code/tooling files, run `graphify update .` to refresh the graph (AST-only)

If `graphify-out/graph.json` does not exist yet, do not block on it — use normal corpus tools, and only build the graph when the user asks `/graphify`.
""",
    encoding="utf-8",
)
print(f"wrote SyV-compatible Cursor rule at {rule}")

# --- AGENTS.md: replace stock ## graphify section with SyV wording ---
agents = Path("AGENTS.md")
text = agents.read_text(encoding="utf-8")
section = """\
## graphify (secondary index)

Optional knowledge-graph tooling at `graphify-out/`. Secondary structural index —
does **not** replace the filesystem corpus SSOT for note I/O (see Laws above).

**Naming (important):** the CLI is `graphify`. On PyPI the *official* Graphify-Labs
package is currently named `graphifyy` (double-y); `graphify` alone is **not** on
PyPI. Prefer installing from the GitHub source to avoid typo-squat confusion:

```bash
./_tools/graphify-setup.sh
# or: uv tool install 'git+https://github.com/Graphify-Labs/graphify.git'
```

Cloud agents install the same way via `.cursor/environment.json` → `install`.

- Skills: `.agents/skills/graphify/`, `.claude/skills/graphify/`, Cursor rule
  `.cursor/rules/graphify.mdc`. Trigger: `/graphify`.
- When `graphify-out/graph.json` exists, `graphify query` / `path` / `explain` help
  with structural navigation (especially `_tools/` and harness config).
- After modifying code/tooling, `graphify update .` refreshes the AST graph (no LLM).
"""
# Drop every graphify H2 (stock or SyV) then append our section once.
pattern = re.compile(r"(?ms)^## graphify[^\n]*\n.*?(?=^## |\Z)")
text = pattern.sub("", text).rstrip() + "\n\n" + section.rstrip() + "\n"
agents.write_text(text, encoding="utf-8")
print("normalized AGENTS.md graphify section (SyV)")
PY

echo
echo "Done. In Cursor / Claude Code, type: /graphify ."
echo "Outputs land in graphify-out/ (gitignored)."
