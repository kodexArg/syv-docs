---
title: Plantilla Facción
folder: 0_proyecto/guias-para-colaboradores
description: Estructura canónica para documentar facciones.
entidad: guia
aliases:
  - Plantilla Facción
tags: []
related:
  - "[[guia-de-facciones]]"
  - "[[guia-de-metadatos]]"
---

Copiá este frontmatter al crear una facción. Reemplazá los valores; las relaciones
con otras facciones/actores van como **wikilinks** en `related`. Las dimensiones
controladas (`entidad`, `alcance`, `estado`) son **campos propios**, no tags.
Ver [[guia-de-metadatos]] y [[glosario-de-tags]].

```yaml
---
title: Nombre de la Facción
folder: 1_trasfondo/facciones/<subcarpeta>
description: Una o dos frases que la definan.
aliases:
  - Nombre alternativo
related:
  - "[[slug-faccion-aliada]]"
  - "[[slug-faccion-rival]]"
entidad: faccion
alcance: publico   # o secreto si guarda secretos
estado: canon      # o propuesta / borrador
tags: []
---
```
