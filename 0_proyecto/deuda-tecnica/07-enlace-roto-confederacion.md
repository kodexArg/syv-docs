---
description: 'El único enlace roto del corpus: un wikilink en cronologia.md que apunta
  a un fragmento de encabezado y resuelve a un destino vacío.'
folder: 0_proyecto/deuda-tecnica
related:
- '[[1_trasfondo/cronologia|Cronología]]'
- '[[0_proyecto/deuda-tecnica/deuda-tecnica|Deuda Técnica]]'
tags: []
title: DT-007 · Enlace roto en Cronología — «Confederación Argentina»
---

> [!success] RESUELTO · 2026-06-26
> Enlace de «Confederación Argentina» reparado como self-link de ruta completa con fragmento; `broken_link_count: 0` confirmado. Verificado. Traza abajo.

> [!info] Tarjeta de deuda técnica
> Tema: **único enlace roto** reportado por el índice (`broken_link_count: 1`).

### `ABIERTO` · DT-007 — «Confederación Argentina» apunta a un fragmento y resuelve a `.md` vacío
#deuda/enlace-roto
**Afecta:** [[1_trasfondo/cronologia|Cronología]]

```gherkin
# language: es
Escenario: Un wikilink a un encabezado resuelve a un destino inexistente
  Dado que cronologia.md contiene un enlace con texto "Confederación Argentina"
  Y que su destino crudo es el fragmento "#2161-2178: La Confederación Argentina"
  Cuando el índice resuelve ese wikilink
  Entonces el target_path queda como ".md" (vacío) y el enlace figura como roto
  Y debería apuntar a la nota o a la sección correcta de la propia Cronología (p. ej. [[1_trasfondo/cronologia#...]])
```