---
title: Personajes
folder: 0_proyecto/guias-para-colaboradores
description: Categorías, metadatos, estructura de contenido para personajes.
tags:
  - guia
  - personajes
  - colaboracion

---
Esta guía establece el formato y las mejores prácticas para crear y documentar personajes dentro del universo de "Subordinación y Valor". Un personaje bien definido es clave para la coherencia narrativa y la inmersión en el mundo.

Antes de crear un personaje, asegúrate de estar familiarizado con las guías generales, especialmente la [Guía de Metadatos](./guia-de-metadatos.md) y el [Manual del Colaborador](./manual-del-colaborador.md).

## Categorías de Personajes

Los personajes se clasifican en tres categorías según su importancia en la narrativa:

- **Canónicos/Principales**: PJs y NPCs clave que impulsan la trama principal, apareciendo en eventos y relatos significativos.
- **Secundarios**: PNJs con trasfondo y motivaciones definidas que enriquecen el mundo. Todo personaje mencionado en relatos debe registrarse aquí, excepto los principales.
- **Arquetipos**: Plantillas genéricas para roles o profesiones (ej: gendarme, médico, koskero).

## Metadatos de Personajes

La sección de metadatos (front matter YAML) es fundamental para la indexación y uso de los personajes por parte de herramientas automáticas y colaboradores.

Además de los campos obligatorios (`titulo`, `carpeta`, `descripcion`) definidos en la [Guía de Metadatos](./guia-de-metadatos.md), los personajes siguen estas convenciones:

- `slug`: Debe coincidir con el nombre del archivo. **Opcional**.
- `nombre`: Nombre del personaje. **Obligatorio**.
- `facciones`: Una lista de links a los archivos de las facciones a las que pertenece el personaje. **Este campo debe existir siempre**, incluso si la lista está vacía.
- `spoilers`: Campo opcional para advertir sobre información sensible (anteriormente `alerta-spoiler`). Contiene una lista de frases que indican si el personaje debe ser presentado con discreción.
  - Ejemplo: `spoilers: ["Este personaje no debe ser presentado directamente a un jugador."]`

**IMPORTANTE**: Si este campo existe, no se deben mostrar los datos del personaje en el atlas, en las cartas, en los relatos, etc.

### Ejemplo Completo de Metadatos

```yaml
---
titulo: "Inquisidora Sofía"
slug: inquisidora-sofia
carpeta: 3_personajes/principales
descripcion: "Joven y serena inquisidora que sirve como primer contacto de la Iglesia con agentes externos en Dársena."
nombre: Sofía
tags:
  - @[1_trasfondo/facciones/iglesia.md]
  - @[2_atlas/darsena/sector-7.md]
facciones:
  - @[1_trasfondo/facciones/iglesia-de-darsena.md]
  - @[1_trasfondo/facciones/santa-inquisicion.md]
spoilers:
  - "Su lealtad final es un secreto que no debe revelarse prematuramente."
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

Finalmente, recuerda usar los **Tags** en los metadatos (ver [Guía de Metadatos](./guia-de-metadatos.md)) para enlazar a otros personajes, lugares o documentos relevantes.
