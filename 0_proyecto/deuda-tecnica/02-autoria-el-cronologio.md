---
description: El corpus afirma a la vez que El Cronologio lo escribió Pedro de los
  Santos y que lo escribió Anselmo Quiroga (con Pedro como copista). Contradicción
  canónica de raíz.
folder: 0_proyecto/deuda-tecnica
related:
- '[[1_trasfondo/codex/las-cronologias|El Cronologio]]'
- '[[3_personajes/principales/pedro-de-los-santos|Pedro de los Santos]]'
- '[[1_trasfondo/cronologia|Cronología]]'
- '[[1_trasfondo/hitos/2029-las-profecias-del-mercado|Profecías del Mercado (2029)]]'
- '[[0_proyecto/deuda-tecnica/deuda-tecnica|Deuda Técnica]]'
tags: []
title: DT-002 · Autoría de El Cronologio — Anselmo vs Pedro (inversión)
---

> [!success] RESUELTO · 2026-06-26
> La obra es ahora **Las Cronologías según los Archivistas** (`El Cronologio` queda como alias legado, el nombre que le dio Anselmo). Ficha nueva [[3_personajes/principales/anselmo-quiroga|Anselmo Quiroga]] (fundador savant, †en su centenario); [[3_personajes/principales/pedro-de-los-santos|Pedro]] = continuador/compilador. Dispositivo *diálogo de epígrafes y márgenes* explícito + margen nuevo de Pedro en el hito 2029. Fechas coherentes (cuerpo 2173 / glosas 2177-78). Verificado. Traza abajo.

> [!danger] Escalado — contradicción canónica de raíz
> ¿Quién escribió *El Cronologio*? El corpus sostiene **dos respuestas mutuamente excluyentes, ambas en `estado: canon`**. Afecta a la voz narradora de todo `1_trasfondo` (epígrafes de los hitos), a la ficha de personaje principal y al codex. Es la deuda de mayor alcance del relevamiento.

### `ABIERTO` · DT-002 — Pedro es «autor de El Cronologio» y a la vez su mero copista
#deuda/incongruencia
**Afecta:** [[1_trasfondo/codex/las-cronologias|El Cronologio]] · [[3_personajes/principales/pedro-de-los-santos|Pedro de los Santos]] · [[1_trasfondo/hitos/2029-las-profecias-del-mercado|Profecías del Mercado (2029)]]

```gherkin
# language: es
Escenario: La autoría de El Cronologio se afirma en dos sentidos opuestos
  Dado que el-cronologio.md está narrado en primera persona ("asentado de mi puño") y su descripción lo atribuye al Hermano Pedro de los Santos
  Y que pedro-de-los-santos.md describe a Pedro como "autor de El Cronologio" y a Anselmo Quiroga como mero "predecesor, voz de los epígrafes más antiguos"
  Y que el colofón de 2029-las-profecias-del-mercado.md dice "Edición y copia de mi puño de esta entrada del Cronologio del Hermano Archivista Anselmo Quiroga. —Hermano Archivista Pedro de los Santos"
  Cuando se pregunta quién es el autor del Cronologio
  Entonces el codex y la ficha responden "Pedro (autor)"
  Y el hito responde "Anselmo (autor), Pedro (copista)"
  Y ambas respuestas conviven marcadas como canon
```

### `ABIERTO` · DT-002b — La atribución del epígrafe varía hito a hito, con fechas incompatibles
#deuda/incongruencia #deuda/fechas
**Afecta:** [[1_trasfondo/hitos/2029-las-profecias-del-mercado|Profecías del Mercado (2029)]] · [[3_personajes/principales/pedro-de-los-santos|Pedro de los Santos]]

```gherkin
# language: es
Escenario: Distintos hitos firman su epígrafe con distinto archivista y distinto año
  Dado que el hito 2029 abre con un epígrafe firmado "—Hermano Archivista Anselmo Quiroga. A 13 días de diciembre del año 2173"
  Y que ese mismo hito cierra con un colofón firmado "—Hermano Archivista Pedro de los Santos" fechado en 2177
  Y que la ficha de Pedro fija que "escribe desde 2177-2178" y le adjudica el epígrafe de 2061
  Cuando se traza la línea de quién escribe qué epígrafe y cuándo
  Entonces no hay regla consistente: la voz salta entre Anselmo (2173) y Pedro (2177-2178) sin criterio declarado
```

### `ABIERTO` · DT-002c — El apellido «Quiroga» está reutilizado en dos personajes sin relación
#deuda/nombres
**Afecta:** [[3_personajes/principales/pedro-de-los-santos|Pedro de los Santos]] (menciona a Anselmo Quiroga) · [[4_diegesis/relatos/block_de_notas/el-caso-del-archivista-notas|El Caso del Archivista (notas)]]

```gherkin
# language: es
Escenario: Dos personajes distintos comparten apellido sin vínculo declarado
  Dado que el cronista del trasfondo se llama Hermano Archivista Anselmo Quiroga
  Y que la backstory de Damián en el block de notas menciona al "Teniente Coronel Quiroga" de Córdoba
  Cuando un lector cruza ambos nombres
  Entonces el apellido compartido sugiere un parentesco o vínculo que el canon no afirma
  Y conviene declarar la relación o desambiguar uno de los dos
```