# Crear Diégesis: Guía Rápida

## ¿Qué es?

Un skill que transforma tu contexto narrativo en una historia canónica de Subordinación y Valor, escrita párrafo a párrafo contigo.

## Uso

```bash
/crear-diegesis [opcional: tu contexto narrativo]
```

### Sin contexto → Te muestra la ayuda
```
/crear-diegesis
```

### Con contexto → Inicia el flujo
```
/crear-diegesis Un perro encuentra una llave en el Microcentro abandonado.
```

---

## Flujo Rápido

### FASE 1: Clarificación (5–10 min)
1. **Título**: Te sugiero 3, tú eliges o escribes uno
2. **Tipo**: ¿Cuento corto, artículo worldbuilding o historia abierta?
3. **Preguntas**: Entiendo tu intención exacta
4. **Validación**: Verifico coherencia con canon SyV
5. **Guardado**: Creo `[titulo]-canon.md`

### FASE 2: Escritura (Sin límites)
1. **Contexto limpio**: Opus 4.6 + tus herramientas canónicas
2. **Escritura iterativa**: Párrafo a párrafo, tú controlas todo
3. **Archivo vivo**: `[titulo].md` se actualiza contigo
4. **Sin imposiciones**: Pausa, retrocede, ajusta estilo, expande, lo que quieras

---

## Tipos de Historias

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Cuento Corto** | Narrativa cerrada (1–5k palabras) | "El Perro Que Escucha" |
| **Artículo Diégesis** | Worldbuilding, contexto, atmósfera | "La Historia de la Nueva Basílica" |
| **Historia Progresiva** | Abierta, apta para rol, divergencias | "Preludio en la Basílica" (campaña) |

---

## Ejemplos Rápidos

### Cuento Corto
```
/crear-diegesis Un técnico de la Guardia descubre que los cables de la Basílica hablan entre sí.
```
→ Crear historia cerrada, introspectiva, ~3000 palabras

### Worldbuilding
```
/crear-diegesis Quiero escribir sobre cómo era Buenos Aires justo antes del Colapso del Microcentro.
```
→ Artículo atmosférico, contexto histórico, ambientación

### Rol Progresivo
```
/crear-diegesis El jugador es un sacerdote recién ordenado. Descubre una herejía en los archivos de la Basílica. Quiero que sea abierta, sin final fijo.
```
→ Escena inicial, múltiples caminos, continúa según decisiones

---

## Controles en FASE 2

Una vez escribiendo, tú eres el editor. Usa estos comandos:

```
"Continúa"                    → Siguiente párrafo
"Retrocede a [párrafo X]"     → Vuelve a ese punto, escribe diferente
"No tan literario"            → Ajusta estilo (más directo)
"Más atmósfera"               → Ajusta estilo (más sensorial)
"Escribe antes de..."         → Inserta escena anterior
"Pausamos aquí"               → Guarda progreso, termina sesión
"Valida coherencia"           → Verifica contra canon
"Explica este párrafo"        → Metacomentario
[Cualquier dirección]         → Tú controlas
```

---

## Archivos Generados

### Después de FASE 1
```
[titulo]-canon.md
├── title: "[Tu Título]"
├── type: "[Tipo de Historia]"
├── context: "[Tu contexto original]"
├── validations: [✓ Cronología, Facciones, etc.]
└── notes: "[Notas de coherencia]"
```

### Durante FASE 2
```
[titulo].md
├── Narrative content actualizado iterativamente
├── Preserva tu voz exacta
└── Validado contra Canon SyV
```

---

## Principios Clave

✓ **Tu voz es sagrada**: No improviso, no extrapolé. Tu contexto es exacto.
✓ **Canónico pero vivo**: Valido contra todos los sistemas SyV sin rigidez.
✓ **Iterativo, no lineal**: Pausas, retrocesos, direcciones abiertas. Sin imposiciones.
✓ **Sin límites predeterminados**: La historia dura lo que tú quieras.

---

## Archivos de Referencia

| Archivo | Contenido |
|---------|-----------|
| **SKILL.md** | Definición completa, arquitectura, normas |
| **EJEMPLOS.md** | 3 flujos completos (Cuento, Rol, Worldbuilding) |
| **IMPLEMENTACION.md** | Detalles técnicos, subagentes, transiciones |
| **README.md** | Este archivo (referencia rápida) |

---

## Empezar Ahora

```
/crear-diegesis Tu contexto de historia aquí
```

O si no tienes uno:

```
/crear-diegesis
```

(Se abre la ayuda)

---

**Versión**: 1.0.0
**Status**: Listo para usar
**Últimas opciones**: Cuento Corto, Worldbuilding, Historia Progresiva (Rol)
