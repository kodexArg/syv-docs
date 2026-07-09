---
alcance: publico
aliases:
- Leyenda del Mapa de Dársena
- Mapa de Dársena
- Colores del Mapa de Dársena
- Findings del Mapa
description: 'Findings del mapa interactivo de Ciudad Dársena y alrededores: regiones,
  color canónico, superficie en km², población y densidad por zona.'
entidad: guia
estado: propuesta
folder: 2_atlas/ciudades/darsena
related:
- '[[barrios-del-muro]]'
- '[[zona-centro]]'
- '[[microcentro]]'
- '[[zona-militar-eclesiastica]]'
- '[[basilica-de-san-pedro]]'
- '[[santa-sede]]'
- '[[barrio-de-la-armada]]'
- '[[barrio-de-los-pescadores]]'
- '[[zona-residencial-alta-sociedad]]'
- '[[fuerzas-armadas]]'
- '[[fuera-del-muro]]'
- '[[franja-de-alsina]]'
- '[[tuberias]]'
tags: []
title: Leyenda del Mapa de Dársena
ubicaciones:
- '[[darsena]]'
---

# Leyenda del Mapa de Dársena

Findings del mapa interactivo de [[darsena|Ciudad Dársena]] **y sus alrededores**: cada polígono con su **color canónico**, su **superficie**, y —donde aplica— su **población** y **densidad**. Áreas geodésicas (proyección equirectangular sobre latitud media; error < 1 % a escala urbana) medidas sobre la geometría del mapa.

> [!info] Procedencia y estado
> Derivada de la herramienta `syv-map` (sandbox de polígonos MapLibre, coordenadas WGS84 reales sobre el área de la antigua dársena porteña). Geometría **en construcción**: las superficies son las actuales y pueden moverse al ajustar bordes. Los **colores se mantienen** como paleta de referencia. La **población** deriva del ancla canónica de 12 500 000 de almas reales en la ciudad (censo oficial del Estado: 5 000 000 — ver el desdoble en [[darsena]]) repartida por densidad; es modelo `propuesta`, no cifra ratificada por zona.

<!-- syv-map: esta leyenda debe poder ocultarse/mostrarse con un botón toggle en el mapa interactivo (pendiente en la app, no en este documento). -->

## Regiones de la ciudad — superficie, población y densidad

Reparto de los **12 500 000 de almas** reales de Dársena (el censo oficial del Estado declara **5 000 000**; ver el desdoble en [[darsena]]). Ancla dura: los [[barrios-del-muro|Barrios del Muro]] concentran el **75 % (9,375 M)**; el gradiente va de la humedad podrida a los jardines secos.

| Región (rótulo del mapa) | Color | km² | Población | % ciudad | hab/km² | Entidad canónica |
|---|---|---:|---:|---:|---:|---|
| Barrios del Muro | `#080808` | 5.73 | 9 375 000 | 75 % | 1 635 000 | [[barrios-del-muro]] |
| Centro de Dársena | `#FF6A1A` | 4.74 | 2 900 000 | 23,2 % | 611 500 | [[zona-centro]] · núcleo [[microcentro]] |
| Barrio de la Armada | `#71f9ac` | 1.36 | 200 000 | 1,6 % | 147 300 | [[barrio-de-la-armada]] |
| Barrio de Pescadores | `#32287b` | 1.01 | 16 000 | 0,13 % | 15 800 | [[barrio-de-los-pescadores]] (Gremio de Pesca) |
| Barrio Norte *(élite)* | `#74ACDF` | 0.48 | 6 600 | 0,05 % | 13 850 | [[zona-residencial-alta-sociedad\|Barrios del Norte]] |
| Santa Sede | `#f2ff42` | 3.35 | 882 | 0,007 % | 263 | [[santa-sede]] ([[zona-militar-eclesiastica\|Isla Oriental]]) · [[basilica-de-san-pedro]] |
| Zona Militar Norte | `ForestGreen` | 0.68 | 100 | ~0 % | 147 | guarnición urbana de [[fuerzas-armadas]] — *sin ficha propia* |
| Muralla | `DarkBlue` | *línea* | — | — | — | el muro perimetral (Muro Norte / Sur / de Barrio Norte) |
| **Total ciudad** | | **~17.35** | **12 500 000** | 100 % | | |

> Las [[tuberias|Tuberías]] (~500 000, subsuelo) son un **subconjunto** de los Barrios del Muro —población off-censo que no suma aparte—. Sobre el río, ~10 000 almas viven a bordo de la flota (~1000 barcos de la clase «Dársena»), fuera del reparto de superficie.

## Alrededores — las zonas exteriores

