# Implementación Técnica: /crear-diegesis

## Registro del Skill

Para habilitar `/crear-diegesis` en Claude Code, el skill debe registrarse en la configuración del proyecto SyV.

### Ubicación del Descriptor
```
/home/kodex/Dev/syv/src/content/docs/_skills/04-crear-diegesis/SKILL.md
```

### Metadatos Requeridos (YAML Frontmatter)
```yaml
---
title: Crear Diégesis
name: crear-diegesis
description: Creador iterativo de diégesis narrativas - convierte contextos en historias canónicas, valida coherencia y guía la escritura párrafo a párrafo
version: 1.0.0
---
```

---

## Arquitectura de Ejecución

### FASE 1: Clarificación (Haiku/Sonnet)

**Entrada**: Usuario + `/crear-diegesis [optional: contexto]`

**Lógica**:
```
IF contexto está vacío:
  → SHOW HELP
ELSE:
  → FASE 1: Clarificación

FASE 1:
  1. Proponer 3 títulos (derivados de contexto)
   2. Preguntar tipo (Cuento / Artículo / Historia Progresiva)
   3. Hacer preguntas clarificadoras (máximo 3)
   4. Invocar subagentes de validación:
      - crear-verdad (coherencia canon)
      - validar-canon (sistemas completos)
      - estilo-literario (viabilidad estilística)
   5. Guardar [story-title]-canon.md
   6. Transicionar a FASE 2
```

**Subagentes Utilizados**:
```python
subagents = [
    {
        "name": "crear-verdad",
        "task": "Validar coherencia narrativa contra cronología, facciones, ubicaciones",
        "model": "sonnet"  # Más capacidad analítica
    },
    {
        "name": "validar-canon",
        "task": "Cross-check contra todos los sistemas SyV",
        "model": "sonnet"
    },
    {
        "name": "estilo-literario",
        "task": "Revisar viabilidad estilística sin modificar intención",
        "model": "haiku"
    }
]
```

**Salida de FASE 1**:
- Archivo `[story-slug]-canon.md` creado
- Confirmación de parámetros
- Declaración de transición a FASE 2

---

### FASE 2: Escritura Iterativa (Opus 4.6)

**Contexto Limpio** (se descarta contexto de FASE 1 para evitar contaminación):

**Inicialización**:
```
MODEL: Claude Opus 4.6
CONTEXT:
  - Filename: [story-slug]-canon.md
  - Available skills: estilo-literario, validar-canon, personajes, ubicaciones, cronologia
  - User context: [Summary from PHASE 1 only]

PROMPT:
"Eres un Arquitecto Narrativo de Subordinación y Valor.
Tu trabajo es escribir [story-title].md párrafo a párrafo con el usuario.

Referencia canónica: [story-slug]-canon.md
Respeta la voz del usuario. No improvises, no extraples.
Perfecciona su intención exacta en prosa canónica SyV.

¿Listo para comenzar?"
```

**Bucle de Escritura**:
```
WHILE usuario no termina:
  → Escribir párrafo/sección
  → Esperar feedback del usuario
  → Procesar comando:
    - Pausar: Guardar progreso
    - Retroceder: Volver a punto anterior
    - Ajustar estilo: Reescribir manteniendo intención
    - Continuar: Escribir siguiente
    - Insertar: Añadir antes/después
    - Validar: Verificar coherencia actual
  → Actualizar [story-slug].md
```

**Archivo de Escritura**:
```
Location: /diegesis/[story-slug].md

YAML Frontmatter:
---
title: "[Story Title]"
slug: "[story-slug]"
type: "[Cuento Corto | Artículo | Historia Progresiva]"
status: "En Escritura"
canon_ref: "[story-slug]-canon.md"
updated: "[timestamp]"
---

[Narrative Content]
```

**Validación Durante Escritura**:
- Invoke `validar-canon` si cambios narrativos ocurren
- Check `estilo-literario` compliance en párrafos clave
- Alert usuario si coherencia se rompe

---

## Estructura de Directorios

```
/home/kodex/Dev/syv/src/content/docs/
├── _skills/
│   └── 04-crear-diegesis/
│       ├── SKILL.md              ← Definición principal
│       ├── EJEMPLOS.md           ← Casos de uso
│       └── IMPLEMENTACION.md     ← Este archivo
│
├── diegesis/                      ← Output stories
│   ├── el-perro-que-escucha.md
│   ├── el-perro-que-escucha-canon.md
│   ├── preludio-en-la-basilica.md
│   └── preludio-en-la-basilica-canon.md
│
└── [resto de estructura SyV]
```

---

## Invocación desde Claude Code CLI

### Comando Directo
```bash
claude code /crear-diegesis "Tu contexto de historia aquí"
```

### Con Parámetros (Futura Expansión)
```bash
claude code /crear-diegesis --type "cuento-corto" --year 2165 "Tu contexto"
```

