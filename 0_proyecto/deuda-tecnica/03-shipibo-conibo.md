---
description: Dos notas homónimas «shipibo-conibo» clasifican a la misma entidad como
  credo y como facción, con alcance contradictorio y ambas en canon.
folder: 0_proyecto/deuda-tecnica
related:
- '[[1_trasfondo/credos/el-camino-del-kene|Shipibo-Conibo (credo)]]'
- '[[1_trasfondo/facciones/facciones-menores/shipibo-conibo|Shipibo-Conibo (facción)]]'
- '[[0_proyecto/deuda-tecnica/deuda-tecnica|Deuda Técnica]]'
tags: []
title: DT-003 · Shipibo-Conibo — ¿credo o facción? homónimo + alcance
---

> [!success] RESUELTO · 2026-06-26
> Credo renombrado a la religión **[[1_trasfondo/credos/el-camino-del-kene|El Camino del Kené]]**, enlazado en ambos sentidos con el pueblo (facción). Alcance reconciliado: la fe es pública, el pueblo y su secreto fúngico son secretos → **dos entidades, no una contradicción**. 3 enlaces colgantes (guaraní, umbanda, artefactos) reparados. Verificado. Traza abajo.

> [!info] Tarjeta de deuda técnica
> Tema: **Shipibo-Conibo**. Misma entidad, dos clasificaciones y dos alcances.

### `ABIERTO` · DT-003 — «shipibo-conibo» existe como credo y como facción a la vez
#deuda/nombres #deuda/incongruencia
**Afecta:** [[1_trasfondo/credos/el-camino-del-kene|Shipibo-Conibo (credo)]] · [[1_trasfondo/facciones/facciones-menores/shipibo-conibo|Shipibo-Conibo (facción)]]

```gherkin
# language: es
Escenario: La misma entidad tiene dos fichas homónimas con entidad distinta
  Dado que existe 1_trasfondo/credos/shipibo-conibo.md con entidad: credo, estado: canon
  Y que existe 1_trasfondo/facciones/facciones-menores/shipibo-conibo.md con entidad: faccion, estado: canon
  Y que ambas comparten el basename shipibo-conibo.md
  Cuando se enlaza [[shipibo-conibo]] sin ruta
  Entonces el grafo resuelve a una sola de las dos de forma no determinista
  Y el corpus no deja claro si Shipibo-Conibo es un credo, una facción, o ambas cosas como notas separadas
```

### `ABIERTO` · DT-003b — Las dos fichas declaran `alcance` contradictorio
#deuda/spoiler
**Afecta:** [[1_trasfondo/credos/el-camino-del-kene|Shipibo-Conibo (credo)]] · [[1_trasfondo/facciones/facciones-menores/shipibo-conibo|Shipibo-Conibo (facción)]]

```gherkin
# language: es
Escenario: Una versión es pública y la otra secreta
  Dado que la ficha de credo declara alcance: publico
  Y que la ficha de facción declara alcance: secreto
  Cuando se decide si Shipibo-Conibo puede exponerse en atlas o relatos
  Entonces el corpus da dos respuestas incompatibles para la misma entidad
```