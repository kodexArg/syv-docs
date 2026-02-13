# Ejemplos de Uso: /crear-diegesis

## Ejemplo 1: Sin Contexto (Help)

```
USER:
/crear-diegesis

ASSISTANT RESPONSE:
# /crear-diegesis: Creador de Diégesis

Este comando convierte tu contexto narrativo en una historia canónica de Subordinación y Valor.

## Cómo funciona:

**1. FASE 1 - Clarificación**
- Sugeriremos títulos (o propones el tuyo)
- Preguntaremos qué tipo de historia es
- Haremos preguntas para entender tu intención exacta
- Validaremos coherencia con el canon
- Guardaremos referencia en [title]-canon.md

**2. FASE 2 - Escritura**
- Limpiaremos el contexto y pasaremos a Opus 4.6
- Escribiremos tu historia párrafo a párrafo contigo
- Tú controlas el ritmo, dirección y ajustes
- Sin límites predeterminados: el usuario manda

## Ejemplos de Invocación:

### Con contexto (comienza FASE 1):
/crear-diegesis Un perro encuentra una llave en ruinas del Microcentro. La llave abre algo que debería estar olvidado.

### Tipos de historias soportadas:
- **Cuento Corto**: Narrativa cerrada (1–5k palabras)
- **Artículo de Diégesis**: Worldbuilding, contexto, ambientación
- **Historia Progresiva**: Narrativa abierta, apta para rol y decisiones del jugador

## Ejemplos en el canon:
- "la-casa-negra-canon.md" → cuento corto ambientado en barrio sur
- "el-perro-canon.md" → historia progresiva con rol-play
- "preludio-canon.md" → artículo de diégesis sobre la Basílica

¿Quieres crear tu propia historia? Usa:
/crear-diegesis [tu contexto aquí]
```

---

## Ejemplo 2: Cuento Corto - "El Perro de Dársena"

```
USER:
/crear-diegesis Un perro vive en las ruinas del Microcentro. Come cables, escucha voces eléctricas. Un día encuentra una llave verde en la basura. No sabe qué abre.

ASSISTANT (PHASE 1):

## CLARIFICACIÓN: "El Perro de Dársena"

Perfecto. Tengo tu contexto. Aquí van las opciones de título:

1. **El Perro de Dársena**
2. **La Llave Verde**
3. **Voces Eléctricas**

¿Cuál te gusta o prefieres escribir otro?

---

USER:
Me gusta "El Perro de Dársena", pero podrías hacerlo "El Perro Que Escucha"

ASSISTANT:
Excelente. Título confirmado: **"El Perro Que Escucha"**

Ahora, ¿qué tipo de historia es?

- **A) Cuento Corto**: Historia cerrada sobre este perro y la llave (finaliza con resolución)
- **B) Artículo de Diégesis**: Entrada worldbuilding sobre los perros mutados del Microcentro
- **C) Historia Progresiva**: El perro es vehículo narrativo; abierta a decisiones/expansión

---

USER:
Cuento corto. Quiero que tenga tensión. El perro entiende más de lo que debería.

ASSISTANT:
Entendido. Cuento corto, perro inteligente, tensión narrativa.

Dos preguntas rápidas:
1. **¿En qué año de la cronología?** (¿cercano al Colapso del Microcentro, o décadas después?)
2. **¿La llave abre algo específico, o el misterio es el punto central?** (No necesitas revelarlo, solo saber si hay pista o no)

---

USER:
Año 2165, 50 años después del Colapso. La llave no abre nada... o eso cree el perro. Luego descubre que abre algo dentro de él.

ASSISTANT (VALIDACIÓN):
Esperando validación de canon... [Invoca subagentes]

✓ **Cronología**: 2165 es coherente (post-Colapso bien establecido)
✓ **Ubicación**: Microcentro abandonado existe en canon
✓ **Tema**: Mutación inteligente es canon SyV
✓ **Estilo**: Apto para Canon de Estilo (metáfora biopunk, elipsis emocional)

---

Contexto clarificado:

**Archivo guardado**: `el-perro-que-escucha-canon.md`

Contenido:
- Título: "El Perro Que Escucha"
- Tipo: Cuento Corto
- POV: Perro (inteligencia aumentada)
- Año: 2165
- Conflicto: Identidad/transformación (llave interna)
- Tono: Tensión, ambigüedad, final abierto

---

## INICIANDO FASE 2

Cambiando a contexto limpio Opus 4.6...

[Contexto limpio. Solo tengo el -canon.md y tus skills de estilo/validación]

---

Comenzaré a escribir **"el-perro-que-escucha.md"** contigo.

Contexto validado:
- **POV**: Perro (inteligencia aumentada, percepción sensorial)
- **Período**: 2165 (50 años post-Colapso Microcentro)
- **Conflicto Central**: La llave no abre puerta. Abre algo dentro de él.
- **Tono**: Tensión, misterio, final ambiguo

**Primer párrafo:**

---

El *fierro* quemaba contra las patas. (3)
Las voces eléctricas aullaban en las Túberías, como siempre al atardecer. (11)
El perro ya no era perro—hacía años que el Colapso le había reescrito cada neurona, cada conexión de la médula.
El olor de la llave verde fue lo primero. Óxido de cobre, plástico endurecido, y algo más—un olor a promesa. (20)

---

¿Te gusta la dirección? ¿Quieres que continúe, que retroeda, que ajuste el tono?

---

USER:
Bien, pero siente como si fuera "demasiado literario". Mantén la tensión pero más directo.

ASSISTANT:
Entendido. Voy a lo directo, sin tanto adorno. Reescribiendo:

---

El fierro quemaba contra las patas. Las voces eléctricas aullaban en las Túberías.
El Colapso lo había reescrito hacía años. Ya no era perro.
La llave verde olía a cobre y promesa.

---

¿Mejor así?

---

[La escritura continúa iterativamente hasta que el usuario la da por terminada. Sin límites, sin imposiciones de estructura. El usuario manda el ritmo.]
```

