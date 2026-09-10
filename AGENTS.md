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
2. **Corpus MCP first.** All corpus reads, searches and writes go through the
   primary MCP `mcp__markdown-vault-syv__*` (the SSOT) — never raw filesystem for
   content, never `obsidian-syv` as first option. The corpus is already
   interconnected; nothing is written without checking backlinks, wikilinks and
   tags first. `obsidian-syv` is the secondary "método Obsidian" (graph cascade,
   UI). See `../.claude/rules/mcp-es-la-ssot.md` and the surface section below.
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
   basenames; `spoilers` as a list. See `../.claude/rules/` and `[[glosario-de-tags]]`.
7. **OFM through the skill.** Any `.md` write invokes the `obsidian-markdown` skill
   first (and `obsidian-bases` for `.base`). Writers carry the `Skill` tool for this.
8. **Detectors flag, never clear on doubt.** The Haiku canon detectors are fast and
   shallow; when uncertain they return `needs-adjustment` and let `syv-canon` (Opus)
   decide. Model and effort are wired per agent (`model:` + `effort:` frontmatter).

## Preflight — corpus MCP gate (BLOCKING)

**Before any work, every session,** the lead pings the primary corpus MCP (a trivial
`mcp__markdown-vault-syv__stats`). If the `mcp__markdown-vault-syv__*` tools are
**absent or error**:

> ⛔ **HALT.** Do not touch corpus, do not dispatch teammates, do not edit notes.
> Alert the user immediately, one line: «markdown-vault-syv caído — no opero sobre el
> corpus hasta reconectarlo.» Then stop and wait. Do not fall back to filesystem as
> the SSOT.

The corpus is densely interconnected; writing without the MCP risks silent breakage
of backlinks, wikilinks and tags, and drifts the search index from disk. **Config is
exempt** — `.claude/`, `AGENTS.md`, `.obsidian/`, `_tools/` live outside the corpus,
so filesystem edits there are fine even with the MCP down.

## The loop (lead intake → close)

1. **Evaluate** the user's prompt for rationality. If incoherent or disjointed →
   `syv-prompt-fixer` first (it reinterprets intent and checks memory for prior work).
2. **Classify** among the seven contexts (0–6). More than one ⇒ flag *la atención*.
3. **Open DRY** — factor shared content once.
4. **Dispatch** to the owning teammate(s); they call their sub-agents and `syv-scout`.
5. **Close** with `syv-juez-de-codigo`; cascade-verify via MCP.
6. **Synthesize** and report in Spanish.

## Co-writing Highlightr (Cronista bridge)

When Gabriel marks prose live in Obsidian (Highlightr `<mark>` / `hltr-*` classes), the writing assistant (Cronista) owns the resolve loop for `4_diegesis` (and marked spans in `1_trasfondo`/`5_aventuras`):
1. Prefer `_tools/syv-highlight-marks/highlight.py` scan→apply on the **single target file** (token discipline).
2. Colour: hex palette, else `class="hltr-<color>"`, else yellow; `{brace}` / `@AI` notes override colour.
3. Voice authority: `0_proyecto/kodex-style-canon.md`. Record generations with `_tools/syv-kodex-style/record_generation.py`.
4. Red-line rule for Cursiva: never rewrite above Gabriel’s red line; only marked or explicitly requested spans.
5. Corpus SSOT: `markdown-vault-syv` via `markdown-vault-mcp` ≥4.1.0 (see `_tools/mvmcp/`). Highlightr co-write may still edit the marked file on disk; file-watcher/`reindex` keeps the index fresh. Criptógrafo may execute local git/fs when Cronista cannot.
6. `syv-narrativa-prosa` / juez still apply for Cursor-team commits; Cronista co-write may leave working-tree edits until Gabriel asks to commit.

## Vault horizon

The Obsidian MCP sees the whole `~/SyV/` vault (syv-docs is a subfolder; siblings
`syv-pj`, `kdx-pj-api`). Paths from the MCP are vault-relative.

