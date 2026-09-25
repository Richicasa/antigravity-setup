# ⚡ Antigravity Pro Suite

> **La suite definitiva de configuración, habilidades (skills), subagentes y protocolos de ingeniería de software para Google Antigravity.**  
> Diseñada para dotar a cualquier máquina con capacidades de desarrollo agéntico de nivel superior con **instalación en 1 solo clic** y **carga progresiva de contexto**.

---

## 🌟 Características Principales

- 🎯 **50 Habilidades Globales Auditadas:** Cubren desde arquitectura frontend, bases de datos y optimización de rendimiento, hasta testing con navegadores, seguridad web y automatización de documentos.
- 👥 **6 Subagentes Especializados:** Agentes delegados listos para investigación biomédica, estadística, narrativa académica, síntesis y redacción técnica.
- 🛡️ **Escudo de Seguridad Antimalware (`skill-security-guard`):** Auditoría estática heurística obligatoria antes de instalar o ejecutar cualquier habilidad o repositorio de terceros.
- 🐘 **Arquitectura de Carga Progresiva (*Zero Context Bloat*):** Evita el *"efecto de un elefante cayendo sobre una hormiga"*. Antigravity solo carga una pequeña descripción inicial de 2 líneas; el manual operativo completo y los scripts de cada skill se activan bajo demanda únicamente cuando la tarea lo requiere.
- ⚡ **Instalador Automático de Herramientas de Desarrollo:** Detecta e instala automáticamente **Git, Node.js LTS, Python 3.12, GitHub CLI y VS Code** mediante `winget` en Windows (o Homebrew/apt en Mac/Linux).
- 📜 **Protocolo Global de Ingeniería (`AGENTS.md`):** Reglas estrictas de ciclo de vida: *Brainstorming → Planning → TDD → Debugging sistemático → Verificación antes de finalizar*.

---

## 🚀 Instalación en 1 Clic

### 🪟 En Windows (Recomendado para tu hermano)

1. Abre una terminal de **PowerShell** (no requiere permisos especiales, pero si abres como Administrador la instalación de herramientas será completamente silenciosa).
2. Clona este repositorio y ejecuta el instalador:

