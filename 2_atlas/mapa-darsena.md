---
alcance: publico
aliases:
- Mapa de Dársena
- Mapa de Ciudad Dársena
description: Mapa interactivo de Ciudad Dársena sobre la geografía real de Buenos
  Aires, con el nivel del mar elevado tras el Colapso. Marcadores enlazados a las
  fichas del atlas.
entidad: guia
estado: borrador
folder: 2_atlas
related:
- '[[darsena]]'
tags: []
title: Mapa de Ciudad Dársena
ubicaciones:
- '[[darsena]]'
---

> [!info] Cómo usar este mapa
> Mapa interactivo (plugin **Leaflet**) sobre la geografía **real** de Buenos Aires. La capa de agua representa el **nivel del mar elevado** tras el Colapso: anega Puerto Madero, la Costanera y toda la franja ganada al río, dejando la barranca natural (Paseo Colón / L. N. Alem) como nueva línea de costa.
>
> **Editar es editar números.** Cada marcador es una línea `marker: tipo, lat, long, [[ficha]]`. Para mover un punto, cambiá sus coordenadas. La costa/inundación vive aparte en `darsena-inundacion.geojson`. Con `draw: true` podés dibujar a mano por encima (clic-derecho-shift para overlays).

```leaflet
id: mapa-darsena
lat: -34.6050
long: -58.3760
defaultZoom: 14
minZoom: 12
maxZoom: 18
height: 640px
width: 100%
tileServer: https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png|Voyager
tileSubdomains: a,b,c,d
geojson: [[darsena-inundacion.geojson]]
geojsonColor: #1f6f8b
draw: true
drawColor: #c1440e
marker: default, -34.6050, -58.3760, [[microcentro|Microcentro]], Corazón administrativo y comercial
marker: default, -34.6080, -58.3700, [[zona-centro|Zona Centro]], Núcleo productivo y educativo
marker: default, -34.6110, -58.3620, [[zona-militar-eclesiastica|Isla Oriental]], Poder militar y eclesiástico — al este de la dársena vieja
marker: default, -34.6090, -58.3610, [[basilica-de-san-pedro|Basílica de San Pedro]], Reconstruida piedra por piedra desde el Vaticano
marker: default, -34.5880, -58.3920, [[zona-residencial-alta-sociedad|Barrios del Norte]], Oasis amurallado de la élite
marker: default, -34.6060, -58.3790, [[tuberias|Las Tuberías]], La ciudad subterránea bajo el Microcentro
marker: default, -34.6150, -58.4080, [[barrios-del-muro|Barrios del Muro]], Distritos hacinados contra la muralla de 20 m
```

## Sobre la geografía

Ciudad Dársena se levanta sobre las ruinas de Buenos Aires. El mapa usa coordenadas reales: lo que hoy es **Puerto Madero** es la [[zona-militar-eclesiastica|Isla Oriental]], separada del resto por la **dársena vieja** (el canal), y la antigua barranca de la costa —que en el Buenos Aires real corría por Paseo Colón y Leandro N. Alem— se vuelve, con el mar elevado, la nueva orilla de la ciudad.

La capa de inundación es un punto de partida **autoral apoyado en cotas reales** (híbrido): la dibujamos a criterio, pero respetando dónde el terreno real es bajo (relleno ganado al río) y dónde sube la barranca. Se ajusta editando `darsena-inundacion.geojson`.

## Referencia

- [[darsena|Ciudad Dársena]] — la ficha madre del atlas
- Mapa de impacto del [[2039-el-meteorito-de-buenos-aires|Cuerpo de Hielo]] (HTML standalone): `mapa_impacto_buenos_aires.html`