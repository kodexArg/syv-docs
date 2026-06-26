---
description: Dos relatos homónimos «el-caso-del-archivista» (notas vs canónico); el
  bloque de notas afirma que el canónico está vaciado, pero el canónico ya tiene prosa
  nueva.
folder: 0_proyecto/deuda-tecnica
related:
- '[[4_diegesis/relatos/el-caso-del-archivista|El Caso del Archivista (relato)]]'
- '[[4_diegesis/relatos/block_de_notas/el-caso-del-archivista|El Caso del Archivista
  (notas)]]'
- '[[0_proyecto/deuda-tecnica/deuda-tecnica|Deuda Técnica]]'
tags: []
title: DT-004 · El Caso del Archivista — basename duplicado y puntero stale
---

> [!info] Tarjeta de deuda técnica
> Tema: **El Caso del Archivista** — convivencia del relato canónico y su block de notas.

### `ABIERTO` · DT-004 — El basename «el-caso-del-archivista» está duplicado
#deuda/nombres #deuda/duplicado
**Afecta:** [[4_diegesis/relatos/el-caso-del-archivista|El Caso del Archivista (relato)]] · [[4_diegesis/relatos/block_de_notas/el-caso-del-archivista|El Caso del Archivista (notas)]]

```gherkin
# language: es
Escenario: Notas y relato canónico comparten basename
  Dado que existe 4_diegesis/relatos/el-caso-del-archivista.md (el relato canónico)
  Y que existe 4_diegesis/relatos/block_de_notas/el-caso-del-archivista.md (el block de notas)
  Y que ambos comparten el basename el-caso-del-archivista.md
  Cuando alguien escribe [[el-caso-del-archivista]] sin ruta
  Entonces el wikilink resuelve a uno de los dos de forma no determinista
  Y solo se evita porque hoy los enlaces existentes usan ruta completa
```

### `ABIERTO` · DT-004b — El block de notas dice que el canónico está «vaciado», pero ya tiene prosa
#deuda/incongruencia #deuda/prosa
**Afecta:** [[4_diegesis/relatos/block_de_notas/el-caso-del-archivista|El Caso del Archivista (notas)]] · [[4_diegesis/relatos/el-caso-del-archivista|El Caso del Archivista (relato)]]

```gherkin
# language: es
Escenario: El puntero al estado del relato canónico quedó desactualizado
  Dado que el block de notas afirma "El relato canónico vive en [[...]] (vaciado para reescribir)"
  Y que 4_diegesis/relatos/el-caso-del-archivista.md ya contiene una escena nueva (la llegada del Inquisidor Saturnino)
  Cuando un colaborador lee la nota de las notas para saber si el canónico está vacío
  Entonces se le informa un estado falso ("vaciado") que el archivo ya no tiene
```