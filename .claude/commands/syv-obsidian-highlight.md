---
description: Loop en vivo que barre una CARPETA (recursiva) buscando los <mark> de colores de Highlightr y refactoriza la prosa según el color (rojo→reescribir · naranja/amarillo→refactor · gris→flujo · verde→aprobar). Edita por filesystem (default) o por MCP. Params: intervalo · carpeta/archivo · backend.
argument-hint: "[intervalo] [carpeta|archivo|.] [--via fs|mcp] — ej. 5m . · 5m 4_diegesis · 2m relato.md --via mcp"
model: opus
---

# /syv-obsidian-highlight — refactor por resaltado de Obsidian (carpeta-recursivo)

Arma un **loop en vivo** que vigila las marcas de resaltado del plugin **Highlightr**
(`<mark style="background:#HEX">…</mark>`) en **toda una carpeta de forma recursiva**
(no un solo archivo) y **refactoriza la prosa según el color de cada marca**. Reemplaza
al viejo sistema de llaves `{…}` como *contenedor*; pero el `{…}` sigue vivo **dentro**
de la marca como **nota puntual** de kodex. Protocolo: [[mark-color-protocol]]; alimenta
el [[kodex-style-canon]].

> **Tier — leé esto.** Este comando **escribe prosa canónica**, no edita config.
> Corré en **modelo de frontera (Opus) al MÁXIMO esfuerzo**. La calidad de la
> reescritura ES el producto. El loop-turn ES el prosista de la casa (mismo estándar
> que `syv-narrativa-prosa`, cargá `[[kodex-style-canon]]`).

## Arquitectura — por qué el loop-turn hace la prosa (y no el writer agent)

El usuario pidió «usar el orquestador o el writer especializado, lo que mejor calce».
**Calce real:** `syv-narrativa-prosa` es **MCP-write-only** (no tiene Bash/Edit) → **no
puede editar por filesystem**, que es la regla dura para escritura en vivo (ver backend
`fs`). Y el orquestador *despacha*, no *redacta*. Por eso el **turno por-ciclo del loop**
(Opus, máximo esfuerzo) **encarna al prosista**: clasifica, redacta con voz-canon y
aplica por el backend elegido. El motor determinista vive en
`_tools/syv-obsidian-highlight/highlight.py` (scan + apply).

## La marca: color (severidad) + `{nota}` (instrucción)

```
<mark style="background: #RRGGBBAA;">TEXTO {nota puntual de kodex}</mark>
```

El color se detecta por **RGB del hex** (ignorá el alpha = 2 últimos dígitos), por
cercanía a la paleta. La `{nota}` interna, si existe, es la **instrucción concreta**.

| Color | Hex | Severidad | Acción |
|---|---|---|---|
| 🔴 rojo | `#FF5582` | rechazo total | reescritura **total** / **suplir lo que falta** (voz-canon); destilar el original a [[kodex-style-canon]] «quita» |
| 🟠 naranja | `#FFB86C` | alta | refactor fuerte |
| 🟡 amarillo | `#FFF3A3` | media | refactor moderado |
| ⚪ gris | `#CACFD9` | mínima — **flujo** | typo / ritmo (la `{nota}` suele nombrarlo); sin tocar el fondo |
| 🟢 verde | `#BBFABB` | aprobado | **no tocar el texto** → destilar a [[kodex-style-canon]] «resultó»; solo quitar la marca |

En **todos**: tras actuar, **quitá la marca `<mark>` y la `{nota}`** (resuelto = sin
marca ni nota). Marca **sin cerrar** = está tipeando → el motor la ignora sola.

## Dos backends de escritura (elegís cuál estudiar)

| `--via` | Cómo escribe | Trade-off |
|---|---|---|
| **`fs`** *(default)* | `highlight.py apply` → `text.replace(old,new,1)` en disco; después **un** `mcp__markdown-vault-syv__reindex` reconcilia el índice | **A prueba de colisión.** El edit por MCP **se auto-colisiona** en vivo: Obsidian Git auto-commitea el `.md` y muta el etag aunque la marca no se haya tocado → *«Concurrent modification»*. Por eso es el camino probado. |
| **`mcp`** *(estudio)* | `mcp__markdown-vault-syv__edit` con `if_match=<etag de read>`, reemplazando SOLO el span | El índice se actualiza solo (sin reindex), pero queda **expuesto a la carrera del auto-commit**: ante colisión de etag, reintentar al próximo ciclo. Útil para comparar. |

## Cómo se dispara

1. **Parseá `$ARGUMENTS`**: token-1 = **intervalo** (`5m`, `2m`, `90s`…; default **`5m`**).
   token-2 = **carpeta o archivo o `.`** (default **`.`** = corpus entero, recursivo).
   flag **`--via fs|mcp`** = backend (default **`fs`**). «the whole base path recursively»
   ⇒ `.`.
   **Auto-stop (default):** el loop **se apaga solo tras 2 pasadas seguidas sin
   cambios** (estado en `/tmp/syv-highlight-loop.state`). Con los defaults, eso es
   **cada 5 min; 2 vueltas vacías lo dejan afuera.**
2. **Convertí el intervalo a cron**: `Nm` con N≤59 → `*/N * * * *`; `Ns` → redondeá a
   minutos (mínimo 1), avisá si redondeaste. **5m → `*/5 * * * *`.**
3. **Preflight**: `mcp__markdown-vault-syv__stats`. Si las tools `mcp__markdown-vault-syv__*`
   faltan o dan error → **HALT**: «⛔ markdown-vault-syv caído — no opero sobre el corpus».
   (El backend `fs` igual necesita la MCP para el `reindex` final.)