Los polígonos de afuera del muro son **órdenes de magnitud más grandes** que los distritos urbanos y de población permanente **~0** (Salvajes dispersos, barcazas, refugiados de paso). No entran en el reparto de los 12,5 M de la ciudad. (El **territorio** administrado por Dársena suma ~15 M si se cuentan los Campos de Reeducación del norte y el ejército de tierra del cinturón — ver [[darsena]].)

| Zona | Color | km² | Ubicación | Población | Entidad canónica |
|---|---|---:|---|---:|---|
| **ZDM** | `#bbe8be` | 279.5 | oeste, sobre Las Ruinas (~10 km del centro) | ~0 | la **DMZ** de [[fuera-del-muro]] — *nombre por ratificar* |
| **El Pantano** | `#dafbeb` | 216.9 | sur ahogado (~13,5 km al S) | ~0 | Los Pantanos de [[fuera-del-muro]] |
| **Lago Muerto** | `#42f2ff` | 9.63 | ~14 km al NO, en el cráter | 0 | el lago del [[2039-el-meteorito-de-buenos-aires\|cráter del meteorito]] |

- **ZDM** — cinturón occidental de escombros que la ciudad mantiene despejado *a base de plomo*: todo lo que se mueve sin autorización —hombre, vehículo o animal— es abatido por los francotiradores del muro. Geográficamente **es la DMZ canónica** (el borde de Las Ruinas que rodea el cráter). Falta fijar qué significa la sigla y si reemplaza o convive con «DMZ».
- **El Pantano** — la *Venecia de la podredumbre* al sur: edificios sumergidos hasta el segundo piso, agua tóxica, niebla con visibilidad < 5 m. Ya es canon en [[fuera-del-muro]] (allí «Los Pantanos», nombrado en singular «El Pantano»); el mapa le da por fin superficie de referencia. Antecede a la zona muerta de la [[franja-de-alsina]] más al sur.
- **Lago Muerto** — el agua que llenó el cráter del [[2039-el-meteorito-de-buenos-aires|Cuerpo de Hielo]]. Tenido por maldito y tabú; solo su orilla este está habitada, en **El Paso del Cráter**, donde la [[fuerzas-armadas|Armada]] asienta base y le da la espalda al lago. En canon existía sin nombre («la herida que se volvió agua»); acá se lo bautiza.

## El impacto — grupo de contexto (no es una región)

El **Cuerpo de Hielo (2039)** se dibuja como cinco anillos concéntricos, un grupo toggleable aparte (apagado por defecto). Centro en el cráter, ~14 km al NO. Radios de efecto: **35 km** (verde) · **14 km** (amarillo) · **6,4 km** (naranja) · **1,4 km** (rojo) · **cráter 800 m** (negro). Ver [[2039-el-meteorito-de-buenos-aires]].

## Modelo de población y densidad

- **Ancla canónica:** 12 500 000 de almas reales en la ciudad ([[darsena]]) —frente al censo oficial de 5 000 000—; los [[barrios-del-muro|Barrios del Muro]] (5,73 km²) sostienen el **75 % = 9,375 M** a **~1 635 000 hab/km²**.
- **¿Es habitable esa densidad?** Sí: es el corazón mismo del universo, un *warren vertical* llevado al extremo. El promedio del Muro (~1,635 M/km²) **iguala y supera** el récord histórico de hacinamiento humano —Kowloon Walled City, ~1,255 M/km²— pero sostenido no sobre una manzana sino sobre **220 veces** esa superficie. El gradiente interno lo explica: el **sur del Muro** trepa a **~4 M/km²** (monobloques de hasta 100 pisos, mediana 40–50), mientras la **franja pegada al muro**, capada a los 20 m de altura del propio muro, baja a **~1 M/km²**. No es realismo de conventillo: es una colmena vertical extrema, coherente con una ciudad que niega su propio tamaño.
- **El cuello de botella no es el espacio sino el servicio** (agua, cloaca, aire): coherente con la mortalidad canónica (tuberculosis 40 %, micosis 45 %, esperanza de vida 42–45).

## Notas de lectura y reconciliación

- La **Muralla** no aporta superficie: sus trazos son líneas (`fill: false`).
- La **suma cruda** de la ciudad (~17.35 km²) es su huella real: los polígonos urbanos **no** se solapan. Sumando los alrededores, el mundo mapeado ronda **~523 km²**.
- **Prosa reconciliada:** los Barrios del Muro miden **5,73 km²** en el mapa, en línea con los *«cinco kilómetros cuadrados»* de [[barrios-del-muro]] (la nota de reconciliación prosa/mapa antes pendiente queda **resuelta**). Sobre esa superficie, el ancla real de 9,375 M da **~1 635 000 hab/km²**.
- **Sin ficha propia todavía:** Zona Militar Norte y las tres zonas exteriores (ZDM, El Pantano como entrada dedicada, Lago Muerto). El mapa las delimita antes de su entrada canónica.