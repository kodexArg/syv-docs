---
title: Personajes
folder: 0_proyecto/guias-para-colaboradores
description: Categorías, metadatos, estructura de contenido para personajes.
entidad: guia
aliases:
  - Guía de Personajes
tags: []
related:
  - "[[guia-de-metadatos]]"
  - "[[manual-del-colaborador]]"
  - "[[guia-de-facciones]]"
---
Esta guía establece el formato y las mejores prácticas para crear y documentar personajes dentro del universo de "Subordinación y Valor". Un personaje bien definido es clave para la coherencia narrativa y la inmersión en el mundo.

Antes de crear un personaje, asegúrate de estar familiarizado con las guías generales, especialmente la [[guia-de-metadatos|Guía de Metadatos]] y el [[manual-del-colaborador|Manual del Colaborador]].

## Categorías de Personajes

Los personajes se clasifican en tres categorías según su importancia en la narrativa:

- **Canónicos/Principales**: PJs y NPCs clave que impulsan la trama principal, apareciendo en eventos y relatos significativos.
- **Secundarios**: PNJs con trasfondo y motivaciones definidas que enriquecen el mundo. Todo personaje mencionado en relatos debe registrarse aquí, excepto los principales.
- **Arquetipos**: Plantillas genéricas para roles o profesiones (ej: gendarme, médico, koskero).

## Metadatos de Personajes

La sección de metadatos (front matter YAML) es fundamental para la indexación y uso de los personajes por parte de herramientas automáticas y colaboradores.

Además de los campos universales (`title`, `folder`, `description`) definidos en la [[guia-de-metadatos|Guía de Metadatos]], los personajes siguen estas convenciones:

- `nombre`: Nombre del personaje. **Obligatorio**.
- `aliases`: Nombres alternativos / nombre propio para display y resistencia a renombres. **Recomendado**.
- `facciones`: Lista de **wikilinks** a los archivos de facción a los que pertenece. **Este campo debe existir siempre**, incluso si la lista está vacía. Ejemplo: `facciones: ["[[inquisicion]]"]`.
- `related` / `ubicaciones` / `apariciones`: listas de **wikilinks** a otras entidades, lugares del atlas y relatos donde aparece.
- `spoilers`: Lista de frases sensibles (reemplaza `alerta-spoiler`/`alerta-spoilers`). Acompañar con el campo `alcance: secreto`.
  - Ejemplo: `spoilers: ["Este personaje no debe ser presentado directamente a un jugador."]`

**IMPORTANTE**: Si este campo existe, no se deben mostrar los datos del personaje en el atlas, en las cartas, en los relatos, etc.

### Ejemplo Completo de Metadatos

```yaml
---
title: Inquisidora Sofía
folder: 3_personajes/principales
description: Joven y serena inquisidora, primer contacto de la Iglesia con agentes externos en Dársena.
aliases:
  - Sofía
nombre: Sofía
facciones:
  - "[[iglesia-de-darsena]]"
  - "[[inquisicion]]"
ubicaciones:
  - "[[sector-7]]"
spoilers:
  - "Su lealtad final es un secreto que no debe revelarse prematuramente."
entidad: personaje
alcance: secreto
tags: []
---
```

## Estructura del Contenido

El cuerpo del archivo de un personaje debe organizarse con los siguientes apartados para mantener la coherencia. El orden sugerido es el siguiente:

- **Aspecto**:
  - Descripción de la apariencia física del personaje. Esta sección no es obligatoria y solo debe completarse si se cuenta con información específica o una imagen de referencia. Puede incluir enlaces a recursos en `6_media/`.
  - Si el personaje tiene un nombre propio, se debe incluir en este apartado.
  - Su uso no es obligatorio, y no se requiere por defecto.

- **Descripción**:
  - Este es el apartado más importante y casi siempre requerido.
  - Aquí se desarrolla libremente la personalidad, comportamiento, manerismos y rol actual del personaje en el mundo.

- **Citas**:
  - Opcionalmente, se pueden incluir una o más citas textuales entre comillas para ilustrar la forma de hablar del personaje, su tono o sus ideas recurrentes.

- **Trasfondo**:
  - Un complemento a la descripción. Detalla la historia del personaje, su pasado, eventos significativos que lo marcaron y las relaciones importantes que ha forjado a lo largo de su vida.

- **Secretos / Trasfondo Oculto / Objetivos Ocultos**:
  - Estos apartados contienen información que no es evidente a primera vista. Revelar estos secretos debería requerir un esfuerzo significativo por parte de los jugadores, y en algunos casos, podría ser imposible.
  - Generalmente los personajes que tienen estos apartados también tienen una alerta de spoilers en metadatos.
  - **ATENCIÓN**: Si el personaje tiene un secreto o trasfondo oculto, no se debe hacer referencia a él en el atlas, en las cartas, en los relatos, etc.

- **Hoja de Personaje**:
  - Esta sección es específica para personajes jugadores (PJs) o NPCs muy relevantes que requieran estadísticas de juego. En la mayoría de los casos, no se utiliza.


---

Finalmente, recuerda enlazar a otros personajes, lugares o documentos con **wikilinks** (`[[slug]]`) en el cuerpo y en propiedades como `facciones`, `ubicaciones`, `apariciones` o `related`. Las dimensiones controladas (`entidad`, `alcance`, `estado`) van como **campos propios** del frontmatter, no dentro de `tags`. `tags` es el vivero open/closed para etiquetas emergentes. Ver [[guia-de-metadatos|Guía de Metadatos]] y [[glosario-de-tags]].
