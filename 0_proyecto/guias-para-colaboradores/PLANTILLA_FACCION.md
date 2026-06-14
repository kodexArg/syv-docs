---
title: Plantilla Facción
folder: 0_proyecto/guias-para-colaboradores
description: Estructura canónica para documentar facciones.
aliases:
  - Plantilla Facción
tags:
  - entidad/guia
related:
  - "[[guia-de-facciones]]"
  - "[[guia-de-metadatos]]"
---

Copiá este frontmatter al crear una facción. Reemplazá los valores; las relaciones
con otras facciones/actores van como **wikilinks** en `related`, los `tags` son
taxonomía. Ver [[guia-de-metadatos]].

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
tags:
  - entidad/faccion
  - alcance/publico   # o alcance/secreto si guarda secretos
---
```
