# syv-highlight-marks — engine

Backend for the `/syv-highlight-marks` command. Reads **any** `<mark>` span
(typically painted **live** in Obsidian with the Highlightr plugin, but not
limited to it) and turns them into a worklist; then applies the resolved
prose back to disk.

## The mark format (two protocols, combined)

```
<mark style="background: #RRGGBBAA;">TEXTO {nota de kodex}</mark>
<mark class="hltr-red">TEXTO {nota de kodex}</mark>
<mark>TEXTO {nota de kodex}</mark>
```

- **Color** (hex, alpha = last 2 digits ignored), when present → **severity /
  action** via nearest-palette classification. This applies uniformly to any
  hex, known or unknown — not a special case.
- **No resolvable hex** (bare `<mark>` or `class`-only) → defaults to
  **medium severity** (`yellow` / `refactor-moderate`).
- Optional **`{...}` brace** inside → the **specific instruction**, and it
  **always overrides** the color/default.
- A **closed** mark is pending work. An **unclosed** `<mark>` = kodex is still
  typing → never matched (the regex requires `</mark>`), so the loop never fights
  live typing.

Three intent axes + two loop-structural colours. The `{brace}` note always
overrides the colour.

| Axis | Color | Hex | Action (`action`) |
|---|---|---|---|
| fidelity | 🟡 yellow / **bare or class-only (default)** | `#FFF3A3` / no hex | `light-touch` — retoque muy suave, sentido intacto |
| fidelity | 🟠 orange | `#FFB86C` (or nearest) | `paraphrase` — decir lo mismo con otras palabras |
| fidelity | 🔴 red | `#FF5582` (or nearest) | `negate` — negar el contenido / rehacer el fragmento |
| lyric+ | 🟣 purple | `#BE9FFF` (or nearest) | `lyric-more` — mucha más lírica (cualquier registro) |
| lyric+ | 🩷 pink | `#FF99C8` (or nearest) | `tender` — más creativo en clave tierna: sensual/calmo/paz/amor, sin violencia |
| calm | 🔵 blue | `#5B8DEF` (or nearest) | `de-purple` — estabas cursi/rimbombante → tranquilizar |
| calm | 🩵 cyan | `#8FE3F0` (or nearest) | `introspective` — más tranquilo e introspectivo: quietud interior, algún placer |
| structural | ⚪ gray | `#CACFD9` (or nearest) | `flow` — flujo / typo (lo nombra el `{brace}`) |
| structural | 🟢 green | `#BBFABB` (or nearest) | `approve` — no tocar el texto, solo quitar la marca |

Color is classified by **nearest palette colour in RGB** (robust to alpha and to
6- or 8-digit hex, and to unknown/custom hex values — general behaviour, not an
exception), not by class name. The palette (`PALETTE`/`ACTION` in
`highlight.py`) is the overridable default table.

## CLI

```bash
# scan a folder recursively (or a single .md) → JSON worklist, sorted by severity
python3 highlight.py scan 4_diegesis/            # folder, recursive
python3 highlight.py scan path/to/file.md        # single file
python3 highlight.py scan .                       # whole corpus

# apply edits from stdin: [{file, old, new}] — literal in-place single replace
echo '[{"file":"4_diegesis/relatos/x.md","old":"<mark ...>..</mark>","new":"texto"}]' \
  | python3 highlight.py apply
```

`scan` worklist item: `file, color, action, severity, hex, line, span, inner,
prose, notes`. `span` is the exact bytes to replace; `prose` is `inner` minus the
`{notes}`.

## Why filesystem editing (the default backend)

Editing through the corpus MCP (`mcp__markdown-vault-syv__edit` + `if_match`)
**self-collides** during live writing: Obsidian Git auto-commits the `.md`, which
mutates the etag even when the mark wasn't touched → *"Concurrent modification"*.
So the proven path is: **literal span replace on disk** (this engine), then a
single `mcp__markdown-vault-syv__reindex` to reconcile the SSOT search index.

`apply` does `text.replace(old, new, 1)` — first occurrence only, UTF-8 safe — the
spirit of `sed -i` but literal (no regex-escaping hazards on prose). It reports
`ambiguous: true` if a span occurred more than once.

The **MCP write backend** exists too (selectable in the command) for study /
comparison — see the command doc. It does not need a reindex (the MCP updates the
index itself) but is exposed to the auto-commit etag race.

## Learning loop

After an in-scope prose write (`1_trasfondo/`, `4_diegesis/`, `5_aventuras/`),
record it so `/syv-kodex-style` can later compare mine-vs-kodex:

```bash
python3 ../syv-kodex-style/record_generation.py <file.md> --note "qué reescribí"
```

Authority on the protocol: `[[mark-color-protocol]]`. Feeds `[[kodex-style-canon]]`.
