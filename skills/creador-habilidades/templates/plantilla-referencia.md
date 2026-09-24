# Plantilla para Archivos de Referencia (`references/*.md`)

Utiliza esta plantilla cuando necesites extraer tablas grandes de parámetros, manuales de API, especificaciones complejas o listas de errores hacia la carpeta `references/`, manteniendo el archivo `SKILL.md` principal conciso y enfocado.

```markdown
# [Nombre del Tema o Componente]: Manual de Referencia

Este documento amplía la información operativa descrita en [SKILL.md](../SKILL.md). Consulta este material únicamente cuando se requiera configuración avanzada o solución de incidencias específicas.

---

## 1. Parámetros y Opciones de Configuración

| Parámetro | Tipo | Obligatorio | Valor por Defecto | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `--env` | `string` | Sí | `development` | Define el entorno de ejecución (`development`, `staging`, `production`). |
| `--timeout` | `integer`| No | `30` | Límite máximo de espera en segundos antes de abortar la operación. |

---

## 2. Códigos de Error y Diagnóstico

| Código | Significado | Acción Correctiva |
| :--- | :--- | :--- |
| `ERR_CONN_REFUSED` | El servicio destino no responde | Verificar si el contenedor o proceso local está activo. |
| `ERR_INVALID_SCHEMA`| Formato de entrada incorrecto | Revisar el esquema JSON en [resources/schema.json](../resources/schema.json). |

---

## 3. Especificaciones de Seguridad y Restricciones

- Nunca incluyas claves de API ni credenciales secretas directamente en archivos Markdown o scripts de la habilidad.
- Si se requieren permisos elevados, documenta el comando exacto que el usuario debe ejecutar para otorgarlos.
```
