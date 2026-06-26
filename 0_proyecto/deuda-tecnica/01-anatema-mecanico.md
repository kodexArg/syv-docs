---
description: El concepto «Anatema Mecánico» vive en dos notas homónimas con alcance
  contradictorio y un campo estado ausente.
folder: 0_proyecto/deuda-tecnica
related:
- '[[1_trasfondo/codex/anatema-mecanico|Anatema Mecánico (codex)]]'
- '[[2_atlas/tecnologia-y-ciencia/vida-bajo-el-anatema-mecanico|Anatema Mecánico (atlas)]]'
- '[[1_trasfondo/cronologia|Cronología]]'
- '[[0_proyecto/deuda-tecnica/deuda-tecnica|Deuda Técnica]]'
tags: []
title: DT-001 · Anatema Mecánico — homónimo, alcance y metadato
---

> [!info] Tarjeta de deuda técnica
> Tema: **Anatema Mecánico**. Una tarjeta, varias variantes del mismo tema en modo APPEND.

### `ABIERTO` · DT-001 — El basename «anatema-mecanico» está duplicado y se enlaza sin ruta
#deuda/nombres
**Afecta:** [[1_trasfondo/codex/anatema-mecanico|Anatema Mecánico (codex)]] · [[2_atlas/tecnologia-y-ciencia/vida-bajo-el-anatema-mecanico|Anatema Mecánico (atlas)]] · enlace ambiguo en [[1_trasfondo/cronologia|Cronología]]

```gherkin
# language: es
Escenario: Un wikilink sin ruta resuelve a una de dos notas homónimas
  Dado que existe 1_trasfondo/codex/anatema-mecanico.md
  Y que existe 2_atlas/tecnologia-y-ciencia/anatema-mecanico.md
  Y que la Cronología enlaza con [[anatema-mecanico]] sin ruta
  Cuando Obsidian resuelve ese wikilink
  Entonces apunta a una sola de las dos notas de forma no determinista
  Y el grafo puede conectar la entidad equivocada
```

### `ABIERTO` · DT-001b — Las dos notas homónimas declaran un `alcance` contradictorio
#deuda/incongruencia #deuda/spoiler
**Afecta:** [[1_trasfondo/codex/anatema-mecanico|Anatema Mecánico (codex)]] · [[2_atlas/tecnologia-y-ciencia/vida-bajo-el-anatema-mecanico|Anatema Mecánico (atlas)]]

```gherkin
# language: es
Escenario: El mismo concepto es secreto en un lado y público en el otro
  Dado que ambas notas describen el concepto Anatema Mecánico con entidad: concepto
  Y que el codex declara alcance: secreto
  Y que el atlas declara alcance: publico
  Cuando se decide si el concepto puede exponerse fuera de spoilers
  Entonces el corpus da dos respuestas incompatibles para la misma entidad
```

### `ABIERTO` · DT-001c — La nota del codex no declara el campo `estado`
#deuda/metadato
**Afecta:** [[1_trasfondo/codex/anatema-mecanico|Anatema Mecánico (codex)]]

```gherkin
# language: es
Escenario: Falta el campo de estado canónico en la ficha del codex
  Dado que 1_trasfondo/codex/anatema-mecanico.md tiene entidad: concepto
  Y que su frontmatter no incluye el campo estado
  Cuando se filtra el corpus por estado (canon · borrador · propuesta)
  Entonces esta nota queda fuera de toda faceta de estado
  Y su contraparte de atlas sí declara estado: canon
```