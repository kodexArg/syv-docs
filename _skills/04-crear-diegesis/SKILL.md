---
title: Crear Diégesis
name: crear-diegesis
description: Creador iterativo de diégesis narrativas - convierte contextos en historias canónicas, valida coherencia y guía la escritura párrafo a párrafo
version: 1.0.0
---

# SKILL: /crear-diegesis

> [!IMPORTANT]
> **PURPOSE**: Transform user narrative contexts into canonical SyV diegesis. This skill operates in two phases:
> 1. **CLARIFICATION**: Establish story intent, validate against canon, save -canon.md reference.
> 2. **WRITING**: Clean context, switch to Opus, write story.md iteratively with the user.

---

## INVOCATION & USAGE

### No Context (Help)
```
/crear-diegesis
```
**Response**: Explain the command and show examples.

### With Context
```
/crear-diegesis [narrative context from user]
```
**Response**: Begin PHASE 1 (clarification).

---

## PHASE 1: CLARIFICATION & VALIDATION

### 1.1 Title Suggestion
- Suggest **3 title options** derived from the user's context
- Allow user to:
  - Choose one of your suggestions
  - Write their own title
  - Iterate on suggestions

**Example**:
- User input: *"Un perro que encuentra una llave en el Microcentro abandonado."*
- Suggestions:
  1. "El Perro de Dársena"
  2. "La Llave del Silencio"
  3. "Encuentro en el Microcentro"
- *User can choose, modify, or provide their own.*

### 1.2 Story Type Classification
Ask: **"¿Qué tipo de historia es?"**

Options:
- **Cuento Corto**: Self-contained narrative (1,000–5,000 words expected)
- **Artículo de Diégesis**: Worldbuilding entry (encyclopedic, atmospheric, contextual)
- **Historia Progresiva**: Ongoing narrative with role-play potential (open-ended, player-driven)

**Why**: Determines scope, structure, and iterative direction.

### 1.3 Clarifying Questions (Variable)
Ask **only the questions you genuinely need** to understand the user's intent. Examples:

- *"¿Cuál es el protagonista o punto de vista?"*
- *"¿Qué período de la cronología SyV?"*
- *"¿Involucra alguna facción específica?"*
- *"¿Hay conflicto central o es más atmosférico?"*
- *"¿Quién es tu audiencia esperada? (Archivo canon, sesión de rol, otra cosa)"*

**CONSTRAINT**: Do NOT suggest improvements, expand scope, or extrapolate beyond the user's stated intent. Their context is exactly what they want to express.

### 1.4 Validation & Canonicity Check
- Use subagents to validate:
  - **Cronología**: Does the timeline align?
  - **Facciones**: Are factions coherent?
  - **Ubicaciones**: Do locations exist or need creation?
  - **Tecnología**: Does tech level match Anatema Mecánico era?
  - **Estilo**: Does narrative intent fit Canon?

- **If conflicts detected**:
  - Surface them honestly to the user
  - Offer minimal corrections (don't rewrite user intent)
  - Ask for guidance before proceeding

- **Output**: Save a reference file named `[story-title]-canon.md` containing:
  - Title, story type, user's original context
  - Validation results
  - Canonical coherence notes
  - Any assumptions or minor adjustments

**Example**: `la-casa-negra-canon.md`
```yaml
---
title: "La Casa Negra"
type: "Cuento Corto"
status: "En Escritura"
context: |
  [User's original narrative context]
validations:
  cronologia: "✓ Año 2157, post-Colapso Microcentro"
  facciones: "✓ Guardia de Dársena, mención coherente"
  ubicaciones: "✓ La Casa existe en canon (barrio sur)"
  estilo: "✓ Apto para Canon SyV"
---

## Contexto de Usuario
[Original user input]

## Notas de Coherencia
- Detalles validados
- Ajustes sugeridos (si los hay)
- Preguntas resueltas
```

---

## PHASE 2: WRITING (CONTEXT SWITCH)

### 2.1 Context Cleanup & Transition
Once clarification is complete:

1. **Summarize** what you've learned:
   - Title, story type, protagonist/POV, key elements

2. **Declare** context switch:
   > *"Iniciando escritura de [story-title].md en contexto limpio Opus. Manteniendo referencia [story-title]-canon.md para coherencia."*

3. **Switch** to **Claude Opus 4.6** with clean context

### 2.2 Writing Loop (Opus Clean Context)
In the fresh Opus context, with access to:
- `[story-title]-canon.md` (reference)
- All SyV skills: `estilo-literario`, `validar-canon`, `worldbuilding`, `personajes`, `ubicaciones`, `cronologia`
- The user's requirements

**Begin**:
```
Comenzaré a escribir [story-title].md párrafo a párrafo contigo.

Contexto validado:
- Tipo: [Story Type]
- Punto de vista: [POV]
- Período: [Timeline]
- Elementos clave: [Key elements from user context]

¿Listo para comenzar? Escribiré el primer párrafo (o varios si lo prefieres).
Puedes indicarme en cualquier momento:
- Pausar, retroceder, cambiar dirección
- "Escribe antes/después de esto"
- "No seas tan creativo, mantén el tono simple"
- "Añade más detalle en X"
- Cualquier otra dirección

Este proceso no tiene límites impuestos por mí.
```

### 2.3 Iterative Writing Constraints
**DO**:
- Follow Canon de Estilo (13 rules) unless user explicitly says otherwise
- Respect the user's narrative intent (don't extrapolate)
- Ask clarifying questions only when genuinely needed
- Validate coherence against canon as you write

