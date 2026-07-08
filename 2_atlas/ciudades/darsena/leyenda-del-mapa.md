---
alcance: publico
aliases:
- Leyenda del Mapa de Dársena
- Mapa de Dársena
- Colores del Mapa de Dársena
description: 'Leyenda del mapa interactivo de Ciudad Dársena: regiones, color canónico
  y superficie geodésica en km² de cada polígono.'
entidad: guia
estado: propuesta
folder: 2_atlas/ciudades/darsena
related:
- '[[barrios-del-muro]]'
- '[[zona-centro]]'
- '[[microcentro]]'
- '[[zona-militar-eclesiastica]]'
- '[[basilica-de-san-pedro]]'
- '[[bajo-pulmon]]'
- '[[barrio-de-los-pescadores]]'
- '[[zona-residencial-alta-sociedad]]'
- '[[fuerzas-armadas]]'
tags: []
title: Leyenda del Mapa de Dársena
ubicaciones:
- '[[darsena]]'
---

# Leyenda del Mapa de Dársena

Correspondencia entre las regiones del mapa interactivo de [[darsena|Ciudad Dársena]], su **color canónico** y su **superficie**. Las áreas son geodésicas (proyección equirectangular sobre la latitud media de la isla; error < 1 % a escala urbana), calculadas sobre la geometría de los polígonos del mapa.

> [!info] Procedencia y estado
> Derivada de la herramienta `syv-map` (sandbox de polígonos MapLibre, coordenadas WGS84 reales sobre el área de la antigua dársena porteña). Geometría **en construcción**: las superficies son las actuales y pueden moverse al ajustar bordes. Los **colores se consideran mantenibles** como paleta de referencia del mapa. Marcada `propuesta` hasta ratificación de canon.

## Regiones

| Región (rótulo del mapa) | Color | Superficie | Entidad canónica |
|---|---|---:|---|
| Barrios del Muro | `#080808` | **8.27 km²** | [[barrios-del-muro]] |
| Centro de Dársena | `#FF6A1A` | **7.02 km²** | [[zona-centro]] · núcleo [[microcentro]] |
| Zona Roja | `#641b1b` | **3.65 km²** | *sin ficha propia — candidata a canon* |
| Santa Sede | `#f2ff42` | **3.33 km²** | [[zona-militar-eclesiastica\|Isla Oriental]] · sede [[basilica-de-san-pedro]] |
| Barrio de la Armada | `#71f9ac` | **1.43 km²** | parte de [[bajo-pulmon]] — *sin ficha propia* |
| Barrio Norte | `#74ACDF` | **1.11 km²** | [[zona-residencial-alta-sociedad\|Barrios del Norte]] |
| Barrio de los Pescadores | `#7a591f` | **0.99 km²** | [[barrio-de-los-pescadores]] |
| Zona Militar Norte | `ForestGreen` | **0.86 km²** | guarnición de [[fuerzas-armadas]] — *sin ficha propia* |
| Muralla | `DarkBlue` | *línea (sin área)* | el muro perimetral: Muro Norte, Muro Sur, Muro de Barrio Norte |

## Notas de lectura

- La **Muralla** no aporta superficie: sus trazos son líneas (`fill: false`), no polígonos rellenos. Miden extensión, no área.
- La **suma cruda** de las regiones (~26.7 km²) **no** es la huella real de la ciudad: los polígonos se solapan (barrios y distritos cayendo dentro del Centro o de los Barrios del Muro). La superficie efectiva requiere una unión geométrica, aún no calculada.
- *Santa Sede* es el rótulo de trabajo del mapa para el asiento eclesiástico; en el canon corresponde a la [[zona-militar-eclesiastica|Isla Oriental]] y su [[basilica-de-san-pedro|Basílica-Fortaleza]].
- Tres regiones (**Zona Roja**, **Barrio de la Armada**, **Zona Militar Norte**) todavía no tienen ficha propia en el Atlas; el mapa las delimita antes de que exista su entrada canónica.