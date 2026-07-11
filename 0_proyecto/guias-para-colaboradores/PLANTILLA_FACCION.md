---
title: Plantilla Facción
folder: 0_proyecto/guias-para-colaboradores
description: Estructura canónica para documentar facciones.
entidad: guia
aliases:
  - Plantilla Facción
tags: []
related:
  - "[[0_proyecto/guias-para-colaboradores/guia-de-facciones|guia-de-facciones]]"
  - "[[0_proyecto/guias-para-colaboradores/guia-de-metadatos|guia-de-metadatos]]"
---

Copiá este frontmatter al crear una facción. Reemplazá los valores; las relaciones
con otras facciones/actores van como **wikilinks** en `related`. Las dimensiones
controladas (`entidad`, `alcance`, `estado`) son **campos propios**, no tags.
Ver [[0_proyecto/guias-para-colaboradores/guia-de-metadatos|guia-de-metadatos]] y [[0_proyecto/guias-para-colaboradores/glosario-de-tags|glosario-de-tags]].

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
