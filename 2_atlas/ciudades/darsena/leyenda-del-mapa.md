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
> Derivada de la herramienta `syv-map` (sandbox de polígonos MapLibre, coordenadas WGS84 reales sobre el área de la antigua dársena porteña). Geometría **en construcción**: las superficies son las actuales y pueden moverse al ajustar bordes. Los **colores se mantienen** como paleta de referencia. La **población** deriva del ancla canónica de 5 000 000 de almas (ver [[darsena]]) repartida por densidad; es modelo `propuesta`, no cifra ratificada por zona.

## Regiones de la ciudad — superficie, población y densidad

Reparto de los **5 000 000 de almas** canónicos de Dársena. Ancla dura: el complejo del Muro concentra el **70 % (3,5 M)**; el gradiente va de la humedad podrida a los jardines secos.

| Región (rótulo del mapa) | Color | km² | Población | % ciudad | hab/km² | Entidad canónica |
|---|---|---:|---:|---:|---:|---|
| Zona Roja *(la más densa)* | `#641b1b` | 3.65 | 1 400 000 | 28 % | 383 000 | núcleo comprimido de [[barrios-del-muro]] — *sin ficha propia* |
| Barrios del Muro | `#080808` | 8.27 | 2 100 000 | 42 % | 254 000 | [[barrios-del-muro]] |
| Centro de Dársena | `#FF6A1A` | 7.02 | 980 000 | 19,6 % | 140 000 | [[zona-centro]] · núcleo [[microcentro]] |
| Barrio de Pescadores | `#32287b` | 0.99 | 170 000 | 3,4 % | 173 000 | [[barrio-de-los-pescadores]] (Gremio de Pesca) |
| Santa Sede | `#f2ff42` | 3.33 | 160 000 | 3,2 % | 48 000 | [[santa-sede]] ([[zona-militar-eclesiastica\|Isla Oriental]]) · [[basilica-de-san-pedro]] |
| Barrio de la Armada | `#71f9ac` | 1.43 | 110 000 | 2,2 % | 77 000 | [[barrio-de-la-armada]] |
| Zona Militar Norte | `ForestGreen` | 0.86 | 50 000 | 1,0 % | 58 000 | guarnición de [[fuerzas-armadas]] — *sin ficha propia* |
| Barrio Norte *(élite)* | `#74ACDF` | 1.11 | 30 000 | 0,6 % | 27 000 | [[zona-residencial-alta-sociedad\|Barrios del Norte]] |
| Muralla | `DarkBlue` | *línea* | — | — | — | el muro perimetral (Muro Norte / Sur / de Barrio Norte) |
| **Total ciudad** | | **~26.6** | **5 000 000** | 100 % | | |

## Alrededores — las zonas exteriores

Los polígonos de afuera del muro son **órdenes de magnitud más grandes** que los distritos urbanos y de población permanente **~0** (Salvajes dispersos, barcazas, refugiados de paso). No entran en el reparto de los 5 M.

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

- **Ancla canónica:** 5 000 000 de almas ([[darsena]]); el complejo del Muro (Zona Roja + Barrios del Muro = 11,9 km²) sostiene el **70 % = 3,5 M**, con Zona Roja como el punto más denso.
- **¿Es habitable esa densidad?** Sí, pero solo como *warren vertical* tipo Kowloon. Medido en **habitación neta por persona** (descontando muros, escaleras y usos no residenciales), a **6–8 pisos** de altura media Zona Roja da **~5–7 m²/persona** — nivel conventillo/Kowloon: escuálido pero históricamente real, y aún **~1/5 del récord** de hacinamiento humano (Kowloon Walled City, ~3,7 m²/p). A baja altura (2–3 pisos) cae por debajo del mínimo de un campo de refugiados: el canon **obliga** a que el Muro sea vertical.
- **El cuello de botella no es el espacio sino el servicio** (agua, cloaca, aire): coherente con la mortalidad canónica (tuberculosis 40 %, micosis 45 %, esperanza de vida 42–45).

## Notas de lectura y reconciliación

- La **Muralla** no aporta superficie: sus trazos son líneas (`fill: false`).
- La **suma cruda** de la ciudad (~26.7 km²) ≈ su huella real (unión 26.6 km²): los polígonos urbanos **no** se solapan (Zona Roja está dibujada *adyacente* a Barrios del Muro, no anidada). Sumando los alrededores, el mundo mapeado ronda **~530 km²**.
- **Tensión con la prosa:** el complejo del Muro mide 11,9 km² en el mapa contra los *«cinco kilómetros cuadrados»* de [[barrios-del-muro]]. Se respetó el ancla de 3,5 M sobre el área del mapa → densidad ~294 k/km² (la mitad de brutal que los ~700 k/km² que implicaría la prosa). Pendiente: reconciliar el polígono o la prosa.
- **Sin ficha propia todavía:** Zona Roja, Zona Militar Norte, y las tres zonas exteriores (ZDM, El Pantano como entrada dedicada, Lago Muerto). El mapa las delimita antes de su entrada canónica.