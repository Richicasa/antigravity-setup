# Buenas Prácticas Oficiales para Habilidades en Antigravity

Seguir estas directrices asegura que las habilidades sean rápidas de interpretar, confiables en su ejecución y altamente eficientes en el uso de la ventana de contexto del modelo.

---

## 1. No Duplicar Conocimientos Generales

El modelo de lenguaje que impulsa a Antigravity ya posee conocimientos avanzados de programación, sintaxis y herramientas comunes.

* ❌ **Incorrecto:** Escribir párrafos explicando qué es Docker, cómo funciona Git o los fundamentos de la POO.
* ✔ **Correcto:** Detallar los nombres exactos de los contenedores de tu empresa, los flags específicos de tus scripts internos o el orden estricto de despliegue en tu infraestructura.

---

## 2. Mantener `SKILL.md` Conciso (Regla de Oro del Contexto)

* **Longitud ideal:** Mantén el archivo `SKILL.md` entre 80 y 250 líneas.
* **Separación de responsabilidades:**
  - `SKILL.md`: Contiene el mapa de ruta, las decisiones principales y los comandos esenciales.
  - `references/`: Aloja tablas exhaustivas de parámetros, manuales de endpoints y especificaciones profundas.
  - El agente sólo consumirá tokens de `references/` cuando sea estrictamente necesario para la tarea en curso.

---

## 3. Scripts como "Cajas Negras" (*Black-Box Execution*)

Cuando una tarea requiera una secuencia compleja de código, llamadas a APIs o lógica iterativa:

* Empaqueta la lógica en un script dentro de la carpeta `scripts/` (ej. `scripts/desplegar.ps1` o `scripts/analizar.py`).
* Instruye al agente para que ejecute el script pasando el flag `--help` si necesita recordar las opciones disponibles, en lugar de ordenar al agente leer todo el código fuente del script.
* **Beneficio:** Ahorra cientos o miles de tokens en el historial del chat y reduce la probabilidad de alucinaciones sintácticas.

---

## 4. Guardar Salidas Extensas en Archivos

* ❌ **Evitar volcar salidas masivas a la terminal:** Si un comando o API produce cientos de líneas de JSON o logs, la terminal se satura y se desperdician tokens en el contexto.
* ✔ **Guardar en archivo y filtrar:** Configura tus scripts para que escriban el resultado en un archivo local (ej. `resultado.json`) y únicamente impriman en consola una línea de confirmación breve:
  ```text
  ✔ Proceso completado con éxito. Resultados guardados en: resultados.json
  ```
* El agente podrá luego consultar o filtrar con comandos específicos solo los campos que necesita.

---

## 5. Incorporar Árboles de Decisión Claros

Los agentes operan con mayor precisión cuando se les proporcionan ramas de decisión explícitas:

```markdown
### Decisión: Modo de Despliegue
- **Si el cambio afecta únicamente al frontend:**
  Ejecuta `npm run build` y sube los archivos estáticos a Cloud Storage.
- **Si el cambio incluye migraciones de base de datos:**
  Ejecuta `alembic upgrade head` ANTES de reiniciar el contenedor de backend.
- **Si el entorno es staging:**
  Usa el flag `--dry-run` para previsualizar los cambios.
```

---

## 6. Pasos de Verificación Concretos y Medibles

Toda habilidad debe concluir con un mecanismo para verificar que el trabajo fue exitoso:
- Comprobación de código de salida (`exit code 0`).
- Prueba de conectividad HTTP (ej. `curl -I https://...` esperando un `200 OK`).
- Ejecución de un comando de estado (ej. `docker ps` o `kubectl get pods`).
- Validación contra una suite de pruebas unitarias o de integración.