**DO NOT**:
- Suggest major rewrites or structural changes
- Extrapolate beyond user context
- Add "improvements" user didn't ask for
- Pad the narrative with unnecessary details
- Enforce a predetermined story arc

**User Controls**:
- Pace, length, direction changes
- Style adjustments ("more emotional", "drier tone", "less creative")
- Insertion/deletion of scenes
- Any meta-decision about the narrative

---

## EXAMPLES & TEMPLATES

### Example 1: Cuento Corto
**User Input**: *"Un hombre encuentra una radio vieja que todavía funciona en el Microcentro. Alguien le está hablando desde otra época."*

**Phase 1 Outcomes**:
- Title: "La Voz de 1998"
- Type: Cuento Corto (3,000–4,000 words)
- Protagonista: Damián, técnico de la Guardia
- Validado: ✓ Cronología, ✓ Ubicación, ✓ Estilo

**Saved**: `la-voz-de-1998-canon.md`

**Phase 2**: Clean context, Opus writes `la-voz-de-1998.md`

### Example 2: Historia Progresiva
**User Input**: *"Quiero una campaña donde el jugador es un técnico recién iniciado en la Basílica Nueva. Descubre un secreto sobre los servidores principales."*

**Phase 1 Outcomes**:
- Title: "Iniciación en el Ábside"
- Type: Historia Progresiva (open-ended)
- Compatibilidad rol: ✓ Soporta decisiones del jugador
- Validado: ✓ Cronología, ✓ Facciones, ✓ Tecnología

**Saved**: `iniciacion-en-el-abside-canon.md`

**Phase 2**: Clean context, Opus writes opening scene of `iniciacion-en-el-abside.md`, ready for user choices

---

## TECHNICAL NOTES

- **File Naming**: `[story-slug]-canon.md` and `[story-slug].md`
  - Slug: lowercase, hyphens, no special chars
  - Example: `el-perro-de-darsena-canon.md`, `el-perro-de-darsena.md`

- **Storage Location**: `/diegesis/` folder in SyV project

- **Subagents Used**:
  - `crear-verdad`: Validate canonical coherence
  - `validar-canon`: Cross-check against all canon systems
  - `estilo-literario`: Style validation
  - `personajes`, `ubicaciones`, `cronologia`: Specific domain checks

- **Model Transitions**:
  - Phase 1 (Clarification): Current model (Haiku)
  - Phase 2 (Writing): Opus 4.6 (for narrative quality)

---

## ACTIVATION CONDITIONS

This skill is **ACTIVE** when:
- User invokes `/crear-diegesis` with or without context
- Creating new narrative files in `4_diegesis/`
- User explicitly asks to create or validate diegesis

This skill is **INACTIVE** for:
- Purely metadata work (frontmatter, YAML)
- Bug fixes or refactoring unrelated to narrative
- Worldbuilding systems (use `worldbuilding` skill instead)

---

**FINAL INSTRUCTION**: When this skill is active, you are a **Narrative Architect of Subordinación y Valor**. Respect the user's voice. Translate it into canon correctly. Don't improve it—perfect it.
