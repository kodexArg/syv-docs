---
description: Registro vivo de errores e incongruencias del corpus SyV, anotados como
  escenarios Gherkin.
folder: 0_proyecto/deuda-tecnica
related:
- '[[0_proyecto/0_proyecto|Proyecto]]'
- '[[0_proyecto/guias-para-colaboradores/guia-de-metadatos|Guía de Metadatos]]'
tags: []
title: Deuda Técnica
---

Registro vivo de **deuda técnica** del corpus: errores, incongruencias y roturas que se descubren mientras el universo crece. Este archivo **no corrige, documenta**. Crece hacia abajo: cada hallazgo se suma como un escenario nuevo y nunca se reescribe lo anterior.

Cada incidencia es un **escenario [Gherkin](https://cucumber.io/docs/gherkin/)** — una línea por hecho — para que se lea sola: `Dado` el estado canónico, `Cuando` aparece el disparador, `Entonces` se ve la contradicción.

> [!info] Cómo se anota una incidencia
> - Un **`Escenario`** por error, con id correlativo `DT-NNN`.
> - **`Dado`** = la verdad canónica o dónde vive · **`Cuando`** = qué dispara el conflicto · **`Entonces`** = la contradicción observable.
> - Las **etiquetas `@…`** sobre el escenario fijan *estado · categoría · severidad* (ver leyenda).
> - La gestión va en comentarios `#` (**afecta · detectado · propuesta**). Ojo: los `[[wikilinks]]` **no** enlazan dentro de un bloque de código, así que ahí van **rutas**, no wikilinks.
> - **No se borra nada**: una incidencia cerrada pasa a `@resuelto` o `@descartado` y conserva su traza.

## Leyenda de etiquetas

| Dimensión | Valores |
|---|---|
| **Estado** | `@abierto` · `@en-revision` · `@resuelto` · `@descartado` |
| **Categoría** | `@fechas` · `@nombres` · `@incongruencia` · `@enlace-roto` · `@huerfano` · `@spoiler` · `@metadato` |
| **Severidad** | `@critico` · `@alto` · `@medio` · `@bajo` |

## Registro de incidencias

```gherkin
# language: es
@abierto @nombres @medio
Escenario: DT-001 — Dos entidades comparten el basename "walter"
  Dado el personaje en 2_atlas/darsena/walter.md
  Y el relato homónimo en 4_diegesis/relatos/walter.md
  Cuando una nota enlaza con [[walter]] sin ruta
  Entonces el wikilink resuelve a un archivo de forma no determinista
  Y el grafo puede conectar la entidad equivocada
  # afecta: 2_atlas/darsena/walter.md, 4_diegesis/relatos/walter.md
  # detectado: 2026-06-25 · regla naming-and-links
  # propuesta: renombrar el relato a walter-relato.md o enlazar con ruta completa
```

## Plantilla (copiar para cada hallazgo nuevo)

```gherkin
# language: es
@abierto @categoria @severidad
Escenario: DT-NNN — <título corto e inequívoco de la incidencia>
  Dado <el hecho canónico, o el lugar donde vive la verdad>
  Y <segundo hecho relevante, si aplica>
  Cuando <la condición que dispara el conflicto>
  Entonces <la contradicción observable / lo que se rompe>
  # afecta: <ruta>, <ruta>...
  # detectado: <YYYY-MM-DD> · <quién o qué regla lo halló>
  # propuesta: <corrección sugerida en una línea>
```