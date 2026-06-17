---
title: Metadatos
folder: 0_proyecto/guias-para-colaboradores
description: Formato autoritativo del frontmatter YAML, relaciones por wikilink, taxonomía de tags y aliases.
entidad: guia
aliases:
  - Guía de Metadatos
tags: []
related:
  - "[[manual-del-colaborador]]"
  - "[[guia-de-personajes]]"
  - "[[guia-de-facciones]]"
---

# Guía de Metadatos

Esta es la guía **única y autoritativa** del frontmatter YAML de "Subordinación y Valor". El corpus es un vault de Obsidian operado por el motor `markdown-vault-syv`: el grafo de conocimiento se construye **solo con wikilinks**, las dimensiones controladas (`entidad`, `alcance`, `estado`) son **campos propios** del frontmatter, los `tags` son un **vivero** abierto para etiquetas emergentes, y los `aliases` protegen contra renombres. Si algo acá contradice otra guía, manda esta — salvo el `[[glosario-de-tags]]`, SSOT de qué campos existen y cómo se escriben.

> [!important] Cómo lo ve `markdown-vault-syv`
> El motor da tres superficies, y cada dato cae en **una sola**: **semántica** (el cuerpo), **facetas** (los campos de frontmatter — *match exacto*, una sola grafía, solo se indexan los campos declarados) y **grafo** (los wikilinks del cuerpo). Por eso una dimensión no se mete dentro de `tags` con barras: cada una es su campo, faceta nativa filtrable con `search(filters=...)`. La jerarquía **no se parte**: el valor es un átomo (`personaje`), no una ruta (`entidad/personaje`).

> [!important]
> El estándar YAML exige el **espacio después de los dos puntos** (`title: Valor`, no `title:Valor`). El bloque va al inicio del archivo, entre líneas `---`. Nombres de campo en **inglés y minúsculas**.

---

## Las tres ideas centrales

1. **Las relaciones son wikilinks.** Personaje ↔ facción ↔ ubicación ↔ concepto ↔ relato se conectan con `[[slug]]`, tanto en el cuerpo como dentro de propiedades de lista del frontmatter (`facciones`, `related`, `ubicaciones`, `apariciones`). El grafo **no** ve los `tags`.
2. **Las dimensiones controladas son campos, no tags.** `entidad`, `alcance` y `estado` viven cada uno en **su propio campo** del frontmatter (faceta de match exacto), no dentro de `tags`. `tags` queda como **vivero** open/closed: etiquetas emergentes que aún no merecen campo propio. Nunca un tag para apuntar a otro archivo. (Esto **reemplaza** tanto la vieja "Regla de Oro" de tag-como-slug como el esquema `#entidad/...` dentro de `tags`. Ver [[glosario-de-tags]].)
3. **Los aliases dan estabilidad y display.** Toda entidad debería declarar `aliases` con su nombre propio, para sobrevivir renombres y mostrar `[[slug|Texto Visible]]`.

---

## Campos del frontmatter

### Universales (todo archivo)

| Campo | Obligatorio | Qué es |
|---|---|---|
| `title` | sí | Título del documento. |
| `folder` | sí | Ruta relativa de la carpeta contenedora. |
| `description` | sí | Una o dos frases del contenido. |
| `entidad` | sí (entidades) | **Exactamente uno** de: `personaje · faccion · ubicacion · concepto · credo · hito · relato · guia · objeto · vehiculo`. Campo propio (faceta), **no** un tag. Lista abierta-extensible. |
| `alcance` | cuando aplique | `secreto` · `publico`. Correlaciona con `spoilers`. Campo propio. |
| `estado` | cuando aplique | `canon` · `borrador` · `propuesta`. Campo propio. |
| `aliases` | recomendado | Lista de nombres alternativos (nombre propio, variantes). |
| `tags` | opcional | **Vivero** open/closed: etiquetas emergentes (normalmente `[]`). **No** cargan dimensiones ni son links. |
| `related` | opcional | Lista de **wikilinks** a entidades relacionadas sin campo propio. |

