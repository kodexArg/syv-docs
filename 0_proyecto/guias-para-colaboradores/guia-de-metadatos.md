---
title: Metadatos
folder: 0_proyecto/guias-para-colaboradores
description: Formato y reglas del frontmatter YAML para archivos markdown.

tags:
  - guia
  - metadatos
  - colaboracion

---


# Guía de Metadatos para archivos `.md` en SyV

Esta guía explica el formato **único y correcto** de metadatos (front matter YAML) que deben tener todos los archivos Markdown del proyecto "Subordinación y Valor".

**IMPORTANTE**: Mantener el estándar YAML en el frontmatter incluye respetar el espacio luego de dos puntos.

- El bloque de metadatos es obligatorio.
- Debe ir al inicio del archivo, delimitado por líneas `---`.
- Todos los campos deben estar en **inglés** y en **minúsculas**.
- Los siguientes campos van al inicio:
  - `title`: Título del documento. **Obligatorio**.
  - `slug`: Identificador único. Debe coincidir exactamente con el nombre del archivo (sin extensión). **Opcional** (implícito en el nombre del archivo, pero si se incluye debe coincidir).
  - `folder`: Ruta relativa de la carpeta donde se ubica el archivo. **Obligatorio**.
  - `description`: Breve descripción del contenido. **Obligatorio**.
  - `tags`: Lista de slugs de otros archivos relacionados. Se usan como referencias directas a otros documentos. **Opcional pero recomendado**.
- Los siguientes son campos opcionales:
  - `region`: Región geográfica separada por comas, por ejemplo "Sud América, Argentina, Ciudad Dársena". **Opcional**.
  - `fecha`: Fecha de referencia, se usa en cronología y atlas. **Opcional**.
- Los personajes tienen los siguientes campos específicos:
  - `nombre`: Nombre del personaje. **Obligatorio**.
  - `facciones`: Listado de facciones a las que pertenece (slugs de archivos de facción). **Obligatorio**.
  - `spoilers`: Indica frases o información a presentar con discreción (reemplaza a `alerta-spoiler`). **Opcional**.


## Criterios de Etiquetado (Tags)

**Definición Estricta**: Un 'tag' en este proyecto es **exclusivamente una referencia a otro archivo existente**.

- Cada archivo tiene un `slug` implícito, que es su **nombre de archivo**.
- Las etiquetas (`tags`) son una lista de estos `slugs` (archivos) con los que el documento actual tiene una relación directa.
- **No existen "temas", "categorías" o "palabras clave" sueltas.**
- **Regla de Oro**: Si no existe un archivo (slug) para un concepto, personaje o lugar, **no se puede etiquetar**.

### Cómo etiquetar
Usa simplemente el **slug** del archivo (nombre del archivo sin extensión) para referenciarlo.

### Qué etiquetar (linkear)
- **Personajes**: Slug del archivo del personaje (ej: `inquisidora-sofia`).
- **Ubicaciones**: Slug del archivo del lugar en el Atlas (ej: `tuberias`).
- **Facciones**: Slug del archivo de la organización (ej: `sia`).
- **Conceptos**: Slug del archivo que explica el concepto (ej: `anatema-mecanico`).

### Qué NO etiquetar
- Palabras sueltas como "misterio", "acción", "futuro".
- Categorías que no tienen un archivo "índice" o explicativo específico.
- El propio archivo o carpetas padres (redundante).


## Buenas prácticas
- Mantén los campos alineados y sin tabulaciones.
- Los `tags` deben ser links directos a archivos existentes, no palabras clave genéricas.
- Usa el slug del archivo (nombre sin extensión) para los tags.
- Verifica que los links en `tags` y `facciones` apunten a archivos válidos.
- No repitas información entre campos.
- La descripción debe ser breve y clara.
- No uses caracteres especiales en los nombres de campos.
- No dejes el bloque de metadatos vacío.
- Si agregas nuevos campos, documenta su uso en esta guía.
- **Usa siempre campos en inglés** (`title`, `folder`, `description`), nunca en español.


## Ejemplos correctos

```yaml
---
title: Año 2031: El Año del Cráter
slug: 2031-ano-del-crater
folder: 1_trasfondo/cronologia/2030-2039
description: El año en que Argentina se convirtió en un mosaico de territorios en guerra.
tags:
- guerra-civil
- mapa-politico
region: Argentina
fecha: 2031
---
```

```yaml
---
title: Cardenal J.M.
folder: 3_personajes/iglesia
description: Líder de la facción eclesiástica en el sector 7.
nombre: Juan Manuel
facciones:
- iglesia
spoilers:
- "Muere en el capítulo 4"
---
```


---

**Actualiza esta guía si se agregan o modifican campos de metadatos en el proyecto.**
