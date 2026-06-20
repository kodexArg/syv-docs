---
description: Aprende del estilo de kodex comparando mi prosa generada vs cómo él la modificó (1_/4_/5_), y vuelca 3 aprendizajes a memoria + engram.
---

# /syv-kodex-style — aprender del lápiz rojo de kodex

Proceso de aprendizaje de estilo. **Se dispara a mano tras un push**: el hook
`pre-push` detecta el push de prosa narrativa (`1_trasfondo/`, `4_diegesis/`,
`5_aventuras/`) y avisa; entonces kodex corre este comando. Toma cada par
`<texto que generé yo>` → `<cómo lo modificó kodex>` desde la última corrida, lo
evalúa, y destila tres aprendizajes que guarda en **mi memoria del proyecto** y
en **engram**.

> **Autoría — leé esto.** En este repo, tanto mis escrituras por la MCP como las
> ediciones a mano de kodex en Obsidian commitean como `markdown-vault-mcp`. Son
> indistinguibles por autor. Por eso "lo mío" se sabe SOLO por el ledger
> (`record_generation.py`) o por el trailer `Co-Authored-By: Claude` en mis
> commits de Bash. Si un archivo no tiene base atribuible, `pair.py` lo **saltea**:
> nunca inventamos un aprendizaje sobre texto que no probamos que era nuestro.

## Pasos

1. **Obtené los pares pendientes** (read-only, no mueve el cursor todavía):

   ```bash
   python3 _tools/syv-kodex-style/pair.py
   ```

   Devuelve JSON `{head, from, pairs:[{file, source, mine_sha, theirs_sha, diff, my_additions}]}`.
   - `diff` = mi versión → la versión de kodex (su modificación).
   - `my_additions` = lo que yo introduje cuando generé (para ver qué de lo mío sobrevivió).
   - Si `pairs` está vacío → no hay nada nuevo, terminá acá.

2. **Evaluá cada par.** Para cada `diff`, clasificá los cambios de kodex en los
   **tres aprendizajes** (esta es la tarea de juicio, no mecánica):

   - ✅ **Lo que resultó** — adiciones mías que kodex aceptó al pie de la letra
     (líneas de `my_additions` que siguen intactas en su versión). *Qué patrón
     mío funciona y conviene repetir.*
   - ✍️ **Lo que kodex agregó / reescribió** — líneas `+` que son suyas. Es
     **voz de kodex y tiene prioridad de estilo**. *Qué giro, registro, palabra
     o ritmo introduce él que yo no había puesto.*
   - ✂️ **Lo que kodex quitó** — líneas `-` que eran mías y él borró. *En qué nos
     excedimos: floritura, redundancia, fantasía gratuita, sobreexplicación.*

   Pensá en términos de **regla de estilo reutilizable**, no de la frase puntual.
   Ignorá ruido no-estilístico (fixes de frontmatter, wikilinks, typos). Si un
   cambio no enseña nada de estilo, descartalo.

3. **Volcá los aprendizajes.**

   - **Memoria del proyecto** — refiná el canon de estilo en
     `/home/kodex/.claude/projects/-home-kodex-Dev-SyV-syv-docs/memory/kodex-style-canon.md`
     (tipo `feedback`). Agregá/afiná reglas bajo las tres secciones; no dupliques
     una regla ya presente, fusionala. Mantené el puntero en `MEMORY.md`.
   - **engram** — `mem_save` una observación por aprendizaje distinto y de peso
     (no por cada diff trivial), con el archivo y el `theirs_sha` como evidencia.

4. **Avanzá el cursor** sólo una vez guardado todo:

   ```bash
   python3 _tools/syv-kodex-style/pair.py --commit
   ```

5. **Reportá en español rioplatense**: qué aprendiste esta corrida (3 bullets:
   resultó / agregó / quitó) y cuántos pares procesaste. Conciso.

## Notas
- Alcance fijo: `1_trasfondo/`, `4_diegesis/`, `5_aventuras/`.
- Para que cubra mis generaciones por MCP, registralas con
  `python3 _tools/syv-kodex-style/record_generation.py <archivo.md> --note "qué escribí"`
  inmediatamente después de escribir. Mis commits de Bash ya se autodetectan por
  el trailer Claude.
- Disparo previsto: **a mano, tras ver el aviso del hook `pre-push`**. El hook
  sólo notifica (no lanza el skill solo). Instalación: `python3 _tools/syv-kodex-style/install_hook.py`.
