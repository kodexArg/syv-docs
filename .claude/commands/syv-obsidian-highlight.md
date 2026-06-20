---
description: Loop en vivo que lee los <mark> de colores (plugin Highlightr de Obsidian) en un .md de prosa y refactoriza según el color (rojo→reescribir · naranja/amarillo→refactor · gris→flujo · verde→aprobar). Param: intervalo del loop.
argument-hint: "[intervalo] [archivo?] — ej. 1m · 2m · 90s (default 1m)"
model: opus
---

# /syv-obsidian-highlight — refactor por resaltado de Obsidian

Arma un **loop en vivo** que vigila las marcas de resaltado del plugin **Highlightr**
(`<mark style="background:#HEX">…</mark>`) en un archivo de prosa y **refactoriza el
texto según el color de cada marca**. Reemplaza al viejo sistema de llaves `{…}`.
Protocolo documentado en [[mark-color-protocol]]; alimenta el [[kodex-style-canon]].

> **Tier — leé esto.** Este comando **escribe prosa canónica**, no edita config.
> Corré en **modelo de frontera (Opus) al MÁXIMO esfuerzo** (`/effort` al tope; no
> uses tiers chicos ni delegues la reescritura a un worker débil). La calidad de la
> reescritura ES el producto.

## Paleta → acción (cómo interactuar con el highlight)

El color se detecta por los componentes **RGB del hex** (ignorá el alpha = 2 últimos
dígitos), no por nombre de clase.

| Color | Hex (Highlightr) | Severidad | Acción |
|---|---|---|---|
| 🔴 rojo | `#FF5582…` | rechazo total | reescritura **total** del fragmento (voz-canon); el original = ejemplo NO aceptado → destilar a [[kodex-style-canon]] «quita» |
| 🟠 naranja | `#FFB86C…` | alta | refactor fuerte |
| 🟡 amarillo | `#FFF3A3…` | media | refactor moderado |
| ⚪ gris | `#CACFD9…` | mínima — **flujo** | retoques de lectura/ritmo, sin tocar el fondo |
| 🟢 verde | `#BBFABB…` | aprobado / ejemplar | **no tocar el texto**: es estilo objetivo → destilar a [[kodex-style-canon]] «resultó»; sólo quitar la marca |

En **todos** los colores: tras actuar, **quitá la etiqueta `<mark>`** (marca = pendiente;
resuelta = sin marca). Marca **sin cerrar** = está tipeando → ignorala.

## Cómo se dispara

1. **Parseá `$ARGUMENTS`**: primer token = **intervalo del loop** (`1m`, `2m`, `90s`…;
   si está vacío, default `1m`). Token siguiente, si lo hay = **archivo objetivo**
   (default: el `.md` que se esté editando / el del último loop de esta sesión).
2. **Convertí el intervalo a cron**: `Nm` con N≤59 → `*/N * * * *`; `Ns` → redondeá a
   minutos (mínimo 1). Avisá si redondeaste.
3. **Preflight**: `mcp__markdown-vault-syv__stats`. Si las tools `mcp__markdown-vault-syv__*`
   faltan o dan error → **HALT**: «⛔ markdown-vault-syv caído — no opero sobre el corpus».
4. **`CronCreate`** recurrente con el *prompt por-ciclo* de abajo (reemplazá `<ARCHIVO>`).
5. **Primera pasada ya** (no esperes el primer tick). Reportá el `job id`; se corta con
   `CronDelete <id>`.

## Prompt por-ciclo (esto va en `CronCreate`, con `<ARCHIVO>` sustituido)

```
[LOOP de marcas de color — Highlightr] Estoy escribiendo en vivo en <ARCHIVO> (prosa canónica: realismo crudo/científico, formal y conciso, SIN fantasía gratuita; si es un hito/relato, regí por [[kodex-style-canon]]). Atendé SOLO <mark style="background:#HEX...">TEXTO</mark>. Sin afectar mi escritura libre:

1. Preflight: mcp__markdown-vault-syv__stats. Si falla, HALT: «⛔ markdown-vault-syv caído».
2. Leé el archivo COMPLETO con mcp__markdown-vault-syv__read (las lecturas por sección vienen rezagadas y no ven marcas recién escritas — usá read completo). Da etag fresco.
3. Encontrá <mark ...>...</mark> CERRADOS. Ignorá <mark> sin cierre (estoy tipeando).
4. Clasificá el color por RGB del hex (ignorá el alpha = 2 últimos dígitos): rojo = R alto, G/B bajos; naranja = R alto, G medio, B bajo; amarillo = R y G altos, B bajo; verde = G alto, R/B más bajos; gris = R≈G≈B (desaturado). Paleta: rojo #FF5582, naranja #FFB86C, amarillo #FFF3A3, verde #BBFABB; gris = hex neutro.
5. Acción (con mcp__markdown-vault-syv__edit, if_match=<etag>; reemplazá SOLO el span <mark>…</mark> completo; re-leé el etag entre edits si hay varias):
   - ROJO → rechazo total. Reescribí TOTALMENTE el fragmento (voz-canon, realista, formal, conciso) y reemplazá la marca por el texto nuevo SIN <mark>. Destilá el original rechazado a kodex-style-canon.md sección «✂️ quita» (memoria de archivo; fusioná, no dupliques). engram OPCIONAL, sólo si sus tools están cargadas.
   - NARANJA → refactor fuerte. AMARILLO → refactor moderado. GRIS → solo flujo (lectura/ritmo, sin tocar el fondo). En los tres: reemplazá por la versión nueva, sin <mark>.
   - VERDE → NO cambies el texto. Quitá SOLO las etiquetas <mark>/</mark>. Destilá ese pasaje aprobado a kodex-style-canon.md sección «✅ resultó». engram OPCIONAL.
6. Si una marca está a medio escribir o el etag colisiona: reintentás el próximo ciclo (no pises mi escritura).
7. Tras escribir prosa por la MCP: registrá la generación con _tools/syv-kodex-style/record_generation.py <ARCHIVO> --note "qué reescribí" (cierra el loop de aprendizaje; ver [[syv-kodex-style-process]]).
8. Si no hay marcas cerradas, NO-OP silencioso.

Reportá en una línea en español sólo si actuaste (qué color, qué fragmento, qué hiciste). Si no hubo marcas: «sin marcas».
```

## Notas
- **Memoria, no engram.** verde/rojo destilan a `kodex-style-canon.md` (memoria de archivo);
  engram queda opcional (sus tools no siempre están cargadas en sesión).
- **Concurrencia.** Edits quirúrgicos con `if_match`; ante colisión de etag, reintento al
  próximo ciclo — nunca pisar la escritura en vivo.
- **Ledger.** Registrá cada reescritura con `record_generation.py` para que `/syv-kodex-style`
  pueda comparar mío-vs-kodex después.

Argumento: $ARGUMENTS
