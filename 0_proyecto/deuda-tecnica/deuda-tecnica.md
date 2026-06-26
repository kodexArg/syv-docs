---
description: 'Manual y registro vivo de deuda técnica del corpus SyV: cada incidencia
  con estado, tags, título, referencia y un escenario BDD/Gherkin.'
folder: 0_proyecto/deuda-tecnica
related:
- '[[0_proyecto/0_proyecto|Proyecto]]'
- '[[0_proyecto/guias-para-colaboradores/guia-de-metadatos|Guía de Metadatos]]'
tags: []
title: Deuda Técnica
---

**Manual + registro vivo** de la deuda técnica del corpus: errores, incongruencias y roturas que se descubren mientras el universo crece. Este archivo **no corrige, describe el problema**. Arriba está el manual (tags, estados, plantilla); abajo, el **tablero de escalado** y el **índice de tarjetas**. Cada incidencia vive en su propia tarjeta `NN-slug.md` dentro de esta carpeta; este archivo **no las repite: escala e indiza**.

## Tags

Etiquetá cada incidencia con uno o más. Son la categoría del *tipo* de deuda (el estado va aparte, abajo):

| Tag | Describe |
|---|---|
| `#deuda/fechas` | Fechas cruzadas o cronología inconsistente. |
| `#deuda/incongruencia` | Contradicción entre dos puntos del canon. |
| `#deuda/incompleto` | Sección, ficha o hito a medio desarrollar o pendiente. |
| `#deuda/nombres` | Colisión de nombres o basenames duplicados. |
| `#deuda/enlace-roto` | Wikilink que apunta a una nota o sección inexistente. |
| `#deuda/huerfano` | Nota sin enlaces entrantes ni salientes. |
| `#deuda/metadato` | Frontmatter mal formado o campo obligatorio ausente. |
| `#deuda/taxonomia` | Campo o valor fuera del glosario, o `tags` mal usado. |
| `#deuda/relacion` | Relación entre entidades que debería ser wikilink y no lo es. |
| `#deuda/spoiler` | Secreto expuesto, o `alcance`/`spoilers` mal marcado. |
| `#deuda/duplicado` | Contenido repetido que rompe el DRY. |
| `#deuda/estructura` | Archivo mal ubicado, vacío o sobrante. |
| `#deuda/prosa` | Inconsistencia de voz, estilo o continuidad narrativa. |

## Estados

| Estado | Significado |
|---|---|
| `ABIERTO` | Detectada, sin resolver. |
| `EN-REVISION` | En análisis o discusión. |
| `RESUELTO` | Corregida — se conserva la traza. |
| `DESCARTADO` | No era un error, o no se corrige. |

> [!info] Cómo se anota una incidencia
> Siempre en este orden:
> 1. **ESTADO** — lo primero y lo más importante.
> 2. **Título** — corto e inequívoco (con id `DT-NNN`).
> 3. **Tags** — uno o más de la tabla de arriba.
> 4. **Referencia de archivo** — al menos una, como `[[wikilink]]`.
> 5. **BDD** — un `Escenario` que **replica** el error (`Dado` / `Cuando` / `Entonces`) o lo **describe** de forma semántica.
>
> Acá **describimos el problema, no la solución**. Y **no se borra nada**: una incidencia cerrada pasa a `RESUELTO` o `DESCARTADO` y conserva su traza.

## Plantilla

Copiá este bloque por cada hallazgo:

````markdown
### `ABIERTO` · DT-NNN — <título corto e inequívoco>
#deuda/<categoria>
**Afecta:** [[ruta/al/archivo]]

```gherkin
# language: es
Escenario: <replica el error, o descríbelo semánticamente>
  Dado <la verdad canónica, o el lugar donde vive>
  Cuando <el disparador del conflicto>
  Entonces <la contradicción observable>
```
````

---

## Escalado

> [!success] Tablero limpio — sin escalados activos
> Las tres deudas escaladas (DT-002 autoría · DT-003 Shipibo-Conibo · DT-001 Anatema Mecánico) fueron resueltas, verificadas y cerradas. No queda ninguna incidencia en escalado.

## Índice de incidencias (tarjetas)

Cada incidencia abierta vive en su propia tarjeta `NN-slug.md` en esta carpeta. **Una vez resuelta y verificada, su tarjeta se elimina** —la traza completa (BDD incluido) queda en el historial de git—; este índice solo enumera lo que sigue abierto.

> [!success] Tanda cerrada y purgada — 2026-06-26
> **DT-001…DT-008: resueltas, verificadas y eliminadas.** Cada una se comprobó contra el corpus con un swarm read-only más chequeo MCP (`broken_link_count: 0`, sin huérfanos espurios) **antes** de borrar su tarjeta. La traza Gherkin de cada incidencia se conserva en el historial de git. Resumen de lo cerrado:
> - **DT-001** Anatema Mecánico (homónimo/alcance/metadato) → atlas renombrado «La Vida bajo el Anatema Mecánico»; codex con `estado: canon` y separación canónica doctrina (secreto) ↔ vida (público).
> - **DT-002** Autoría de El Cronologio → obra «Las Cronologías según los Archivistas»; Anselmo autor/fundador, Pedro continuador-compilador; ficha de Anselmo creada.
> - **DT-003** Shipibo-Conibo (credo vs facción) → credo «El Camino del Kené» + pueblo (facción) como dos entidades enlazadas; alcance reconciliado.
> - **DT-004** El Caso del Archivista (homónimo + puntero stale) → basename único `el-caso-del-archivista-notas`; puntero «vaciado» corregido.
> - **DT-005** `folder` ≠ ruta → corregido en las 7 notas de `block_de_notas`.
> - **DT-006** `related` malformado (Cecilia Torres) → lista YAML de wikilinks; mismo fix en el hito 2031.
> - **DT-007** Enlace roto «Confederación Argentina» → reparado; `broken_link_count: 0`.
> - **DT-008** Fantasma de índice `template-deuda-tecnica` → purgado; índice y disco reconciliados.

- `ABIERTO` · **DT-009** — [[0_proyecto/deuda-tecnica/09-seguridad-nacional-darsena-vs-dns|Seguridad Nacional Dársena vs DNS]] · `#deuda/incongruencia` `#deuda/incompleto`