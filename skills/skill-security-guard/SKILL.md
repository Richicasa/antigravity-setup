---
name: skill-security-guard
description: >-
  Auditoría de seguridad y antimalware para habilidades, agentes y repositorios de GitHub antes de instalarlos o ejecutarlos. Escanea código malicioso, prompt injection, reverse shells, exfiltración de credenciales (SSH/AWS/.env), ejecución ofuscada y comandos destructivos.
---

# Skill Security Guard (Escáner Antimalware para Habilidades de IA)

Esta habilidad proporciona un protocolo defensivo estricto para auditar cualquier repositorio, habilidad (*skill*) o perfil de agente de GitHub **antes** de permitir su instalación o ejecución en la máquina local.

---

## 1. Protocolo de Instalación Segura (Cuarentena y Escaneo)

Siempre que se vaya a añadir o inspeccionar una habilidad de un repositorio externo de GitHub:

```
[Repositorio Externo GitHub]
           │
           ▼
[Paso 1: Descarga en Cuarentena Aislada]
($HOME\.gemini\antigravity\scratch\.quarantine\<skill-name>)
           │
           ▼
[Paso 2: Ejecución del Escáner Antimalware]
(scan_skill.ps1 -TargetPath <quarantine_path>)
           │
           ├────────────────────────────┐
           ▼                            ▼
[Veredicto: SEGURO (Código 0)]     [Veredicto: RIESGO (Código 1)]
           │                            │
           ▼                            ▼
[Paso 3: Mover a Global/Proyecto]  [Paso 3: BORRADO INMEDIATO Y ALERTA]
Instalación completada limpia.     Bloqueo total + Informe de amenazas.
```

---

## 2. Ejecución del Escáner

El script de escaneo estático heurístico se ubica en:
`scripts/scan_skill.ps1`

### Comando de Auditoría:
```powershell
& "$HOME\.gemini\config\skills\skill-security-guard\scripts\scan_skill.ps1" -TargetPath "<ruta_a_auditar>"
```

---

## 3. Matriz de Decisión y Acciones de Seguridad

| Nivel de Amenaza | Hallazgo Típico | Acción Obligatoria |
| :--- | :--- | :--- |
| **CRITICAL** | Reverse Shells, Base64 + IEX, borrado masivo de disco, desactivar Windows Defender. | **BLOQUEO INMEDIATO.** Eliminar carpeta de cuarentena. Nunca ejecutar. |
| **HIGH** | Webhooks Discord/Telegram de exfiltracion, lectura de claves de acceso, Prompt Injection agresivo. | **BLOQUEO POR DEFECTO.** Requiere aprobacion explicita y desinfeccion del codigo. |
| **MEDIUM** | Uso de funciones de ejecucion dinamica de strings o subprocesos con shell directo. | **ADVERTENCIA.** Revisar si el script tiene justificacion tecnica legitima. |
| **SAFE** | Sin patrones de ataque. | **APROBADO.** Proceder con la instalación. |

---

## 4. Escaneo Preventivo de Skills Existentes

Para auditar en cualquier momento todas las habilidades instaladas globalmente en tu máquina:
```powershell
Get-ChildItem -Path "$HOME\.gemini\config\skills" -Directory | ForEach-Object {
    & "$HOME\.gemini\config\skills\skill-security-guard\scripts\scan_skill.ps1" -TargetPath $_.FullName
}
```
