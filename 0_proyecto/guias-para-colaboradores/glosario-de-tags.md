---
aliases:
  - Glosario de Tags
  - Glosario de Metadatos
  - SSOT de Tags
description: 'SSOT del modelo de frontmatter de syv-docs sobre markdown-vault-syv: campos controlados obligatorios, estandarizados, relaciones por wikilink, y tags como vivero open/closed.'
folder: 0_proyecto/guias-para-colaboradores
related:
  - '[[0_proyecto/guias-para-colaboradores/guia-de-metadatos|guia-de-metadatos]]'
  - '[[0_proyecto/guias-para-colaboradores/manual-del-colaborador|manual-del-colaborador]]'
tags: []
title: Glosario de Tags y Metadatos
entidad: guia
estado: canon
---

# Glosario de Tags y Metadatos

SSOT del **vocabulario y el modelo de campos** del frontmatter en `syv-docs`, diseñado para el motor `markdown-vault-syv`. `[[guia-de-metadatos]]` manda sobre el **formato**; este archivo manda sobre **qué campos existen y cómo se escriben**.

> [!important] El motor en una línea
> `markdown-vault-syv` da tres superficies: **semántica** (el cuerpo), **facetas** (campos de frontmatter, match exacto, solo los declarados) y **grafo** (wikilinks del cuerpo). Cada dato cae en una sola.

## Principio: una dimensión = un campo

Las dimensiones controladas **no** viven dentro de `tags` con barras. Cada una es **su propio campo** de frontmatter (faceta nativa, filtrable con `search(filters=...)` y `list_tags("campo")`).

### Campos obligatorios (toda ficha de entidad)
| Campo | Valor | Notas |
|---|---|---|
| `title` | texto | universal |
| `folder` | ruta | universal |
| `description` | 1–2 frases | universal |
| `entidad` | uno de: `personaje · faccion · ubicacion · concepto · credo · hito · relato · guia · objeto · vehiculo` | **exactamente uno**. Lista **abierta-extensible** (open/closed) |

### Campos estandarizados (cuando apliquen)
| Campo | Valor |
|---|---|
| `alcance` | `secreto` · `publico` (correlaciona con `spoilers`) |
| `estado` | `canon` · `borrador` · `propuesta` |

### Relaciones (wikilinks entre comillas, listas)
`facciones`, `ubicaciones`, `apariciones`, `related` → `"[[slug]]"`. Para que sean **aristas del grafo** deben repetirse en el cuerpo (ver [[0_proyecto/guias-para-colaboradores/recomendacion-wikilinks-en-prosa|recomendacion-wikilinks-en-prosa]]).

### Específicos
`nombre` (personajes), `region`, `fecha`, `fecha_exacta`, `spoilers` (lista).

`fecha_exacta` (hitos / cronología): fecha exacta del evento en formato ISO `YYYY-MM-DD`. **Opcional** — solo cuando el día se conoce con precisión canónica; complementa a `fecha`, que admite año o año-mes. No inventar el día si el canon no lo fija.

### `tags` — el vivero open/closed
`tags` deja de cargar dimensiones. Queda como **lado abierto**: etiquetas emergentes que querés filtrar exacto pero que aún no merecen campo propio.
- **NO** entra lo que ya es dimensión controlada (va a su campo) ni contenido descriptivo (lo halla la semántica).
- Lo que se usa seguido **gradúa** a campo propio (y se registra acá por PR).

## Cómo se escribe un valor
minúsculas · ASCII · guiones · **sin `#`** en frontmatter · una sola grafía (el motor hace match exacto, no perdona variantes).

## El principio open/closed
- **Closed**: los campos y valores de arriba — gobernados, en este glosario.
- **Open**: inventá el valor/campo que la situación pida; único deber → registrarlo por PR en este archivo.

## Antes / Después del refactor
```yaml
# ANTES
tags: [entidad/personaje, alcance/secreto, estado/canon]
# DESPUÉS
entidad: personaje
alcance: secreto
estado: canon
tags: []        # vivero, normalmente vacío tras migrar
```