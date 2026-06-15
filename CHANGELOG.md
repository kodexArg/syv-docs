# Changelog

## [Unreleased]
- group: deterministic-metadata-migration
  priority: high
  commit: b2d4c05
  changes:
    - refactor(frontmatter): migración determinística de metadatos — eliminar ~24 tags legacy (trasfondo, atlas, geografia, religion, trasfondo/codex/*), normalizar folder en 14 index files, preservar campos Astro
    - refactor(relations): convertir anatema-mecanico tag → wikilink en related
    - feat(tooling): _tools/migrate_metadata.py (migrador ruamel-based determinístico, dry-run default, --apply para escribir; preserva quotes/indent, re-emite solo frontmatter)
    - test(tooling): 20 passing tests — idempotencia, preservación de cuerpo, validación YAML

- group: obsidian-anchor-metadata-rewrite
  priority: high
  commit: bd7b739
  changes:
    - docs(guias): reescribir guía de metadatos para paradigma Obsidian — taxonomía cerrada y wikilinks
    - docs(guias): alinear 5 guías hermanas (personajes, facciones, manual, plantillas, index)
    - chore(frontmatter): normalizar YAML y preservar campos Astro (sidebar, order, hidden, slug)

- group: obsidian-migration-complete
  priority: high
  commit: 96be17d
  changes:
    - refactor(tags): migrar 158 .md — tags organizacionales → taxonomía cerrada (#entidad/, #alcance/, #estado/)
    - refactor(wikilinks): convertir 148 cross-refs legacy (../x.md, @path, display-names) → wikilinks en cuerpo y frontmatter
    - refactor(aliases): añadir aliases en toda entidad con nombre propio — proteger contra renombres
    - refactor(spoilers): reemplazar alerta-spoiler* (legacy) → campo spoilers + tag #alcance/secreto
    - feat(ubicaciones): crear 8 fichas-stub (#estado/propuesta) — cementerio-de-chacarita, torres-hidroponicas, academia-de-ciencias-de-darsena, bazar-del-muro, aduana-nacional, mercado-de-antigua-estacion, jardines-del-norte, basilica-de-san-pedro
    - feat(facciones): crear 8 fichas-stub (#estado/propuesta) — direccion-nacional-de-seguridad, rtu, seguridad-urbana, curatores, curia-romana, alto-clero, archivistas-y-cientificos-teologicos, sanidad
    - chore(validation): verificación adversarial (orch-critic) — 0 wikilinks colgados reales, YAML válido, correlación spoilers↔#alcance/secreto, 0 huérfanos reales
