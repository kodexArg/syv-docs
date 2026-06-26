---
description: 'El índice de la MCP lista template-deuda-tecnica.md como nota huérfana,
  pero el archivo no existe en disco: desync índice/disco.'
folder: 0_proyecto/deuda-tecnica
related:
- '[[0_proyecto/deuda-tecnica/deuda-tecnica|Deuda Técnica]]'
tags: []
title: DT-008 · Fantasma de índice — template-deuda-tecnica.md
---

> [!info] Tarjeta de deuda técnica
> Tema: **desync índice ↔ disco** (tooling, no contenido del corpus).

### `ABIERTO` · DT-008 — El índice cree que existe un template que no está en disco
#deuda/estructura
**Afecta:** [[0_proyecto/deuda-tecnica/deuda-tecnica|Deuda Técnica]] (carpeta `0_proyecto/deuda-tecnica/`)

```gherkin
# language: es
Escenario: Una nota huérfana del índice no tiene archivo en disco
  Dado que get_orphan_notes lista 0_proyecto/deuda-tecnica/template-deuda-tecnica.md con frontmatter vacío
  Y que un read de esa ruta responde "Document not found"
  Y que el listado de la carpeta en disco solo muestra deuda-tecnica.md
  Cuando se confía en el índice para enumerar las tarjetas existentes
  Entonces aparece un archivo fantasma que ya no existe
  Y conviene un reindex para reconciliar índice y disco
```