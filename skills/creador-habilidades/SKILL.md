---
name: creador-habilidades
description: >-
  Guía experta en español para diseñar, estructurar, redactar, empaquetar y validar nuevas habilidades (skills) en Google Antigravity según las especificaciones oficiales de https://antigravity.google/docs/skills. Úsala cuando el usuario pida crear una nueva habilidad, diseñar un archivo SKILL.md, estructurar runbooks automatizados, empaquetar flujos de trabajo reutilizables o generar habilidades personalizadas para el agente.
---

# Creador de Habilidades para Antigravity

Esta habilidad capacita al agente para actuar como un arquitecto y desarrollador de habilidades (*Skills*) para Google Antigravity, garantizando que cada nueva habilidad creada sea modular, cumpla estrictamente con la especificación oficial, no sature la ventana de contexto y ofrezca pasos de ejecución verificables.

---

## 1. Principio Rector: Divulgación Progresiva (*Progressive Disclosure*)

Antigravity opera bajo el patrón de divulgación progresiva para mantener un contexto limpio y eficiente:
- **Descubrimiento inicial:** El agente sólo carga en su contexto el campo `name` y `description` de cada habilidad disponible.
- **Activación bajo demanda:** El archivo principal `SKILL.md` se lee únicamente si el usuario solicita algo que coincide con la `description`.
- **Estructura modular:** El archivo `SKILL.md` debe mantenerse conciso y accionable. La documentación extensa, tablas y especificaciones deben ubicarse en `references/` y vincularse con enlaces relativos Markdown.

### Enlaces a Documentación de Soporte:
- [Especificación Oficial de Habilidades](references/especificacion-oficial.md)
- [Buenas Prácticas de Rendimiento y Contexto](references/buenas-practicas.md)
- [Banco de Preguntas de Descubrimiento](references/preguntas-descubrimiento.md)
- [Plantilla Base para SKILL.md](templates/plantilla-skill.md)
- [Plantilla para Archivos de Referencia](templates/plantilla-referencia.md)
- [Ejemplo de Habilidad Completa](examples/ejemplo-habilidad.md)

---

## 2. Dónde Viven las Habilidades

Antes de crear los archivos, determina el alcance con el usuario:

| Ámbito | Ubicación | Cuándo Utilizarlo |
| :--- | :--- | :--- |
| **Global (Toda la máquina)** | `~/.gemini/config/skills/<nombre-habilidad>/` | Herramientas generales, flujos personales, utilidades multiplataforma que deben estar disponibles en cualquier proyecto. |
| **Espacio de Trabajo (Proyecto)** | `<raiz-proyecto>/.agents/skills/<nombre-habilidad>/` | Reglas y flujos específicos de un repositorio (ej. pruebas internas, despliegues del proyecto, convenciones de equipo). |

---

## 3. Anatomía de una Habilidad

Una habilidad se organiza como un directorio autónomo:

```text
<nombre-habilidad>/
├── SKILL.md                 # [Obligatorio] Instrucción principal con frontmatter YAML
├── references/              # [Opcional] Manuales extensos, APIs, tablas de referencia
├── templates/               # [Opcional] Plantillas de código, configuración o prompts
├── examples/                # [Opcional] Ejemplos de entrada/salida y casos de uso
└── scripts/                 # [Opcional] Scripts ejecutables de apoyo (PowerShell, Bash, Python)
```

---

## 4. Flujo de Creación en 5 Fases

Cuando el usuario te pida crear una nueva habilidad, sigue rigurosamente este procedimiento:

### Fase 1: Entrevista de Descubrimiento
No asumas requerimientos ambiguos. Realiza una breve ronda de preguntas (2 a 3 preguntas clave) consultando el [Banco de Preguntas de Descubrimiento](references/preguntas-descubrimiento.md):
1. ¿Cuál es el objetivo primordial y alcance del flujo?
2. ¿Qué disparadores o frases clave usará el usuario para activarla?
3. ¿Requiere ejecución de comandos/scripts o es únicamente de razonamiento y protocolo?
4. ¿Debe instalarse a nivel global (`~/.gemini/config/skills/`) o local en el proyecto (`.agents/skills/`)?

### Fase 2: Determinación del Tipo de Habilidad
Evalúa si la habilidad requiere scripts auxiliares:
- **Solo instrucciones:** Si el flujo consiste en razonamiento, coordinación de herramientas existentes o cumplimiento de directrices escritas sin scripts complejos.
- **Habilidad con scripts auxiliares:** Si algún paso involucra procesamiento de datos de más de 5 líneas, lógica iterativa o APIs específicas. En este caso:
  - Crea scripts en `scripts/` (ej. `.ps1`, `.py`, `.sh`).
  - Trata los scripts como **cajas negras**: enseña al agente a invocarlos con `--help` para conocer sus parámetros en lugar de volcar todo el código al contexto.
  - Guarda las salidas extensas en archivos (no en la consola directa).

### Fase 3: Redacción del Frontmatter YAML y `SKILL.md`
El archivo `SKILL.md` **debe comenzar obligatoriamente** con el frontmatter YAML:

```yaml
---
name: nombre-en-minusculas-con-guiones
description: >-
  Descripción en tercera persona. Especifica con precisión qué hace y cuándo debe activarse.
  Incluye disparadores claros y exclusiones (cuándo NO usarla).
---
```

**Estructura obligatoria del cuerpo de `SKILL.md`:**
1. **Título y Propósito:** Resumen conciso de una oración.
2. **Prerrequisitos / Entorno:** Herramientas CLI necesarias, credenciales o variables de entorno.
3. **Flujo de Ejecución Paso a Paso:** Pasos numerados con instrucciones claras e imperativas.
4. **Árboles de Decisión:** Reglas condicionales explícitas (*"Si ocurre X, haz Y; si ocurre Z, haz W"*).
5. **Manejo de Errores y Diagnóstico:** Qué hacer ante los fallos más comunes.
6. **Verificación:** Pasos concretos para confirmar que el objetivo se cumplió.

> [!TIP]
> Usa la [Plantilla Base para SKILL.md](templates/plantilla-skill.md) para acelerar la redacción.

### Fase 4: Creación de Material de Apoyo
- Extrae documentación pesada hacia `references/<nombre>.md` y usa enlaces relativos como `[Especificación Oficial](references/especificacion-oficial.md)`.
- Si generas scripts ejecutables, asegúrate de que incluyan mensajes breves de estado y manejo de errores con códigos de salida (`exit 0` en éxito, `exit 1` en error).

### Fase 5: Validación Técnica
Antes de dar por concluida la creación, ejecuta el script de validación o realiza el checklist:
- [ ] Frontmatter YAML válido delimitado por `---`.
- [ ] Campo `name` en minúsculas, solo letras, números y guiones (`a-z0-9-`), sin espacios.
- [ ] Campo `description` detallado en tercera persona, con disparadores y exclusiones.
- [ ] Todos los enlaces relativos Markdown apuntan a archivos existentes.
- [ ] No duplica conocimientos generales que el modelo ya conoce de forma nativa.
- [ ] Se ejecutó el script de validación `scripts/validar-habilidad.ps1` exitosamente.