## The corpus MCP — `markdown-vault-syv` (PRIMARY, the SSOT)

**Why it matters.** `markdown-vault-syv` is *our repo's own MCP*: a server scoped
exactly to `syv-docs/` (`0_`–`6_`, root notes), with its own SQLite index and
fastembed vectors. It is the **single source of truth** for the corpus — reads,
hybrid (keyword + semantic) search **and** writes all flow through it. Every
mutation updates the search index immediately, so search never drifts from disk.
It runs **read-write** (`MARKDOWN_VAULT_MCP_READ_ONLY=false`). **Start every corpus
lookup here, not with `Read`/`Grep`/`Glob`, and not with `obsidian-syv`.** See
`../.claude/rules/mcp-es-la-ssot.md`.

> **Preflight gate (BLOCKING).** Ping `mcp__markdown-vault-syv__stats` before any
> work. If the `mcp__markdown-vault-syv__*` tools are absent or error: **HALT**,
> one line — «⛔ markdown-vault-syv caído — no opero sobre el corpus hasta
> reconectarlo.» — then stop. Do not fall back to filesystem as the SSOT.

**Read & search** — first option, always
- `search` — hybrid/semantic/keyword search (`mode="hybrid"` preferred); the workhorse
- `read` — full content of a note (returns an `etag` for optimistic-concurrency writes)
- `list_documents` — enumerate notes (optionally by folder/pattern); `list_folders` — folders that hold docs
- `get_context` — assembled context around a note; `stats` — collection size/capabilities (also the preflight ping)
- `get_backlinks` · `get_outlinks` — inbound / outbound links of a note
- `get_broken_links` · `get_orphan_notes` — graph hygiene (verify hits before acting — table-cell `\|` pipes are false positives)
- `get_most_linked` · `get_similar` · `get_recent` · `get_connection_path` — graph navigation
- `get_history` · `get_diff` — change history and diffs of a note
- `fetch` — retrieve a document/attachment by reference

**Write & mutate** — index auto-updates after each; cascade-verify relations
- `write` — create or overwrite a note (whole-file; pass `frontmatter` + `content`)
- `edit` — surgical change; pass `if_match` with the `etag` from `read` to avoid clobbering
- `rename` — move/rename a note; `delete` — remove a note (IRREVERSIBLE unless git history)

**Index maintenance**
- `reindex` — rebuild the search index; `build_embeddings` / `embeddings_status` — semantic vectors

**Visual UI (do not use to retrieve content)** — `browse_vault`, `show_context` open a
user-facing UI; for content use `search`/`read`/`list_documents`/`get_context`.

## Frontmatter del corpus (quick view)

`markdown-vault-syv` is the **primary** SSOT and indexes frontmatter as exact-match
facets (only declared fields). The controlled dimensions live in **their own fields**
(`entidad` / `alcance` / `estado`, atom values — not inside `tags`); relations are
quoted wikilinks; `tags` is the open vivero (usually `[]`).

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

Authority: `../.claude/rules/` (one contract per file) + the corpus SSOT
`[[glosario-de-tags]]` and `[[guia-de-metadatos]]`.

## Obsidian MCP surface — `obsidian-syv` (SECONDARY, "método Obsidian")

Not the first option. Reserve `mcp__obsidian-syv__*` for what `markdown-vault-syv`
does not cover: the live Obsidian graph cascade, UI commands, and cross-checking
backlinks/wikilinks in the running app. Its horizon is the whole `~/SyV/` vault
(siblings `syv-pj`, `syv-pj-api`), so it is also the way to glance at sibling repos.

- **Read/UI**: `vault_read`, `vault_list`, `vault_get_document_map`, `search_simple`,
  `search_query` (JsonLogic), `tag_list`, `open_file`, `command_list`,
  `command_execute`, `active_file_get_path`, `periodic_note_get_path`
- **Write/mutate** (only if `markdown-vault-syv` write is unavailable): `vault_write`,
  `vault_append`, `vault_patch`, `vault_move`, `vault_delete`
