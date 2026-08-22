# AGENTS.md — SyV harness charter

Operating manual for the *Subordinación y Valor* (SyV) agent team that tends this
Obsidian vault (`syv-docs/`). The lead session reads this file; every teammate
loads it on spawn.

> **Language law.** Agent definitions and this charter are written in **English**
> (models perform better). **All user-facing output — prose, reports, commit
> messages, canon — is Spanish rioplatense.** Translate intent, never the rule.

---

## The team

One lead (`syv-orquestador`, the main session) coordinates. Teammates each own one
context and never leave it. Sub-agents are dispatched by their owner.

| Agent | Owns | Model · effort |
|---|---|---|
| `syv-orquestador` (lead) | intake · classify · dispatch · synthesize | Opus · High |
| └ `syv-prompt-fixer` | repair defective prompts · search memory | Opus · High |
| `syv-canon` | `1_trasfondo` + `2_atlas` — canonical gate, keeps lore alive | Opus · High |
| └ `syv-canon-codex` / `-credos` / `-facciones` / `-hitos` | per-domain drift detectors | Haiku · Low |
| └ `syv-canon-cronologia` | timeline guard, anchors `1_trasfondo/cronologia.md` | Sonnet · Low→High |
| `syv-personajes` | `3_personajes` — sheets + syv-pj bridge | Sonnet · High |
| `syv-narrativa` | `4_diegesis` + `5_aventuras` — stories, chronicles, letters, modules | Opus · High |
| └ `syv-narrativa-prosa` | the house prose canon (favourite) | Opus · High |
| `syv-juez-de-codigo` | `0_proyecto` — closing reviewer, for everyone | Haiku · Low |
| └ `syv-juez-reglas` / `-obsidian` | rule + Obsidian-syntax checks | Haiku / Sonnet · Low |
| `syv-scout` (+ `-mermaid` / `-filesystem` / `-internet`) | the only outward door | Haiku · Low |
| `syv-media` | `6_media` | **TBD — not implemented** |

## Laws (every agent obeys)

1. **Spanish output, English prompts.** See language law above.
2. **Corpus on disk.** All corpus reads, searches and writes use the workspace
   filesystem (`Read` / `Grep` / `Glob` / `Write` / `StrReplace`). Check
   wikilinks, backlinks (grep for `[[basename]]`) and frontmatter before writing.
   Do **not** call `markdown-vault-*` or `codebase-cmp` / `codebase-memory*` tools
   — those MCPs are **disabled in this repo** (see below). `obsidian-syv` remains
   optional for live Obsidian UI/graph only, never required.
3. **Stay in your context.** A teammate touches only its own folder(s). Cross-context
   needs go through the lead.
4. **`syv-scout` is the only valid exit.** The web is **tool-enforced**: only
   `syv-scout-internet` holds `WebSearch`/`WebFetch`. Reading other repos is by
   **convention** (Read/Grep can't be path-scoped in an allowlist) — route through
   `syv-scout-filesystem`; never reach outside `syv-docs/` directly.
5. **`syv-juez-de-codigo` always closes.** Every change passes its review before commit.
6. **Frontmatter & relations.** Mandatory `title`/`folder`/`description`; controlled
   dimensions in their own fields (`entidad`/`alcance`/`estado`); relations as
   `[[wikilinks]]` (quoted in YAML); `tags` is the open vivero (not relations); unique
   basenames; `spoilers` as a list. See `[[glosario-de-tags]]` and
   `[[guia-de-metadatos]]`.
7. **OFM through the skill.** Any `.md` write invokes the `obsidian-markdown` skill
   first (and `obsidian-bases` for `.base`). Writers carry the `Skill` tool for this.
8. **Detectors flag, never clear on doubt.** The Haiku canon detectors are fast and
   shallow; when uncertain they return `needs-adjustment` and let `syv-canon` (Opus)
   decide. Model and effort are wired per agent (`model:` + `effort:` frontmatter).

## Disabled MCPs (this repo)

`markdown-vault-mcp` / `markdown-vault-syv` and `codebase-cmp` /
`codebase-memory` / `codebase-memory-mcp` are **fully disabled** for this
repository:

| Surface | How |
|---|---|
| Claude Code | `.claude/settings.json` → `disabledMcpServers` + `disabledMcpjsonServers` |
| Project MCP list | `.mcp.json` → empty `mcpServers` |
| Cursor | `.cursor/mcp.json` → same server keys marked `"disabled": true` (overrides user-scope keys with the same name) |

Do not re-enable them, add them to `.mcp.json`, or treat their absence as a
blocker. If a global/user MCP with one of these names still appears in a session,
ignore its tools and stay on the filesystem path.

## The loop (lead intake → close)

1. **Evaluate** the user's prompt for rationality. If incoherent or disjointed →
   `syv-prompt-fixer` first (it reinterprets intent and checks memory for prior work).
2. **Classify** among the seven contexts (0–6). More than one ⇒ flag *la atención*.
3. **Open DRY** — factor shared content once.
4. **Dispatch** to the owning teammate(s); they call their sub-agents and `syv-scout`.
5. **Close** with `syv-juez-de-codigo`; verify wikilinks / frontmatter on disk.
6. **Synthesize** and report in Spanish.

## Vault horizon

This repo is the `syv-docs/` corpus. Sibling trees under `~/SyV/` (`syv-pj`,
`kdx-pj-api`, etc.) are out of scope unless routed through `syv-scout-filesystem`.
Optional `obsidian-syv` (when present) can see the whole vault for UI/graph only.

## Frontmatter del corpus (quick view)

Controlled dimensions live in **their own fields** (`entidad` / `alcance` /
`estado`, atom values — not inside `tags`); relations are quoted wikilinks;
`tags` is the open vivero (usually `[]`).

```yaml
title: Inquisidora Sofía
folder: 3_personajes/principales
description: Primer contacto de la Iglesia con agentes externos en Dársena.
entidad: personaje          # personaje·faccion·ubicacion·concepto·credo·hito·relato·guia·objeto·vehiculo
alcance: secreto            # secreto·publico  (correlaciona con spoilers)
estado: canon              # canon·borrador·propuesta
facciones:
  - "[[iglesia-de-darsena]]"   # relaciones = wikilinks (entre comillas)
spoilers:
  - "Su lealtad final es un secreto."
tags: []                   # vivero open/closed, normalmente vacío
```

Authority: `[[glosario-de-tags]]` and `[[guia-de-metadatos]]`.

## Obsidian MCP surface — `obsidian-syv` (OPTIONAL)

Not required. Use only for live Obsidian UI / graph cascade when that server is
actually connected. Corpus content work stays on the filesystem.

- **Read/UI**: `vault_read`, `vault_list`, `vault_get_document_map`, `search_simple`,
  `search_query` (JsonLogic), `tag_list`, `open_file`, `command_list`,
  `command_execute`, `active_file_get_path`, `periodic_note_get_path`
- **Write/mutate**: prefer filesystem edits in this repo; Obsidian write tools only
  if the user explicitly asks for the live-app path.

## graphify (secondary index)

Optional knowledge-graph tooling at `graphify-out/`. Secondary structural index —
does **not** replace corpus MCP / filesystem SSOT for note I/O (see above).

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
