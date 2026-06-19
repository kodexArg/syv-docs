# Changelog

## [Unreleased]
- group: canon-meteorito-buenos-aires-2039
  priority: high
  commit: 3af3788
  changes:
    - feat(hitos): nuevo hito 2039-el-meteorito-de-buenos-aires.md — impacto canónico 4-abr-2039, cuerpo hielo puro ~50m, ~1 Megatón, cráter 800m, sin radioactividad
    - fix(cronologia): fecha correcta del Meteorito — 4-abr-2039 (no 2030-12-27); causación y energía documentadas; 1M + 5M muertes indirectas
    - fix(hitos): 2039-la-larga-noche.md — alineado con fecha 2039; estado canon añadido; prefijo escr removido; sección Cuerpo de Hielo incorporada
    - fix(hitos): 2031-la-fragmentacion-de-argentina.md — causación corregida a Nodo Sur (no meteorito); wikilink a [[2039-el-meteorito-de-buenos-aires]] agregado; estado canon reordenado
    - fix(hitos): 2034-a-cielo-abierto.md — fecha 2034 corregida de 2031; estado canon agregado
    - fix(sinopsis): sección renombrada a "El Colapso y la Fragmentación (2030-2039)"; causación alineada
    - fix(atlas): darsena.md — Historia refactorizado — separados eventos Nodo Sur (2030) y Cuerpo de Hielo (2039)
    - fix(atlas): universidad-pontificia-america.md — fecha impacto corregida a 2039

- group: canon-caridad-divina-erradicada-las-manos-calladas
  priority: high
  changes:
    - feat(facciones-menores): nueva secta clandestina [[las-manos-calladas|Las Manos Calladas]] (las-manos-calladas) — ex-miembros de la disuelta Congregación de la Caridad Divina, unidos por vínculos personales, sin jerarquía ni registros
    - refactor(canon): erradicar la Congregación de la Caridad Divina de raíz — purga de rastros en sinopsis, iglesia, exorcistas, arpistas y credos (hermandades, shipibo-conibo, guarani)
    - refactor(personajes): reasignar María, sor-nikole, sor-catalina, padre-alejandro-soria, hermana-laura-castillo a [[las-manos-calladas|Las Manos Calladas]]; red de vínculos personales tejida; carlos-gimenez como satélite periférico
    - refactor(diegesis): repuntar carta-a-sor-sofia y cursiva a [[las-manos-calladas|Las Manos Calladas]] respetando la voz epistolar
    - chore(canon): cero wikilinks colgantes a Congregación de la Caridad Divina en syv-docs (queda solo la referencia de origen histórico en la ficha de [[las-manos-calladas|Las Manos Calladas]])

- group: personajes-maria-unificada
  priority: high
  changes:
    - refactor(personajes): unificar las dos Marías en una sola ficha canónica (slug madre-superiora-maria) — biografía reconciliada (Congregación → dirección del Faro), 5 aliases; eliminada hermana-superior-maria.md
    - fix(personajes): repuntar backlinks al slug canónico — sor-nikole, hermana-laura-castillo, monseñor-miguel
    - fix(facciones): repuntar congregacion-caridad-divina.md y exorcistas.md a madre-superiora-maria
    - fix(sinopsis): repuntar referencia de María al slug canónico
    - feat(personajes): nueva ficha de Lisa (3_personajes/secundarios/lisa.md), nadadora de las Tuberías; enlazada desde walter-relato.md

- group: canon-anatema-mecanico-fecha-unificada
  priority: high
  commit: 902f766
  changes:
    - fix(cronologia): unificar fecha del Anatema Mecánico — 13-mar-2061 (+24h del Gran Silencio, Córdoba); eliminar variante errónea (+5 meses, 15-ago)
    - fix(codex): corregir siglo — "Constitución de 2161" → "2061" en anatema-mecanico.md
    - fix(facciones-menores): actualizar fecha en los-remanentes.md al canon 13-mar-2061
    - fix(codex): sincronizar qia-inteligencias-artificiales-cuanticas.md con fecha de Anatema Mecánico
    - fix(sinopsis): refrescar línea temporal del prólogo — Anatema Mecánico ahora 13-mar-2061