### Específicos por tipo de entidad

| Campo | Aplica a | Qué es |
|---|---|---|
| `nombre` | personajes | Nombre propio del personaje. **Obligatorio** en personajes. |
| `facciones` | personajes, otros | Lista de **wikilinks** a archivos de facción. Siempre presente en personajes (vacía si no aplica). |
| `ubicaciones` | varios | Lista de **wikilinks** a archivos del atlas. |
| `apariciones` | personajes, lugares | Lista de **wikilinks** a relatos/crónicas/cartas donde aparece. |
| `region` | atlas, cronología | Región geográfica, p. ej. `Sud América, Argentina, Ciudad Dársena`. |
| `fecha` | cronología, atlas | Fecha o año de referencia. |
| `spoilers` | cualquiera con secreto | Lista de frases sensibles. Reemplaza `alerta-spoiler`/`alerta-spoilers`. |

---

## Relaciones por wikilink

Las propiedades que expresan relación contienen **wikilinks entre comillas** (YAML exige comillas porque `[[...]]` arranca con corchete):

```yaml
facciones:
  - "[[inquisicion]]"
  - "[[iglesia-de-darsena]]"
related:
  - "[[damian-diconte]]"
ubicaciones:
  - "[[tuberias]]"
apariciones:
  - "[[walter|Walter (relato)]]"
```

✓ `facciones: ["[[inquisicion]]"]`
✗ `facciones: ["Sagrada Inquisición Argentina"]` (nombre-display: no enlaza)
✗ `tags: [inquisicion]` (los tags no son relaciones)

### Desambiguación de basenames

El vault raíz `/home/kodex/Dev/SyV` contiene basenames duplicados (p. ej. existe `walter.md` como personaje **y** como relato; hay varios `index.md`). Cuando un slug es ambiguo:

- Preferí un **nombre de archivo único** al crear (`walter` personaje, `walter-relato` el relato), o
- Usá **wikilink con path** cuando haga falta: `[[4_diegesis/relatos/walter|Walter (relato)]]`.
- Declará `aliases` para que el display sea el nombre propio sin importar el slug.

---

## Dimensiones controladas y el vivero `tags`

Las tres dimensiones controladas son **campos propios**, cada uno con su catálogo cerrado de valores. El motor las indexa como facetas de **match exacto** (una sola grafía, minúsculas, ASCII, guiones, sin `#`):

```yaml
entidad: personaje      # personaje · faccion · ubicacion · concepto · credo · hito · relato · guia · objeto · vehiculo
alcance: secreto        # secreto · publico
estado: canon           # canon · borrador · propuesta
```

- Toda ficha de entidad lleva **exactamente un** valor de `entidad`.
- `alcance: secreto` marca contenido con secretos (correlaciona con `spoilers`).
- El valor es un **átomo**, no una ruta: `entidad: personaje`, nunca `entidad/personaje`.

`tags` queda como **vivero open/closed**: el lado abierto para etiquetas emergentes que querés filtrar exacto pero que aún no merecen campo propio. Normalmente `[]`. **No** entra lo que ya es dimensión controlada (va a su campo) ni contenido descriptivo (lo halla la semántica del cuerpo). Lo que se usa seguido **gradúa** a campo propio, y se registra por PR en el [[glosario-de-tags]].

✓ `entidad: personaje` · `alcance: secreto` · `tags: []`
✗ `tags: ["entidad/personaje", "alcance/secreto"]` (dimensiones → campos propios)
✗ `tags: ["walter", "tuberias"]` (eso son relaciones → wikilinks)
✗ `tags: ["misterio", "futuro"]` (palabra suelta descriptiva → la halla la semántica)

---

## Aliases

```yaml
aliases:
  - Sofía
  - Inquisidora Sofía
```

