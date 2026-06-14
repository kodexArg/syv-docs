# Changelog

## [Unreleased]
- group: obsidian-anchor-metadata-rewrite
  priority: high
  commit: pending
  changes:
    - docs(guias): reescribir guía de metadatos para paradigma Obsidian — taxonomía cerrada y wikilinks
    - docs(guias): alinear 5 guías hermanas (personajes, facciones, manual, plantillas, index)
    - chore(frontmatter): normalizar YAML y preservar campos Astro (sidebar, order, hidden, slug)

- group: obsidian-migration-158-files
  priority: high
  commit: pending
  changes:
    - refactor(tags): migrar 158 .md — tags organizacionales → taxonomía cerrada (#entidad/, #alcance/, #estado/)
    - refactor(wikilinks): convertir 148 cross-refs legacy (../x.md, @path, display-names) → wikilinks en cuerpo y frontmatter
    - refactor(aliases): añadir aliases en toda entidad con nombre propio — proteger contra renombres
    - refactor(spoilers): reemplazar alerta-spoiler* (legacy) → campo spoilers + tag #alcance/secreto

- group: obsidian-new-entities-16-stubs
  priority: normal
  commit: pending
  changes:
    - feat(ubicaciones): crear 8 fichas-stub (#estado/propuesta) — cementerio-de-chacarita, torres-hidroponicas, academia-de-ciencias-de-darsena, bazar-del-muro, aduana-nacional, mercado-de-antigua-estacion, jardines-del-norte, basilica-de-san-pedro
    - feat(facciones): crear 8 fichas-stub (#estado/propuesta) — direccion-nacional-de-seguridad, rtu, seguridad-urbana, curatores, curia-romana, alto-clero, archivistas-y-cientificos-teologicos, sanidad
    - refactor(reconexion): vincular menciones texto-plano con wikilinks en 16 entidades nuevas

- group: obsidian-verification-converged
  priority: normal
  commit: pending
  changes:
    - chore(validation): verificación adversarial (orch-critic) — 0 wikilinks colgados reales, YAML válido, correlación spoilers↔#alcance/secreto, 0 huérfanos reales
    - docs(migration): documentar pendientes de revisión de canon en .migration/PENDIENTES-REVISION.md (fuera de repo)
