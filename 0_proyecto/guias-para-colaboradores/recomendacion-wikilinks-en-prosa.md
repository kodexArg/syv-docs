---
aliases:
  - Wikilinks en la prosa
  - Ver relacionados
description: 'Recomendación de estilo: agrupar los wikilinks al final del artículo o sección en una tarjeta «Ver relacionados», en vez de intercalarlos en el párrafo, para una lectura más limpia. No obligatoria, sin migración.'
folder: 0_proyecto/guias-para-colaboradores
related:
  - '[[guia-de-metadatos]]'
  - '[[manual-del-colaborador]]'
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
relaciones navegables sin ensuciar el párrafo. Ver [[guia-de-metadatos]] para el
detalle de cómo se declaran relaciones.

## Alcance

- Recomendación, no obligación.
- Sin migración retroactiva: nadie tiene que reescribir lo viejo por esto.

> [!info]- Ver relacionados
> [[guia-de-metadatos]] · [[manual-del-colaborador]]