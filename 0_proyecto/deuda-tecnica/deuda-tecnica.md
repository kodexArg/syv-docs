---
description: 'Manual y registro vivo de deuda técnica del corpus SyV: cada incidencia
  con estado, título, referencia y un escenario BDD/Gherkin.'
folder: 0_proyecto/deuda-tecnica
related:
- '[[0_proyecto/0_proyecto|Proyecto]]'
- '[[0_proyecto/guias-para-colaboradores/guia-de-metadatos|Guía de Metadatos]]'
tags: []
title: Deuda Técnica
---

**Manual + registro vivo** de la deuda técnica del corpus: errores, incongruencias y roturas que se descubren mientras el universo crece. Este archivo **no corrige, describe el problema**. Arriba, cómo se usa; bajo la línea, las incidencias se suman hacia abajo a medida que aparecen.

> [!info] Cómo se anota una incidencia
> Siempre en este orden:
> 1. **ESTADO** — lo primero y lo más importante.
> 2. **Título** — corto e inequívoco (con id `DT-NNN`).
> 3. **Referencia de archivo** — al menos una, como `[[wikilink]]`.
> 4. **BDD** — un `Escenario` que **replica** el error (`Dado` / `Cuando` / `Entonces`) o lo **describe** de forma semántica.
>
> Acá **describimos el problema, no la solución**. Y **no se borra nada**: una incidencia cerrada pasa a `RESUELTO` o `DESCARTADO` y conserva su traza.

## Estados

| Estado | Significado |
|---|---|
| `ABIERTO` | Detectada, sin resolver. |
| `EN-REVISION` | En análisis o discusión. |
| `RESUELTO` | Corregida — se conserva la traza. |
| `DESCARTADO` | No era un error, o no se corrige. |

## Plantilla

Copiá este bloque por cada hallazgo:

````markdown
### `ABIERTO` · DT-NNN — <título corto e inequívoco>
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

%% La primera incidencia va acá, bajo la línea. Copiá la plantilla de arriba. %%