---

## Ejemplo 3: Historia Progresiva - "Preludio en la Basílica"

```
USER:
/crear-diegesis Quiero armar una campaña de rol donde el jugador es un técnico recién iniciado. Descubre que los servidores principales no son lo que parecen. Hay algo guardado ahí. Quiero que sea abierta, que el jugador pueda divergir.

ASSISTANT (PHASE 1):

## CLARIFICACIÓN: Historia Progresiva

Tus opciones de título:
1. **Preludio en la Basílica**
2. **El Técnico de Ábside**
3. **Liturgia Herética**

¿Cuál prefieres?

---

USER:
"Preludio en la Basílica" me late.

ASSISTANT:
Confirmado: **Preludio en la Basílica**

Preguntas rápidas:
1. **¿Cuál es el "algo guardado"?** (No necesita ser revelado aún, pero ¿lo sabes tú? ¿Lo saben los NPCs? ¿Es misterio genuino?)
2. **¿Jugador único o grupo?** (Afecta cómo escribo las opciones)
3. **¿El técnico es leal a la Basílica al inicio, o desconfiado?**

---

USER:
Lo guardado es un fragmento de IA pre-Colapso. El jugador no lo sabe. Grupo de 3-4 jugadores. El técnico es leal pero curioso.

ASSISTANT (VALIDACIÓN):
✓ Cronología: Pre-Colapso IA coherente
✓ Facciones: Basílica Nueva es NPCs controlables
✓ Tecnología: Anatema Mecánico vs IA antigua es canon tension
✓ Estilo: Apto para tensión narrativa + decisiones

Archivo guardado: `preludio-en-la-basilica-canon.md`

---

## FASE 2 (Opus limpio)

Comenzaré a escribir **"preludio-en-la-basilica.md"** como inicio de campaña.

Contexto:
- **Jugadores**: 3-4 técnicos iniciados
- **Ubicación**: Nueva Basílica, Ábside (servidores principales)
- **Misterio Central**: IA fragmentada guardada en hardware antiguo
- **Mecánica**: Decisiones abren/cierran caminos narrativos

**Escena de Apertura:**

[Escribe escena de ingreso a la Basílica, primer encuentro, introducción de misterio]

---

¿Qué desean hacer los técnicos?
- A) Inspeccionar los servidores como se ordena
- B) Hacer preguntas al sacerdote supervisor
- C) Explorar más allá del área asignada

[La campaña diverge según la decisión. Sin final predeterminado.]
```

---

## Flujo de Comandos Rápido

| Comando | Resultado |
|---------|-----------|
| `/crear-diegesis` | Muestra ayuda |
| `/crear-diegesis [contexto]` | Inicia FASE 1 (clarificación) |
| (En FASE 2) `Escribe antes de X...` | Narrativa se ajusta |
| (En FASE 2) `No tan literario, más directo` | Estilo se adapta |
| (En FASE 2) `Retrocedemos a [párrafo]` | Vuelve a ese punto, continúa diferente |

---

## Notas para Usuarios

✓ **Tu contexto es exacto**: No lo expandiremos, lo perfeccionaremos.
✓ **Sin límites**: La historia dura lo que tú quieras.
✓ **Control total**: Pausas, direcciones, ajustes siempre en tu mano.
✓ **Canónico**: Validado contra estilo, facciones, cronología, tecnología SyV.
✓ **Iterativo**: Párrafo a párrafo, con feedback inmediato.
