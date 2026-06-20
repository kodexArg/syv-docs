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
| `queue_commit.py` | Worker del hook `post-commit`. Anota cada commit in-scope en `queue.jsonl`. Barato, sin LLM, nunca bloquea un commit. Es el disparador "en cada commit". |
| `record_generation.py` | Ledger. Claude lo llama tras escribir prosa in-scope: snapshot del blob que produjo → `generations.jsonl`. La autoridad de "esto es mío". |
| `pair.py` | Motor de emparejamiento. Lee ledger + historia git, arma pares `<mío → versión de kodex>` con diffs. Read-only salvo `--commit` (avanza el cursor). Fuente de verdad = git, no la cola: funciona aunque el hook no haya disparado. |
| `install_hook.py` | Instala el hook idempotente y siembra el cursor en HEAD. |
| `state.json` | Cursor: último `last_sha` procesado. (volátil, gitignored) |
| `queue.jsonl` / `generations.jsonl` | Logs volátiles (gitignored). |

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

# procesar lo pendiente (lo hace el comando /syv-kodex-style):
python3 _tools/syv-kodex-style/pair.py            # ver pares
python3 _tools/syv-kodex-style/pair.py --commit   # ver + avanzar cursor
```

Los tres aprendizajes: ✅ lo que resultó (aceptado al pie de la letra) · ✍️ lo que
kodex agregó (prioridad de estilo) · ✂️ lo que kodex quitó (dónde nos excedimos).