- group: canon-shipibo-conibo-intramuros-extramuros
  priority: normal
  commit: 7261f8c
  changes:
    - refactor(credos): Shipibo-Conibo — población refactorizada intramuros (censables, ~450) vs extramuros (incalculable); patrón Umbanda adoptado
    - refactor(facciones-menores): shipibo-conibo.md alineado con distribución intramuros/extramuros

- group: personajes-maria-aliases-desambiguacion
  priority: normal
  commit: 4128fa6
  changes:
    - refactor(personajes): madre-superiora-maria.md — refinados aliases para desambiguar de Hermana Superior María (secundaria)

- group: personajes-secundarios-grafo-wikilinks
  priority: normal
  commit: affd67a
  changes:
    - feat(personajes): 27 secundarios huérfanos — enganchados al grafo con wikilinks
    - refactor(indice): secundarios.md — listado de los 27 reparados + descripción breve de rol

- group: walter-relato-renombrado-elevado
  priority: normal
  commit: b4ae1d8
  changes:
    - refactor(relatos): walter.md → walter-relato.md — basename único, diferenciación de personaje Walter
    - feat(relatos): walter-relato.md elevado a versión mejorada del relato

- group: mocs-relatos-cronicas-cartas-cierre
  priority: normal
  commit: d6f7da7
  changes:
    - refactor(mocs): relatos.md, cronicas.md, cartas.md — agregado title + description + tags #entidad/guia
    - docs(structure): cerrados MOCs con [continuará...] — estructuras listas para expansión

- group: strip-framework-consolidate-cities
  priority: high
  commit: cad02ec
  changes:
    - refactor(frontmatter): eliminar TODOS los campos de framework legacy (sidebar, order, hidden, slug) de 31 archivos — corpus framework-agnóstico puro
    - refactor(structure): fusionar 4 index.md de ciudades (dársena, mendoza, san-luis, fuerte-san-martin) — prosa intro → epígrafe en <ciudad>.md
    - refactor(structure): renombrar index.md raíz → inicio.md — evitar patrón index.md de framework
    - chore(tooling): nuevo _tools/strip_framework.py (ruamel-based, reusa patrón migrate_metadata.py)
    - test(validation): verificación post-migración — 0 campos framework, 0 huérfanos de contenido real, 0 title: Index

- group: finalize-metadata-migration
  priority: high
  commit: pending
  changes:
    - chore(tooling): eliminar check_tags.py / remove_tags.py (scripts pre-taxonomía, reemplazados por _tools/migrate_metadata.py)
    - docs(guias): actualizar guía-de-metadatos.md — documentar eliminación de scripts obsoletos y referencia al migrador determinístico

- group: deterministic-metadata-migration
  priority: high
  commit: b2d4c05
  changes:
    - refactor(frontmatter): migración determinística de metadatos — eliminar ~24 tags legacy (trasfondo, atlas, geografia, religion, trasfondo/codex/*), normalizar folder en 14 index files, preservar campos de sitio legacy
    - refactor(relations): convertir anatema-mecanico tag → wikilink en related
    - feat(tooling): _tools/migrate_metadata.py (migrador ruamel-based determinístico, dry-run default, --apply para escribir; preserva quotes/indent, re-emite solo frontmatter)
    - test(tooling): 20 passing tests — idempotencia, preservación de cuerpo, validación YAML

- group: obsidian-anchor-metadata-rewrite
  priority: high
  commit: bd7b739
  changes:
    - docs(guias): reescribir guía de metadatos para paradigma Obsidian — taxonomía cerrada y wikilinks
    - docs(guias): alinear 5 guías hermanas (personajes, facciones, manual, plantillas, index)
    - chore(frontmatter): normalizar YAML y preservar campos de sitio legacy (sidebar, order, hidden, slug)

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
