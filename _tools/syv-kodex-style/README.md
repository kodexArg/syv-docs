# syv-kodex-style

Aprende del **lápiz rojo de kodex**: compara la prosa narrativa que generó Claude
contra cómo kodex la modificó, y destila reglas de estilo. Alcance:
`1_trasfondo/`, `4_diegesis/`, `5_aventuras/`.

## Por qué hace falta un ledger

En este repo, tanto las escrituras de Claude por la MCP como las ediciones a mano
de kodex en Obsidian commitean como `markdown-vault-mcp <noreply@markdown-vault-mcp>`.
Son **indistinguibles por autor o mensaje**. Por eso "esto lo escribí yo (Claude)"
se sabe sólo por dos señales:

1. El **ledger** `generations.jsonl`, escrito por `record_generation.py`.
2. El trailer `Co-Authored-By: Claude` en los commits de Bash de Claude.

Todo lo demás que toque esos archivos se asume modificación de kodex.

## Piezas

| Archivo | Rol |
|---|---|
| `on_push.py` | Worker del hook `pre-push`. **El disparador es el _push_, no el commit** (el push consolida una sesión de auto-commits de Obsidian — mejor límite para aprender). Anota el tip pusheado en `pushes.jsonl` y **avisa por stderr**; NO corre el análisis. Nunca bloquea un push. |
| `record_generation.py` | Ledger. Claude lo llama tras escribir prosa in-scope: snapshot del blob que produjo → `generations.jsonl`. La autoridad de "esto es mío". |
| `pair.py` | Motor de emparejamiento. Lee ledger + historia git, arma pares `<mío → versión de kodex>` con diffs. Read-only salvo `--commit` (avanza el cursor). Fuente de verdad = git + cursor: funciona aunque el hook no haya disparado. |
| `install_hook.py` | Instala el hook `pre-push` idempotente, limpia el viejo `post-commit`, y siembra el cursor en HEAD. |
| `state.json` | Cursor: último `last_sha` procesado. (volátil, gitignored) |
| `pushes.jsonl` / `generations.jsonl` | Logs volátiles (gitignored). |

## Flujo

1. Trabajás; Obsidian auto-commitea. Claude escribe prosa y registra con `record_generation.py`.
2. **Hacés `git push`** → el hook `pre-push` avisa: «✍️ corré /syv-kodex-style».
3. Corrés el skill **a mano** → procesa todo lo pusheado desde la última vez, destila los 3 aprendizajes a memoria + engram, avanza el cursor.

El hook no lanza el skill solo (sería automático, no "a mano", y un hook no puede inyectar en la sesión interactiva): te recuerda, vos disparás.

El razonamiento (clasificar el diff en los tres aprendizajes y guardarlos en
memoria + engram) lo hace el comando `/syv-kodex-style`, no estos scripts.

## Instalación

```bash
python3 _tools/syv-kodex-style/install_hook.py
```

## Uso

```bash
# tras escribir prosa por la MCP (para que el proceso sepa que fue mío):
python3 _tools/syv-kodex-style/record_generation.py 1_trasfondo/hitos/2029-...md --note "rellené llaves"

# tras un push, procesar lo pendiente (lo hace el comando /syv-kodex-style):
python3 _tools/syv-kodex-style/pair.py            # ver pares
python3 _tools/syv-kodex-style/pair.py --commit   # ver + avanzar cursor
```

Los tres aprendizajes: ✅ lo que resultó (aceptado al pie de la letra) · ✍️ lo que
kodex agregó (prioridad de estilo) · ✂️ lo que kodex quitó (dónde nos excedimos).
