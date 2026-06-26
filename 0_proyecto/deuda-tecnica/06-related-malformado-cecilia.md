---
description: 'El campo related de hermana-cecilia-torres.md es un string JSON en lugar
  de una lista YAML de wikilinks: no genera aristas en el grafo.'
folder: 0_proyecto/deuda-tecnica
related:
- '[[3_personajes/secundarios/hermana-cecilia-torres|Hermana Cecilia Torres]]'
- '[[0_proyecto/deuda-tecnica/deuda-tecnica|Deuda Técnica]]'
tags: []
title: DT-006 · `related` malformado en Hermana Cecilia Torres (string en vez de lista)
---

> [!success] RESUELTO · 2026-06-26
> El `related` de Cecilia ahora es lista YAML de wikilinks (genera aristas). De paso se detectó y corrigió el mismo bug en `aliases`/`related` del hito **2031-la-fragmentacion**. Verificado. Traza abajo.

> [!info] Tarjeta de deuda técnica
> Tema: **relación que no enlaza** por frontmatter mal tipado.

### `ABIERTO` · DT-006 — `related` es un string, no una lista de wikilinks
#deuda/metadato #deuda/relacion
**Afecta:** [[3_personajes/secundarios/hermana-cecilia-torres|Hermana Cecilia Torres]]

```gherkin
# language: es
Escenario: Una relación declarada como string no crea aristas en el grafo
  Dado que hermana-cecilia-torres.md declara related con el valor literal "[\"[[inquisicion]]\", \"[[guardianes-de-la-memoria]]\"]"
  Y que la regla pide related como lista YAML de wikilinks entre comillas
  Cuando Obsidian y la MCP construyen el grafo de relaciones
  Entonces tratan el campo como un único texto y no como dos enlaces
  Y los backlinks hacia inquisicion y guardianes-de-la-memoria no se generan
```