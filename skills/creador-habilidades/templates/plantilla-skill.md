# Plantilla Base para SKILL.md

Copia este esquema base y adáptalo para crear una nueva habilidad en Google Antigravity:

```markdown
---
name: nombre-de-la-habilidad
description: >-
  Describe en tercera persona el propósito exacto de la habilidad y los casos de uso en los que
  debe activarse. Incluye términos clave que el usuario podría utilizar al pedir ayuda y especifica
  claramente cuándo NO debe utilizarse.
---

# Título Descriptivo de la Habilidad

Breve resumen (1 a 2 oraciones) explicando el flujo de trabajo especializado o runbook que implementa esta habilidad.

---

## 1. Prerrequisitos y Verificación de Entorno

Antes de comenzar la ejecución, valida que las dependencias requeridas estén presentes:

- [ ] Herramienta instalada: `nombre-herramienta --version`
- [ ] Variables de entorno o credenciales configuradas en el sistema.

---

## 2. Flujo Operativo Paso a Paso

### Paso 1: Preparación inicial
Explica la primera acción o comando requerido:
```bash
comando de preparacion --parametro valor
```

### Paso 2: Ejecución Principal
Detalla el núcleo del procedimiento con los comandos exactos o scripts de apoyo:
```bash
comando de ejecucion principal
```

> [!TIP]
> Si este paso involucra opciones avanzadas, consulta [Documento de Referencia](references/guia-avanzada.md).

### Paso 3: Verificación de Resultados
Instrucciones claras para confirmar que la acción se completó con éxito:
```bash
comando de verificacion o test
```

---

## 3. Árbol de Decisiones (Opcional)

Si el flujo presenta variaciones según el contexto:
- **Si ocurre la condición A:** Ejecuta la acción 1.
- **Si ocurre la condición B:** Ejecuta la acción 2.

---

## 4. Resolución de Problemas Frecuentes

| Error o Síntoma Común | Causa Probable | Solución Recomendada |
| :--- | :--- | :--- |
| `Error 401 Unauthorized` | Sesión o token expirado | Ejecutar `auth login` |
| Fallo en compilación | Dependencia faltante | Ejecutar instalación de paquetes |
```