```powershell
git clone https://github.com/Richicasa/antigravity-setup.git
cd antigravity-setup
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

> **¿Qué hace el instalador automáticamente?**
> 1. Comprueba si tienes instalados `git`, `node`, `python`, `gh` y `code`. Si falta alguno, lo instala silenciosamente vía Windows Package Manager (`winget`).
> 2. Crea las carpetas globales estándar en tu perfil (`~/.gemini/config/skills` y `~/.agents/skills`).
> 3. Copia las 45 habilidades y 6 subagentes listos para usar.
> 4. Configura el archivo maestro `AGENTS.md` y las políticas de ejecución `config.json`.
> 5. Ejecuta el escáner antimalware para garantizar que todas las habilidades estén 100% limpias.

---

### 🍎 En macOS / 🐧 En Linux

1. Abre tu terminal.
2. Clona y ejecuta el script:

```bash
git clone https://github.com/Richicasa/antigravity-setup.git
cd antigravity-setup
chmod +x install.sh
./install.sh
```

---

## 🧠 ¿Por qué Carga Progresiva? (*Lazy Loading*)

Muchos usuarios cometen el error de volcar cientos de instrucciones en el prompt del sistema. Cuando un modelo recibe un contexto gigante desde el primer token:
1. Pierde capacidad de razonamiento agudo y atención selectiva.
2. Genera respuestas lentas y costosas.
3. Se produce confusión entre instrucciones contradictorias.

**Nuestra Solución:**
En este repositorio, cada habilidad cuenta con un encabezado estándar:
```yaml
---
name: performance-optimization
description: Optimiza aplicaciones en frontend, backend, queries y Core Web Vitals (LCP, INP, CLS)...
---
```
Antigravity únicamente lee este encabezado en su índice general. Cuando tú le dices: *"Optimiza el tiempo de carga de mi página web"*, el agente detecta que la habilidad relevante es `performance-optimization`, abre su archivo `SKILL.md` bajo demanda, ejecuta sus herramientas y resuelve el problema quirúrgicamente sin malgastar memoria ni tokens en otras 44 habilidades no relacionadas.

---

## 📦 Catálogo de Habilidades (45 Skills Incluidas)

### 🛡️ 1. Seguridad, Defensa & Integridad
- **`skill-security-guard`**: Escáner antimalware heurístico. Detecta reverse shells, scripts ofuscados en Base64, exfiltración de tokens (`.env`, `.ssh`, `.aws`) e inyecciones de prompt en repositorios antes de instalarlos.
- **`owasp-top-10`**: Detección y mitigación de las 10 vulnerabilidades críticas de aplicaciones web (XSS, SQLi, CSRF, fallos de control de acceso).
- **`secure-by-design`**: Principios de diseño seguro desde la arquitectura de software.
- **`accidental-data-loss-prevention`**: Bloqueo preventivo de comandos destructivos (`rm -rf`, `DROP TABLE`, borrado de buckets en la nube) requiriendo confirmación obligatoria.

### 🎨 2. Arquitectura Frontend & UI/UX
- **`frontend-design`**: Diseño de interfaces limpias, modernas y distintivas sin caer en plantillas genéricas.
- **`web-design-guidelines`**: Auditoría de usabilidad, tipografía, jerarquía visual y accesibilidad web.
- **`design-doc-mermaid`**: Generación de diagramas de arquitectura en Mermaid (diagramas de secuencia, clases, entidad-relación y flujos).
- **`generative_ui`**: Renderizado de widgets interactivos HTML directamente en la conversación.
- **`vercel-react-best-practices`**: Buenas prácticas oficiales de ingeniería de Vercel para React y Next.js.

### ⚙️ 3. Ingeniería de Software & Buenas Prácticas
- **`codebase-design`**: Filosofía de John Ousterhout (*Philosophy of Software Design*): diseño de módulos profundos (*deep modules* con interfaz compacta y mucha lógica oculta), costuras (*seams*) limpias y testabilidad natural.
- **`domain-modeling`**: Modelado activo de dominio: construcción y mantenimiento del glosario vivo del proyecto (`CONTEXT.md`) y registro estricto de ADRs solo ante verdaderos *trade-offs* irreversibles.
- **`improve-codebase-architecture`**: Escáner de oportunidades arquitectónicas y deuda técnica en el código con generación de reporte visual HTML.
- **`wizard`**: Generador de scripts bash interactivos (`template.sh`) para guiar a un humano paso a paso en acciones complejas (credenciales en dashboards, tokens, migraciones de BD).
- **`karpathy-guidelines`**: Directrices de Andrej Karpathy para programar con IA: cambios quirúrgicos, sin sobre-ingeniería y con criterios verificables de éxito.
- **`git-workflow-and-versioning`**: Commits atómicos, ramas aisladas, rebase limpio y resolución de conflictos.
- **`api-and-interface-design`**: Diseño ergonómico de APIs y contratos estrictos entre frontend y backend antes de escribir lógica.
- **`performance-optimization`**: Optimización de Core Web Vitals (LCP, INP, CLS), perfilado de memoria y eliminación de cuellos de botella.
- **`observability-and-instrumentation`**: Telemetría, OpenTelemetry, logs estructurados JSON y métricas de error.
- **`documentation-and-adrs`**: Creación de Architecture Decision Records (ADRs) para documentar decisiones técnicas complejas.
- **`shipping-and-launch`**: Checklist previo al despliegue en producción y estrategias de rollback.
- **`ci-cd-and-automation`**: Automatización de pipelines de integración continua y calidad de código.

### 🧪 4. Testing & Automatización Web
- **`playwright-cli`**: Automatización y control de navegadores headless para pruebas e interacción web.
- **`webapp-testing`**: Pruebas de integración visuales para aplicaciones web locales mediante Playwright.
- **`browser-use`**: Control directo del navegador vía Chrome DevTools Protocol (CDP).
- **`test-driven-development`**: Metodología TDD: test primero, código mínimo para pasar y refactorización continua.
- **`verification-before-completion`**: Regla obligatoria: nunca dar por cerrada una tarea sin verificar los tests en la consola.
- **`systematic-debugging`**: Aislamiento metódico de errores de raíz antes de tocar una sola línea de código.

### ☁️ 5. Backend, Datos & Firebase
- **`supabase-postgres-best-practices`**: Optimización de PostgreSQL, Row Level Security (RLS) e índices.
- **`managing-python-dependencies`**: Gestión moderna de dependencias y entornos virtuales con `uv` y `pip`.
- **`firebase-basics`**, **`firebase-auth-basics`**, **`firebase-firestore`**, **`firebase-security-rules-auditor`**, **`firebase-data-connect`**, **`firebase-hosting-basics`**, **`firebase-app-hosting-basics`**, **`firebase-ai-logic-basics`**, **`firebase-remote-config-basics`**, **`firebase-crashlytics`**: Suite integral para aplicaciones construidas sobre Google Firebase.
- **`bigquery-sql`**, **`bigquery-ai-ml`**, **`bigtable-basics`**: Optimización de consultas analíticas y bases de datos a gran escala.

### 📚 6. Documentación, Redacción Científica & Archivos
- **`writing-shape`**: Escultura de artículos o capítulos a partir de un banco desordenado de notas o fuentes (*raw material*), párrafo por párrafo debatiendo formato y progresión lógica.
- **`docx`**: Creación y edición profunda de documentos Word a bajo nivel XML preservando estilos y tipografía.
- **`pdf`**: Extracción quirúrgica de texto, tablas y metadatos desde documentos PDF.
- **`xlsx`**: Lectura y generación avanzada de hojas de cálculo de Excel.
- **`articulos-u-zotero`**: Integración con Zotero Desktop y Microsoft Word con campos dinámicos nativos (`w:fldSimple`), estilo Vancouver y figuras científicas en alta resolución.
- **`humanizar-texto-es`**: Redacción y reescritura de alta naturalidad lingüística eliminando patrones robóticos.
- **`creador-habilidades`**: Guía para diseñar, escribir y empaquetar nuevas habilidades según el estándar de Antigravity.
- **`find-skills`**: Localizador inteligente de nuevas habilidades en el ecosistema skills.sh.

### 🤖 7. Orquestación Agéntica Avanzada
- **`writing-plans`** y **`executing-plans`**: Desglose estructurado de tareas complejas en pasos secuenciales verificables.
- **`subagent-driven-development`** y **`dispatching-parallel-agents`**: Ejecución en paralelo mediante subagentes independientes.
- **`ralph-loop-workflow`**, **`ralph-tui-prd`**, **`ralph-tui-create-json`**, **`ralph-wiggum`**: Bucles autónomos de desarrollo guiados por especificaciones hasta el 100% de cumplimiento.
- **`requesting-code-review`**: Auditoría de código previa al merge.
- **`finishing-a-development-branch`**: Limpieza de ramas y estrategia de integración.

---

## 👥 Subagentes Especializados Incluidos

| Subagente | Rol |
| :--- | :--- |
| **`clinical_evidence_officer`** | Experto en medicina basada en evidencia, análisis de ensayos clínicos y verificación GRADE. |
| **`research_synthesist`** | Síntesis de literatura científica, extracción de datos y matrices comparativas de estudios. |
| **`academic_statistician`** | Metodólogo bioestadístico: cálculo de tamaños de muestra, meta-análisis y modelos de regresión. |
| **`academic_narratologist`** | Redactor de prosa biomédica y académica de alto impacto bajo directrices ICMJE. |
| **`document_generator`** | Compilador de documentos Word (`.docx`) y formatos listos para publicación. |
| **`technical_writer`** | Documentación de software, guías técnicas para desarrolladores y manuales de arquitectura. |

---

## 🔄 Cómo Mantenerlo Actualizado

Para recibir nuevas habilidades, mejoras en los subagentes o actualizaciones de seguridad que suba a este repositorio:

```powershell
cd antigravity-setup
git pull origin main
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

---

## 📄 Licencia

Configuración y habilidades licenciadas bajo la licencia MIT.  
Creado con ❤️ para potenciar el desarrollo de software agéntico al máximo nivel.
