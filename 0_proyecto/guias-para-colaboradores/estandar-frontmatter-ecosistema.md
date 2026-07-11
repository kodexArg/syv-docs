---
aliases:
- Estándar de Frontmatter SyV
- Frontmatter del Ecosistema
- Estándar de Frontmatter Ecosistémico
description: 'Baseline de higiene de frontmatter compartido por todo el ecosistema
  SyV, con el contrato por clase de documento y las exenciones explícitas: contratos
  de código, spec de skills y archivos generados.'
entidad: guia
estado: propuesta
folder: 0_proyecto/guias-para-colaboradores
related:
- '[[0_proyecto/guias-para-colaboradores/glosario-de-tags|Glosario de Tags]]'
- '[[0_proyecto/guias-para-colaboradores/guia-de-metadatos|Metadatos]]'
tags: []
title: Estándar de Frontmatter del Ecosistema SyV
---

> [!important] Un baseline compartido, no un molde único
> SyV no es un vault homogéneo: es un conjunto de repos con roles distintos, y **cada subsistema tiene su propio contrato de frontmatter**, gobernado por su propia autoridad. Este documento fija la **higiene compartida** que aplica a todo documento human-facing, y marca **explícitamente las exenciones**: los schemas que NO se tocan con las reglas del corpus de lore.

## Por qué no hay "un solo frontmatter para todo"

Auditado (jul 2026): fuera de `syv-docs`, el frontmatter rico o lo consume código o lo genera un script. Aplicar la taxonomía de lore (`entidad`, `spoilers`, `region`…) a ciegas rompería backends y tests de contrato. La extensión correcta de los principios **no es un barrido de archivos** — es este contrato por clase.

## Las clases de documento

| Clase | Dónde | Quién gobierna su schema | Reglas de lore |
|---|---|---|---|
| **Vault de lore** | `syv-docs` | [[0_proyecto/guias-para-colaboradores/glosario-de-tags\|Glosario de Tags]] + [[0_proyecto/guias-para-colaboradores/guia-de-metadatos\|Metadatos]] | ✅ completas |
| **Vault human/agente** | docs a mano de `syv-image-generation` | este estándar (baseline) | ◐ solo baseline |
| **Contrato de datos** | `syv-pj` | su `MODEL.md` · `API.md` · `hoja-personaje.md` + tests | ⛔ exento |
| **Spec de skills/agentes** | `syv-harness` | spec de skills de Claude Code (`name`/`model`/`tools`/`effort`) | ⛔ exento |
| **Generado** | `syv-image-generation/prompts/characters/*.md` | su generador (`scripts/sheet_to_comfy.py`) — dice *"no editar a mano"* | ⛔ se regenera |
| **Docs técnicos** | `syv-map` · `syv-pj-api` · `syv-pj-frontend` · `syv-pj-flutter` · `syv-design-system` · `syv-frontend` | convención del repo | ➖ mínimo/opcional |

## Baseline compartido (todo doc human-facing nuevo)

Aplica a documentación escrita **a mano** en cualquier repo. Es el subconjunto **transferible** de las reglas del corpus:

1. **YAML válido** — bloque `---`, espacio tras cada `:`, sin tabs, nunca vacío.
2. **`title` + `description`** presentes en todo doc human-facing.
3. **Nombres de campo** en inglés, minúscula, átomo (`snake` o guion). Nada de campos español-multi-palabra nuevos.
4. **Valores de faceta = átomos** — minúscula, ASCII, guiones, una sola grafía (`cordoba`, no `Córdoba`); el match es exacto.
5. **`tags` = vivero** — normalmente `[]`, sin barras, sin dimensiones ni relaciones.
6. **Relaciones = wikilinks**, en frontmatter **y** con eco en prosa (el grafo del MCP solo ve el cuerpo).
7. **Links path-qualified** relativos a la raíz del vault del documento (ver abajo).

## Exenciones — no apliques las reglas del corpus acá

> [!warning] Estos schemas tienen dueño; tocarlos rompe cosas
> - **`syv-pj`** — su frontmatter (`nombre`, `probabilidad`, `peso_sorteo`, `sesgo_faccion`, `tags` con barras…) lo parsea el motor procedural y lo cubren tests de contrato. Renombrar campos o "arreglar" los `tags` es un breaking change: cualquier cambio es una migración coordinada de datos + Pydantic + tests, gobernada por su `MODEL.md`.
> - **`syv-harness`** — los `.md` de skills/agentes usan el frontmatter del spec de Claude Code (`name`, `description`, `model`, `tools`, `effort`). No llevan `title` ni `entidad`.
> - **Archivos generados** — los docs de `syv-image-generation/prompts/characters/` los emite `sheet_to_comfy.py`; su formato se cambia en el **generador**, nunca a mano (una edición manual se pierde al regenerar).

## Links y la raíz del vault

SyV tiene **vaults anidados**: hay un `.obsidian` en **`~/SyV/`** (ecosistema) y otro en **`~/SyV/syv-docs/`** (corpus). Cada documento path-qualifica **relativo a la raíz de su propio vault**:

- Dentro de `syv-docs` → relativo a `syv-docs`: `[[2_atlas/ciudades/darsena/darsena|Dársena]]`. Coincide con el MCP `markdown-vault-syv`, cuyo root es `syv-docs`.
- Cross-repo desde el ecosistema → relativo a `~/SyV`: `[[syv-pj/resources/personajes/damian-diconte-detective|Damián DiConte]]`.

Así cada link resuelve **determinísticamente** en su vault, sin depender de resolución por basename. Herramienta: el skill `syv-link-qualifier`, apuntado al vault correcto.

> [!question] Decisión abierta — reconciliar los dos vaults
> El corpus vive en dos raíces a la vez (MCP = `syv-docs`; Obsidian del ecosistema = `~/SyV`). Un link interno de `syv-docs` correcto para el MCP (`[[2_atlas/...]]`) **no** resuelve si abrís `~/SyV` como vault (esperaría `[[syv-docs/2_atlas/...]]`). Falta decidir: ¿el corpus se navega como su propio vault (status quo, MCP-first) o se unifica todo bajo `~/SyV` (y hay que prefijar `syv-docs/`, incompatible con el root del MCP)? Hasta resolverlo, **cada doc path-qualifica a la raíz de su propio vault**.

## Enforcement

- El linter de reglas (`syv-juez-reglas`) valida el baseline en docs human-facing y **saltea** las clases exentas según su clase de documento.
- `syv-link-qualifier` mantiene los links path-qualified por-vault (idempotente).
- Los schemas exentos los validan sus propios dueños: los tests de `syv-pj`, el spec de skills, y el generador de retratos.