# Especificación Oficial de Habilidades (Skills) en Google Antigravity

Una habilidad (*Skill*) en Google Antigravity es un paquete autocontenido de conocimiento, instrucciones y herramientas accesorias que enseñan al agente cómo realizar flujos de trabajo específicos de forma repetible, precisa y autónoma.

Fuente oficial de referencia: [https://antigravity.google/docs/skills](https://antigravity.google/docs/skills)

---

## 1. Ciclo de Vida y Descubrimiento de una Habilidad

El sistema de Antigravity gestiona las habilidades en tres etapas clave:

1. **Descubrimiento (*Discovery*):** Al iniciar una sesión o conversación, el agente inspecciona los directorios de habilidades disponibles y extrae **únicamente** los metadatos del encabezado YAML: `name` y `description`. No lee el cuerpo de los archivos `SKILL.md` en esta etapa para ahorrar memoria y contexto.
2. **Activación Condicional (*Triggering*):** Cuando el usuario envía un mensaje, el modelo compara la intención del usuario con los campos `description` de las habilidades descubiertas. Si hay una coincidencia clara, la habilidad se activa.
3. **Carga e Ingesta (*Progressive Loading*):** Solo al activarse, el agente lee el contenido completo de `SKILL.md`. Si el archivo contiene enlaces relativos a `references/`, el agente solo los leerá si necesita profundizar durante la ejecución de los pasos.

---

## 2. Ubicaciones de Almacenamiento

Antigravity admite dos niveles de alcance para las habilidades:

### A. Ámbito Global (Máquina local)
* **Ruta:** `~/.gemini/config/skills/<nombre-habilidad>/` (en Windows: `C:\Users\<usuario>\.gemini\config\skills\<nombre-habilidad>\`)
* **Uso:** Habilidades transversales que deben estar disponibles en cualquier proyecto o incluso cuando no hay ningún espacio de trabajo abierto en el IDE.

### B. Ámbito de Proyecto / Espacio de Trabajo (Workspace)
* **Ruta:** `<raiz-del-proyecto>/.agents/skills/<nombre-habilidad>/` (también soporta `.agent/skills/` por retrocompatibilidad).
* **Uso:** Convenciones, pipelines, migraciones o pruebas exclusivas de un repositorio de código específico. Se pueden compartir con el equipo mediante Git.

---

## 3. Especificación del Frontmatter YAML

El archivo `SKILL.md` debe iniciar en la primera línea con un bloque YAML delimitado por `---`:

```yaml
---
name: nombre-de-la-habilidad
description: >-
  Descripción completa y detallada en tercera persona. Explica qué hace la habilidad,
  los términos y disparadores por los que debe activarse, y cuándo NO debe utilizarse.
---
```

### Reglas de los Campos:

| Campo | Tipo | Obligatorio | Reglas y Restricciones |
| :--- | :--- | :--- | :--- |
| `name` | `string` | **Sí** | Identificador único. Solo letras minúsculas, dígitos y guiones medios (`^[a-z0-9-]+$`). No debe contener espacios, mayúsculas ni caracteres especiales. Máximo 64 caracteres. |
| `description` | `string` | **Sí** | Texto descriptivo redactado en tercera persona. Máximo 1024 caracteres. Es el factor decisivo para que el agente elija la habilidad. |

### Redacción Eficaz de la `description`:
- **Comienza en tercera persona:** *"Proporciona directrices para...", "Automatiza el despliegue de...", "Guía paso a paso en..."*.
- **Incluye palabras clave de activación (*Triggers*):** Menciona explícitamente sinónimos y acciones que el usuario podría escribir (ej. *"crear habilidad, redactar SKILL.md, empaquetar runbook"*).
- **Define límites negativos (*Exclusions*):** Aclara lo que no hace (ej. *"No usar para consultas SQL generales; usa bigquery-sql en su lugar"*).

---

## 4. Estructura de Directorios Recomendada

```text
<nombre-habilidad>/
├── SKILL.md                 # [Obligatorio] Documento de entrada con frontmatter YAML
├── references/              # [Opcional] Documentación extendida, especificaciones de APIs, tablas
├── templates/               # [Opcional] Plantillas de código o archivos base
├── examples/                # [Opcional] Ejemplos de uso real o transcripciones de muestra
└── scripts/                 # [Opcional] Scripts ejecutables auxiliares (PowerShell, Bash, Python)
```

---

## 5. Reglas de Enlace Markdown

Para referenciar documentos auxiliares dentro de la habilidad:
- Utiliza **siempre rutas relativas**: `[Manual](references/manual.md)` o `[Plantilla](templates/plantilla.md)`.
- No utilices rutas absolutas con `file:///` en las habilidades portables, ya que cambiarían entre máquinas y entornos de desarrollo.