4. **`CronCreate`** recurrente con el *prompt por-ciclo* de abajo (sustituí `<CARPETA>` y `<VIA>`).
5. **Inicializá el contador** (`printf '0' > /tmp/syv-highlight-loop.state`) y corré la
   **primera pasada ya** (no esperes el primer tick). Reportá el `job id`; se corta solo
   a las **2 pasadas sin cambio**, o a mano con `CronDelete <id>`.

## Prompt por-ciclo (esto va en `CronCreate`, con `<CARPETA>` y `<VIA>` sustituidos)

```
[LOOP marcas Highlightr — barrido recursivo de <CARPETA>, backend <VIA>] kodex escribe prosa canónica EN VIVO (realismo crudo/científico, formal y conciso, SIN fantasía gratuita; regí por [[kodex-style-canon]] — leelo antes de redactar). Atendé SOLO <mark ...>TEXTO {nota?}</mark> CERRADAS. Sin pisar su escritura libre:

AUTO-STOP (default "2 paradas sin cambio"): el estado vive en /tmp/syv-highlight-loop.state (entero). Si esta pasada NO aplica ningún cambio → contador++ (si no existe, "1"); si llega a >=2 → DETENÉ el loop: CronList → job cuyo prompt contiene "barrido recursivo de <CARPETA>" → CronDelete ese id; reportá «⏹ loop detenido: 2 pasadas seguidas sin cambios». Si SÍ aplicás algún cambio → reseteá el contador a "0".

1. Preflight: mcp__markdown-vault-syv__stats. Si falla, HALT: «⛔ markdown-vault-syv caído» (no toques el contador).
2. Worklist: `python3 _tools/syv-obsidian-highlight/highlight.py scan <CARPETA>` → JSON de spans (file, color, action, severity, line, span, inner, prose, notes), ya ordenado por severidad. Las marcas sin cerrar NO aparecen (kodex tipeando). Si está vacío → pasada SIN cambio: aplicá AUTO-STOP (contador++) y fin.
3. Por cada span, redactá el texto nuevo (Opus, voz-canon) según color + `{nota}`:
   - ROJO → reescritura total / suplí lo que falte. Destilá el original a kodex-style-canon.md «✂️ quita» (fusioná, no dupliques).
   - NARANJA → refactor fuerte. AMARILLO → moderado. GRIS → solo flujo/typo (lo que diga la nota), sin tocar el fondo.
   - VERDE → NO cambies el texto; el nuevo = el TEXTO sin la marca. Destilá a kodex-style-canon.md «✅ resultó».
   En TODOS: el texto nuevo va SIN `<mark>` y SIN `{nota}`. Si el `{…}` es corrección factual/geográfica, OBEDECELA (canon vivo).
4. Aplicá según <VIA>:
   - fs  → armá [{file, old:<span exacto, incluido cualquier \n interno>, new:<texto>}] y pasalo por stdin a `python3 _tools/syv-obsidian-highlight/highlight.py apply`. Si algún item necesita absorber puntuación/espacios/saltos vecinos (p.ej. cortar una oración entera o cerrar un párrafo con línea en blanco), ampliá `old`/`new` con esos bytes vecinos. Tras aplicar ≥1: UN `mcp__markdown-vault-syv__reindex` (reconcilia el índice; los edits de disco no lo actualizan solos) y reseteá /tmp/syv-highlight-loop.state a "0".
   - mcp → por cada span: mcp__markdown-vault-syv__read del archivo (etag fresco) → mcp__markdown-vault-syv__edit con if_match=<etag>, old_text=<span exacto>, new_text=<texto>. Re-leé el etag entre edits del mismo archivo. Ante colisión de etag → reintentás el próximo ciclo (no pises la escritura en vivo). NO reindexes (el MCP ya actualiza el índice). Reseteá el contador a "0" si aplicaste ≥1.
5. Tras escribir prosa in-scope (1_/4_/5_): `python3 _tools/syv-kodex-style/record_generation.py <ARCHIVOS> --note "qué reescribí"` (cierra el loop de aprendizaje; ver [[syv-kodex-style-process]]).
6. Si una marca está a medio escribir o un edit colisiona: reintentás el próximo ciclo, nunca pisás la escritura en vivo (si no aplicaste nada más, cuenta como pasada sin cambio).

Reportá en una línea en español: si actuaste → cuántas marcas, qué colores, qué archivos, backend; si no hubo marcas → «sin marcas (N/2)»; si detuviste el loop → el mensaje de AUTO-STOP.
```

## Notas

- **Filesystem por defecto, MCP para estudio.** El default `fs` es a prueba de colisión;
  `mcp` queda expuesto al auto-commit de Obsidian Git — útil para comparar comportamientos.
- **Reindex solo en `fs`.** Los edits de disco no tocan el índice de la MCP; un `reindex`
  por ciclo lo reconcilia (ver `[[mcp-broken-links-lazy]]`).
- **Memoria, no engram.** verde/rojo destilan a `kodex-style-canon.md`; engram opcional.
- **Reversible.** Todo queda en git (Obsidian Git + commits) — kodex puede revertir cualquier
  reescritura.
- **Auto-stop «2 paradas sin cambio» (default).** El loop lleva un contador en
  `/tmp/syv-highlight-loop.state`: cada pasada que NO aplica cambios lo incrementa, cada
  pasada con cambios lo resetea a `0`; al llegar a `2` el propio ciclo hace `CronDelete` de
  su job y reporta «⏹ loop detenido». Evita que el loop quede girando en vacío cuando kodex
  terminó de marcar. (Es session-only: si se cierra Claude, el cron muere igual.)
- **Motor:** `_tools/syv-obsidian-highlight/highlight.py` (+ `README.md`). Python 3.13, stdlib.

Argumento: $ARGUMENTS
