---
description: 'Notas alojadas en .../relatos/block_de_notas/ declaran en frontmatter
  folder: 4_diegesis/relatos, ocultando que viven en el subdirectorio de notas.'
folder: 0_proyecto/deuda-tecnica
related:
- '[[4_diegesis/relatos/block_de_notas/el-fuego-que-cayo-sobre-el-norte|El Fuego que
  Cayó sobre el Norte]]'
- '[[4_diegesis/relatos/block_de_notas/el-caso-del-archivista|El Caso del Archivista
  (notas)]]'
- '[[0_proyecto/deuda-tecnica/deuda-tecnica|Deuda Técnica]]'
tags: []
title: DT-005 · El campo `folder` no coincide con la ruta real (block_de_notas)
---

> [!info] Tarjeta de deuda técnica
> Tema: **`folder` declarado ≠ ruta real** en el subdirectorio `block_de_notas`.

### `ABIERTO` · DT-005 — «El Fuego que Cayó sobre el Norte» declara un folder que no es el suyo
#deuda/metadato #deuda/estructura
**Afecta:** [[4_diegesis/relatos/block_de_notas/el-fuego-que-cayo-sobre-el-norte|El Fuego que Cayó sobre el Norte]]

```gherkin
# language: es
Escenario: El frontmatter folder no refleja el subdirectorio real
  Dado que el archivo vive en 4_diegesis/relatos/block_de_notas/el-fuego-que-cayo-sobre-el-norte.md
  Y que su frontmatter declara folder: 4_diegesis/relatos
  Cuando un proceso confía en el campo folder para ubicar la nota
  Entonces cree que está en relatos y no en block_de_notas
  Y se pierde la señal de que es material de cantera, no relato publicable
```

### `ABIERTO` · DT-005b — «El Caso del Archivista (notas)» repite el mismo desajuste de folder
#deuda/metadato #deuda/estructura
**Afecta:** [[4_diegesis/relatos/block_de_notas/el-caso-del-archivista|El Caso del Archivista (notas)]]

```gherkin
# language: es
Escenario: Otra nota de block_de_notas declara folder de relatos
  Dado que el archivo vive en 4_diegesis/relatos/block_de_notas/el-caso-del-archivista.md
  Y que su frontmatter declara folder: 4_diegesis/relatos
  Cuando se audita la coherencia entre ruta y campo folder
  Entonces el subdirectorio block_de_notas queda invisible en el metadato
```