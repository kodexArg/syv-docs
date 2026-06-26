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

> [!danger] Lo que hay que mirar primero
> Lo más grave del relevamiento, en orden de prioridad:
> 1. **[[0_proyecto/deuda-tecnica/02-autoria-el-cronologio|DT-002 — Autoría de El Cronologio (Anselmo vs Pedro)]]** · `#deuda/incongruencia` — contradicción de raíz: el corpus afirma a la vez que el autor es Pedro y que es Anselmo (con Pedro como copista), **ambas en `estado: canon`**. Toca la voz narradora de todo `1_trasfondo`.
> 2. **[[0_proyecto/deuda-tecnica/03-shipibo-conibo|DT-003 — Shipibo-Conibo: ¿credo o facción?]]** · `#deuda/incongruencia` — la misma entidad clasificada de dos formas, con alcance público/secreto en conflicto.
> 3. **[[0_proyecto/deuda-tecnica/01-anatema-mecanico|DT-001 — Anatema Mecánico homónimo]]** · `#deuda/incongruencia` — concepto duplicado con alcance contradictorio y metadato incompleto.

## Índice de incidencias (tarjetas)

Cada finding vive en su propia tarjeta `NN-slug.md` en esta carpeta. Acá va el índice; el detalle (BDD incluido) está en cada archivo. Variantes del mismo tema (DT-NNNb, DT-NNNc) se agregan en modo APPEND dentro de su tarjeta.

> [!success] Tanda resuelta — 2026-06-26
> **8 de 9 cerradas** (DT-001…DT-008); **DT-009 queda `ABIERTO`** por pedido (pendiente). Resueltas vía MCP `markdown-vault-syv`, marcadas con `<mark>` (azul = nuevo · naranja = refactor) y **verificadas adversarialmente** (10 críticos). Integridad final: `broken_link_count: 0`, sin huérfanos espurios. La traza Gherkin se conserva en cada tarjeta.

- `RESUELTO` · **DT-001** — [[0_proyecto/deuda-tecnica/01-anatema-mecanico|Anatema Mecánico — homónimo, alcance y metadato]] · `#deuda/nombres` `#deuda/incongruencia` `#deuda/spoiler` `#deuda/metadato`
- `RESUELTO` · **DT-002** — [[0_proyecto/deuda-tecnica/02-autoria-el-cronologio|Autoría de El Cronologio — Anselmo vs Pedro]] · `#deuda/incongruencia` `#deuda/fechas` `#deuda/nombres`
- `RESUELTO` · **DT-003** — [[0_proyecto/deuda-tecnica/03-shipibo-conibo|Shipibo-Conibo — credo vs facción]] · `#deuda/nombres` `#deuda/incongruencia` `#deuda/spoiler`
- `RESUELTO` · **DT-004** — [[0_proyecto/deuda-tecnica/04-el-caso-del-archivista-homonimo|El Caso del Archivista — homónimo y puntero stale]] · `#deuda/nombres` `#deuda/duplicado` `#deuda/incongruencia` `#deuda/prosa`
- `RESUELTO` · **DT-005** — [[0_proyecto/deuda-tecnica/05-folder-frontmatter-vs-ruta|folder ≠ ruta en block_de_notas]] · `#deuda/metadato` `#deuda/estructura`
- `RESUELTO` · **DT-006** — [[0_proyecto/deuda-tecnica/06-related-malformado-cecilia|related malformado (Cecilia Torres)]] · `#deuda/metadato` `#deuda/relacion`
- `RESUELTO` · **DT-007** — [[0_proyecto/deuda-tecnica/07-enlace-roto-confederacion|Enlace roto — Confederación Argentina]] · `#deuda/enlace-roto`
- `RESUELTO` · **DT-008** — [[0_proyecto/deuda-tecnica/08-fantasma-indice-template|Fantasma de índice — template-deuda-tecnica]] · `#deuda/estructura`
- `ABIERTO` · **DT-009** — [[0_proyecto/deuda-tecnica/09-seguridad-nacional-darsena-vs-dns|Seguridad Nacional Dársena vs DNS]] · `#deuda/incongruencia` `#deuda/incompleto`

> [!note] DT-001 estaba inline acá como ejemplo sembrado
> Se promovió a su propia tarjeta [[0_proyecto/deuda-tecnica/01-anatema-mecanico|01-anatema-mecanico]] (con sus variantes DT-001b/c). **No se borró nada**: la traza vive completa en la tarjeta.