### Flujo Interactivo (Recomendado)
```bash
# 1. Abre el proyecto SyV
cd /home/kodex/Dev/syv

# 2. Invoca Claude Code
claude code

# 3. En la sesión interactiva:
/crear-diegesis Tu contexto narrativo aquí
```

---

## Manejo de Errores

### Error: Sin Contexto
```
USER: /crear-diegesis

RESPONSE: [Muestra SKILL.md:HELP]
```

### Error: Coherencia Canónica Rota
```
FASE 1:
✗ Cronología: Año 2500 es post-futura (canon máximo 2200)
✗ Ubicación: "Nueva Vancouver" no existe en SyV

RESPUESTA:
"He detectado 2 incompatibilidades:
1. Año 2500 está fuera del rango canónico (máx 2200)
   → ¿Ajustamos a 2178 (actual) o pre-Colapso?
2. "Nueva Vancouver" no existe
   → ¿Usamos Buenos Aires/Dársena o creas ubicación nueva?

[Espera confirmación antes de continuar]"
```

### Error: Ambigüedad de Intención
```
FASE 1 (Preguntas Clarificadoras):
"Tu contexto menciona 'misterio oscuro' pero no está claro si:
A) El protagonista lo descubre y debe decidir qué hacer
B) El protagonista lo causa accidentalmente
C) El protagonista es testigo pasivo

¿Cuál es tu intención?"
```

---

## Guardar Progreso

### Checkpoint Manual (FASE 2)
```
USER: Guarda aquí

ASSISTANT:
Guardando `el-perro-que-escucha.md` (párrafos 1-23 completos).
Puedes retomar desde aquí cuando quieras.
```

### Checkpoint Automático
Cada transición de párrafo, la escritura se guarda en `[story-slug].md`.

---

## Transiciones Entre Modelos

### FASE 1 → FASE 2
```
[Haiku/Sonnet termina FASE 1]
                    ↓
[Genera summary: title, type, POV, key elements]
                    ↓
[Invoca Opus 4.6 con contexto limpio]
                    ↓
[Opus inicia escritura desde 0, solo referencia -canon.md]
```

**Razón**: Opus es mejor para narrativa sostenida. Haiku se usa para clasificación/validación (más rápido).

---

## Referencia de Skills Disponibles en FASE 2

| Skill | Uso en Escritura |
|-------|------------------|
| `estilo-literario` | Validar cumplimiento de 13 reglas. Aplicar ajustes estilísticos. |
| `validar-canon` | Verificar coherencia si cambios narrativos grandes ocurren. |
| `personajes` | Crear/refinar personajes nuevos en narrativa. |
| `ubicaciones` | Crear/refinar ubicaciones nuevas. |
| `cronologia` | Validar timeline de eventos. |
| `crear-verdad` | Resolver contradicciones canónicas. |

---

## Límites y Restricciones

### Qué SÍ Puedo
✓ Escribir párrafo a párrafo
✓ Ajustar estilo a solicitud del usuario
✓ Retroceder/pausar
✓ Validar coherencia
✓ Crear personajes/ubicaciones nuevas (si canon lo permite)
✓ Abrir/cerrar narrativas según usuario

### Qué NO Puedo
✗ Contradecir intención explícita del usuario
✗ Extrapolativamente expandir más allá del contexto
✗ Sugerir "mejoras" no solicitadas
✗ Imponer estructura narrativa
✗ Añadir "detalles atmosféricos" no pedidos
✗ Reescribir completo sin permiso

---

## Testing y QA

### Test Case 1: Help Response
```
Input: /crear-diegesis (sin contexto)
Expected: Despliega SKILL.md Help section
Status: ✓
```

### Test Case 2: Cuento Corto Flujo Completo
```
Input: /crear-diegesis [contexto perro]
Expected:
  - Propone títulos
  - Pregunta tipo (selecciona Cuento)
  - 2 preguntas clarificadoras
  - Valida
  - Crea -canon.md
  - Transiciona a Opus
  - Escribe primer párrafo
Status: ✓
```

### Test Case 3: Historia Progresiva con Divergencia
```
Input: /crear-diegesis [contexto rol]
Expected:
  - Crea -canon.md
  - FASE 2: Escena abierta con 3+ opciones de acción
  - Usuario selecciona camino
  - Narrativa diverge sin final fijo
Status: ✓
```

---

## Notas para Desarrollo Futuro

1. **Integración con Git**: Auto-commit de -canon.md tras FASE 1
2. **Historial de Versiones**: Mantener todas las versiones de [story-slug].md
3. **Exportación**: Guardar como .epub, .pdf para lectura offline
4. **Colaborativo**: Múltiples usuarios en misma historia (requiere lock/merge)
5. **Analytics**: Contar palabras, párrafos, tiempo de escritura
6. **Plantillas Narrativas**: Pre-filled -canon.md para géneros comunes

---

**Última Actualización**: 2026-02-09
**Versión**: 1.0.0
**Status**: Listo para implementación
