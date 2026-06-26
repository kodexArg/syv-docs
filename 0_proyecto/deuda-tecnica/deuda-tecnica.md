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

**Manual + registro vivo** de la deuda técnica del corpus: errores, incongruencias y roturas que se descubren mientras el universo crece. Este archivo **no corrige, describe el problema**. Arriba está el manual (tags, estados, plantilla); bajo la línea, las incidencias se suman hacia abajo a medida que aparecen.

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

## Incidencias

### `ABIERTO` · DT-001 — La Gran Guerra Global está sin desarrollar en la Cronología
#deuda/incompleto
**Afecta:** [[1_trasfondo/cronologia|Cronología]] — secciones «2036-2039: Preludio a la Gran Guerra Global» y «2039-2047: La Gran Guerra Global»

```gherkin
# language: es
Escenario: El corazón bélico del canon es un marcador de relleno
  Dado que la Cronología es la columna vertebral del canon (2020 → 2178)
  Y que esas dos secciones sólo contienen el texto "[Sección a desarrollar]"
  Cuando un relato, hito o ficha necesita anclar un hecho entre 2036 y 2047
  Entonces no hay canon donde apoyarse y se arriesga inventar incongruencias
```