# Ejemplo de Referencia: Habilidad Completa de Despliegue

Este ejemplo ilustra cómo se estructura una habilidad real conforme a los estándares de Antigravity.

---

### Archivo: `SKILL.md`

```markdown
---
name: despliegue-servicio-web
description: >-
  Automatiza el empaquetado, pruebas previas y despliegue de microservicios web en servidores de producción.
  Activa esta habilidad cuando el usuario pida desplegar a producción, publicar un release de la aplicación,
  o ejecutar la canalización de entrega continua del servicio web. No usar para despliegues en desarrollo local.
---

# Despliegue de Servicio Web

Esta habilidad guía y automatiza el flujo de publicación del servicio web, garantizando que no se publiquen compilaciones rotas.

---

## 1. Verificación Previa

Antes de iniciar, ejecuta la validación del entorno:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/verificar-entorno.ps1
```

Si algún componente falla, consulta la guía en [Guía de Solución de Entorno](references/solucion-entorno.md).

---

## 2. Flujo Operativo de Despliegue

### Paso 1: Ejecución de la Suite de Pruebas
Valida que todos los tests unitarios y de integración pasen sin errores:
```bash
npm test -- --coverage
```

### Paso 2: Compilación de Artefactos
Genera la versión optimizada para producción:
```bash
npm run build
```

### Paso 3: Despliegue en el Servidor
Sube el paquete compilado mediante el script automatizado:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/publicar.ps1 -Ambiente "produccion"
```

---

## 3. Verificación Post-Despliegue

Envía una solicitud al endpoint de salud y verifica la respuesta:
```bash
curl -f -s https://api.midominio.com/health
```
Criterio de éxito: Debe responder código HTTP `200` y cuerpo `{"status": "healthy"}`.
```
