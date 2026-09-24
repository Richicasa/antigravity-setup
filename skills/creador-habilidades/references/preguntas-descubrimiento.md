# Banco de Preguntas para el Descubrimiento de Habilidades

Cuando el usuario solicite crear una nueva habilidad, no formules todas las preguntas a la vez para no abrumarlo. Selecciona 2 o 3 preguntas relevantes por ronda para refinar los requisitos de forma conversacional.

---

## Ronda 1: Comprensión del Objetivo y Alcance

1. **"¿Cuál es el objetivo principal que debe resolver esta habilidad?"**
   *(Ejemplo: Automatizar la creación y prueba de APIs en FastAPI, o desplegar aplicaciones a Firebase con verificación de estado).*
2. **"¿Qué frases o peticiones típicas usarás para pedirle al agente que la use?"**
   *(Esto definirá el campo `description` del frontmatter para que el agente sepa cuándo activarse).*
3. **"¿Qué entradas necesitará el flujo (archivos, argumentos, URLs) y cuál es el resultado o entregable esperado?"**

---

## Ronda 2: Nivel de Rigidez y Manejo de Errores

1. **"En caso de que un paso falle (por ejemplo, fallo de conexión o error de compilación), ¿prefieres que el agente intente alternativas automáticamente, o que se detenga y solicite tu orientación?"**
2. **"¿Hay pasos donde el comando o método debe ser estrictamente exacto (ej. flags mandatorios de seguridad), o el agente tiene flexibilidad para elegir la mejor herramienta?"**
3. **"¿Existen casos borde o errores conocidos comunes que debamos documentar en la sección de resolución de problemas?"**

---

## Ronda 3: Ámbito y Dependencias Técnicas

1. **"¿Dónde prefieres instalar la habilidad?"**
   - **Global (`~/.gemini/config/skills/`):** Para que esté disponible en cualquier carpeta o proyecto de tu equipo.
   - **Local del Proyecto (`.agents/skills/`):** Para que quede guardada dentro del repositorio actual y pueda compartirse con tu equipo vía Git.
2. **"¿Este flujo requiere scripts auxiliares para automatizar comandos largos (PowerShell, Python, Bash), o basta con un conjunto de instrucciones escritas paso a paso?"**
3. **"¿Hay herramientas CLI externas, APIs o claves de acceso que deban estar previamente instaladas en el sistema?"**

---

## Criterios de Completitud para Iniciar la Creación

Antes de redactar los archivos, asegúrate de tener claros:
- [x] Nombre formal de la habilidad (`name` en minúsculas y con guiones).
- [x] Descripción clara con disparadores de activación (`description`).
- [x] Ámbito de instalación (Global vs. Local).
- [x] Lista ordenada de pasos del flujo.
- [x] Mecanismo de validación o prueba final.
