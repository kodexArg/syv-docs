---
description: Completa todas las llaves {…} pendientes en 1_trasfondo/hitos/ (best effort, voz del Archivista) y reemplaza en todos los archivos.
---

# /goal — completar las llaves `{…}` de los hitos

Hacé tu **mejor esfuerzo** para **completar y reemplazar todo el texto entre llaves `{…}`** en los archivos de `1_trasfondo/hitos/`, iterando **todos** los archivos.

## Procedimiento

1. **Inventario primero (grep).** Corré:
   `grep -rnE '[{}]' 1_trasfondo/hitos/`
   Cada bloque `{…}` puede:
   - ser una **instrucción** («escribí acá algo que…»), o
   - envolver **texto existente** seguido de una segunda llave con la **corrección**: `{texto…} {cómo mejorarlo}`.
   Las llaves pueden **abarcar varios párrafos** (abren en una línea y cierran líneas después).

2. **Completá cada bloque** siguiendo su instrucción embebida, en la voz del Hermano Archivista (Pedro de los Santos, o Anselmo Quiroga según el capítulo), respetando el canon y el contexto inmediato (que enganche con lo de antes y lo de después).

3. **Reglas de estilo (CRÍTICAS — el usuario corrige seguido sobre esto):**
   - **Cruda realidad y realismo científico.** NO agregues fantasía gratuita, metáforas recargadas ni floritura. Fáctico, sobrio, formal.
   - Registro formal de crónica; rioplatense sin voseo pesado.
   - **Conciso:** si un bloque «es largo y aburrido», **acortalo**; no lo agrandes salvo que la instrucción lo pida explícitamente.
   - Respetá fechas y hechos del canon; no inventes entidades nuevas sin necesidad.

4. **Reemplazá en el archivo** (quitando las llaves y la instrucción). Los hitos se editan en vivo (usuario + linter + Obsidian Git): **releé el disco justo antes de editar** y aplicá por rango de líneas o match exacto. La MCP `markdown-vault-syv` puede estar desincronizada → `reindex` antes de leer.

5. **Reportá** qué bloques completaste, en qué archivos, con el texto resultante de cada uno, para visto bueno.

Empezá siempre por el grep.
