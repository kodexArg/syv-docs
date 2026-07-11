---
aliases:
  - Wikilinks en la prosa
  - Ver relacionados
description: 'Recomendación de estilo: agrupar los wikilinks al final del artículo o sección en una tarjeta «Ver relacionados», en vez de intercalarlos en el párrafo, para una lectura más limpia. No obligatoria, sin migración.'
folder: 0_proyecto/guias-para-colaboradores
related:
  - '[[0_proyecto/guias-para-colaboradores/guia-de-metadatos|guia-de-metadatos]]'
  - '[[0_proyecto/guias-para-colaboradores/manual-del-colaborador|manual-del-colaborador]]'
tags: []
title: Wikilinks en la prosa (recomendación)
entidad: guia
estado: canon
---

# Wikilinks en la prosa

> [!tip] Esto es una recomendación, no una regla
> Es una preferencia de estilo. **No se migra nada** retroactivamente: aplica de
> acá en adelante, cuando escribas o edites un artículo. Un wikilink suelto en
> medio de la prosa, cuando el flujo lo pide, sigue siendo válido.

## La recomendación

Se **prefiere** ubicar los wikilinks **después del texto**, no intercalados en
medio del párrafo. En concreto:

- Juntalos **al final del artículo** o de la **sección** que los contiene.
- Presentalos en una **tarjeta** (callout) titulada **«Ver relacionados»**.

Así se ve la tarjeta:

```markdown
> [!info]- Ver relacionados
> [[sofia]] · [[inquisicion]] · [[tuberias]]
```

(El `-` la deja plegada por defecto: ocupa una línea hasta que el lector la abre.)

## Por qué

- **Lectura más limpia.** La prosa fluye sin cortes; el lector no tropieza con
  corchetes ni saltos en medio de una frase.
- **Relaciones a la vista.** Quien quiere navegar encuentra todas las conexiones
  juntas, al pie del artículo, en un solo lugar previsible.

## Nota sobre el grafo

Esto **no** debilita el grafo de relaciones. La tarjeta «Ver relacionados» vive en
el **cuerpo** del documento, así que sus wikilinks **siguen contando como aristas**
(el motor del corpus solo registra como relación los enlaces del cuerpo, no los del
frontmatter). La recomendación ordena la lectura *y*, de paso, mantiene las
relaciones navegables sin ensuciar el párrafo. Ver [[0_proyecto/guias-para-colaboradores/guia-de-metadatos|guia-de-metadatos]] para el
detalle de cómo se declaran relaciones.

## Anclas en el texto (cuando hace falta señalar la palabra)

Si querés que el lector sepa *qué palabra* corresponde a cada enlace —sin ensuciar
la prosa con corchetes—, usá una **nota al pie** sobre la primera mención, no un
wikilink inline. Se renderiza como un superíndice (p. ej. «Las Tuberías¹») y su
definición, que **sí** lleva el wikilink, se agrupa al pie:

```markdown
…sobreviven como grafitis en Las Tuberías[^tuberias] y en los murales del túnel…

[^tuberias]: [[2_atlas/ciudades/darsena/tuberias|Las Tuberías]]
```

Así el enlace queda **abajo, no inline**, y el grafo conserva la arista (la
definición vive en el cuerpo, no en el frontmatter). Es el mismo criterio de la
tarjeta de cierre, solo que con ancla puntual.

El bloque de cierre puede titularse **«Ver relacionados»** o **«Ver también»**:
son equivalentes. Elegí uno y mantenelo dentro del documento.

## Alcance

- Recomendación, no obligación.
- Sin migración retroactiva: nadie tiene que reescribir lo viejo por esto.

> [!info]- Ver relacionados
> [[0_proyecto/guias-para-colaboradores/guia-de-metadatos|guia-de-metadatos]] · [[0_proyecto/guias-para-colaboradores/manual-del-colaborador|manual-del-colaborador]]