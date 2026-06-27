---
alcance: publico
aliases:
- Mapa de Dársena
- Mapa de Ciudad Dársena
description: 'Mapa interactivo de Ciudad Dársena sobre la geografía real de Buenos
  Aires. Lienzo base: el fondo real, listo para taparse con capas propias.'
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

> [!info] Lienzo base
> Mapa interactivo (plugin **Leaflet**) sobre la geografía **real** de Buenos Aires. Por ahora está **vacío**: solo el fondo real, sin marcadores ni polígonos. El plan es ir **tapando** ese fondo con capas propias (el muro, el agua, etiquetas renombradas) hasta convertirlo en Ciudad Dársena.
>
> `draw: true` queda activo: clic-derecho-shift para dibujar a mano.

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
draw: true
drawColor: #c1440e
```

## Referencia

- [[darsena|Ciudad Dársena]] — la ficha madre del atlas
- Mapa de impacto del [[2039-el-meteorito-de-buenos-aires|Cuerpo de Hielo]] (HTML standalone): `mapa_impacto_buenos_aires.html`