Permite escribir `[[inquisidora-sofia|Sofía]]` y que Obsidian resuelva referencias por cualquiera de los nombres. Imprescindible cuando el `title`/nombre propio difiere del slug.

---

## Spoilers

Campo `spoilers`: lista de frases sensibles. Unifica los legacy `alerta-spoiler` y `alerta-spoilers` (escalar string), que quedan **prohibidos**.

```yaml
spoilers:
  - "Su lealtad final no debe revelarse prematuramente."
tags:
  - entidad/personaje
  - alcance/secreto
```

> [!warning]
> Si una entidad tiene `spoilers`, **no se la referencia** desde atlas, relatos ni cartas de forma que exponga el secreto. (Ver [[guia-de-personajes]].)

---

## Ejemplos canónicos

### Personaje

```yaml
---
title: Inquisidora Sofía
folder: 3_personajes/principales
description: Primer contacto de la Iglesia con agentes externos en Dársena.
aliases:
  - Sofía
nombre: Sofía
facciones:
  - "[[iglesia-de-darsena]]"
  - "[[inquisicion]]"
ubicaciones:
  - "[[sector-7]]"
apariciones:
  - "[[el-primer-contacto]]"
spoilers:
  - "Su lealtad final es un secreto."
tags:
  - entidad/personaje
  - alcance/secreto
---
```

### Facción

```yaml
---
title: Arpistas
folder: 1_trasfondo/facciones/facciones-menores
description: Red proscrita de arqueólogos tecnológicos que neutralizan y preservan tecnología prohibida.
aliases:
  - Los Arpistas
related:
  - "[[inquisicion]]"
  - "[[dgapc]]"
  - "[[iglesia-de-darsena]]"
tags:
  - entidad/faccion
  - alcance/publico
---
```

### Ubicación (atlas)

```yaml
---
title: Las Tuberías
folder: 2_atlas/darsena
description: Comunidad subacuática bajo Dársena.
aliases:
  - Tuberías
region: Argentina, Ciudad Dársena
related:
  - "[[walter]]"
tags:
  - entidad/ubicacion
---
```

### Relato (diegesis)

```yaml
---
title: Walter
folder: 4_diegesis/relatos
description: Fragmento de la juventud de Walter en las Tuberías.
aliases:
  - Walter (relato)
related:
  - "[[walter]]"
  - "[[tuberias]]"
tags:
  - entidad/relato
---
```

### Hito / cronología

```yaml
---
title: "2031: El Año del Cráter"
folder: 1_trasfondo/cronologia/2030-2039
description: Argentina se vuelve un mosaico de territorios en guerra.
region: Argentina
fecha: 2031
related:
  - "[[guerra-civil]]"
tags:
  - entidad/hito
---
```

---

## Migración: qué cambia respecto al esquema viejo

- `tags` deja de ser slug-de-archivo → pasa a taxonomía `#entidad/...`. Las relaciones que vivían en `tags` se mueven a `related`/`facciones`/`ubicaciones` como wikilinks.
- `facciones` con nombre-display (`"Iglesia Católica"`) → wikilink al slug (`"[[iglesia-catolica]]"`).
- `alerta-spoiler` / `alerta-spoilers` (string) → `spoilers` (lista) + tag `#alcance/secreto`.
- Sintaxis `@[ruta.md]` de guías viejas → wikilink `[[slug]]`.
- No se renombran `nombre`/`region`/`fecha`: el cambio es tags→taxonomía, relaciones→wikilinks, aliases.

> [!note]
> Los scripts `check_tags.py` / `remove_tags.py` (regla de tags pre-taxonomía) fueron eliminados y reemplazados por `_tools/migrate_metadata.py` — un migrador determinista basado en ruamel, con dry-run por defecto e `--apply` para escribir cambios.

---

Las reglas indelebles de este esquema viven en `.claude/rules/` (un contrato por archivo). **Actualizá esta guía si se agrega o modifica un campo o una rama de taxonomía.**
