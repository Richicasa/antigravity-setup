<#
.SYNOPSIS
    Escáner de seguridad y antimalware para habilidades, repositorios y scripts de agentes de IA.
.DESCRIPTION
    Audita estáticamente archivos de habilidades (SKILL.md, scripts .ps1, .sh, .py, .js)
    en busca de exfiltración de credenciales, prompt injection, reverse shells, ofuscación
    y comandos destructivos.
.PARAMETER TargetPath
    Ruta a la carpeta de la habilidad o repositorio a auditar.
#>
param (
    [Parameter(Mandatory=$true)]
    [string]$TargetPath
)

if (!(Test-Path $TargetPath)) {
    Write-Error "La ruta especificada no existe: $TargetPath"
    exit 2
}

$threatPatterns = @(
    # --- CRITICAL: Reverse Shells & Shell Execution Injections ---
    @{ Category="REVERSE_SHELL"; Severity="CRITICAL"; Pattern='(?i)(/dev/tcp/|nc(\.exe)?\s+(-e|/bin/sh)|bash\s+-i\s+>&|mkfifo\s+/tmp/|socket\.socket.*pty\.spawn)'; Message="Posible Reverse Shell detectado" },
    @{ Category="OBFUSCATION_EXEC"; Severity="CRITICAL"; Pattern='(?i)(IEX\s*\(|Invoke-Expression|powershell(\.exe)?\s+-[eE](nc(odedcommand)?)?\s+[A-Za-z0-9+/=]{20,}|\[Convert\]::FromBase64String|base64\s+-d.*\|\s*(ba|z)?sh)'; Message="Ejecucion de codigo ofuscado o Base64 detectada" },
    @{ Category="DESTRUCTIVE_SYSTEM"; Severity="CRITICAL"; Pattern='(?i)(rm\s+-rf\s+([/~]|\$HOME)|Remove-Item.*-Recurse\s+.*[CDE]:\\|del\s+/[sfq]\s+[CDE]:\\Windows|format\s+[C-Z]:)'; Message="Comando de destruccion masiva de archivos o sistema" },
    @{ Category="DISABLE_DEFENDER"; Severity="CRITICAL"; Pattern='(?i)(Set-MpPreference.*-DisableRealtimeMonitoring|netsh\s+advfirewall.*state\s+off|sc\s+stop\s+WinDefend)'; Message="Intento de deshabilitar Windows Defender o Firewall" },

    # --- HIGH: Exfiltracion de Credenciales y Red Maliciosa ---
    @{ Category="EXFILTRATION_WEBHOOK"; Severity="HIGH"; Pattern='(?i)(discord(app)?\.com/api/webhooks|api\.telegram\.org/bot[0-9]+:|webhook\.site/[a-f0-9-]+|ngrok-free\.app|burpcollaborator)'; Message="Uso de webhooks o tuneles comunmente usados para exfiltracion" },
    @{ Category="CREDENTIAL_ACCESS"; Severity="HIGH"; Pattern='(?i)(\.ssh[\\/](id_rsa|id_ed25519|known_hosts)|\.aws[\\/]credentials|AppData[\\/]Roaming[\\/].*(Discord|Chrome|Edge)[\\/]Local Storage|System32[\\/]config[\\/](SAM|SYSTEM)|mimikatz)'; Message="Acceso directo a claves SSH, credenciales AWS o sesiones de navegador" },
    @{ Category="SUSPICIOUS_OUTBOUND_POST"; Severity="HIGH"; Pattern='(?i)((curl(\.exe)?|Invoke-WebRequest|Invoke-RestMethod)\s+.*(-X\s*POST|-Method\s*Post|--data).*\$(env:)?(TOKEN|KEY|PASS|SECRET|CRED))'; Message="Envio POST de variables de entorno confidenciales al exterior" },

    # --- HIGH / MEDIUM: Prompt Injections & Jailbreaks ---
    @{ Category="PROMPT_INJECTION"; Severity="HIGH"; Pattern='(?i)(ignore\s+(all\s+)?previous\s+instructions|disregard\s+(all\s+)?prior\s+(directives|instructions)|system\s+override:\s*you\s+must|you\s+are\s+now\s+unfiltered|bypass\s+safety\s+filters|jailbreak\s+activated)'; Message="Intento de Jailbreak / Prompt Injection en instrucciones del agente" },

    # --- MEDIUM: Llamadas de red genericas en scripts ---
    @{ Category="DYNAMIC_CODE_EXEC"; Severity="MEDIUM"; Pattern='(?i)(eval\(|exec\(|os\.system\(|subprocess\.Popen\(.*shell\s*=\s*True)'; Message="Ejecucion dinamica de strings mediante eval/exec/system" }
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "       AUDITORIA DE SEGURIDAD Y ANTIMALWARE PARA SKILLS   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Objetivo: $TargetPath" -ForegroundColor Gray
Write-Host ""

$files = Get-ChildItem -Path $TargetPath -Recurse -File | Where-Object {
    $_.Extension -match '(?i)\.(md|ps1|bat|cmd|sh|py|js|ts|json|yaml|yml|txt)$' -and
    $_.FullName -notmatch '[\\/]\.git[\\/]' -and
    $_.Name -ne 'scan_skill.ps1' -and
    $_.Name -ne 'threat-patterns.md'
}

$findings = @()
$criticalCount = 0
$highCount = 0
$mediumCount = 0

foreach ($file in $files) {
    $relativePath = $file.FullName.Replace($TargetPath, "")
    $lineNum = 0
    
    Get-Content -Path $file.FullName -ErrorAction SilentlyContinue | ForEach-Object {
        $lineNum++
        $line = $_
        
        foreach ($rule in $threatPatterns) {
            if ($line -match $rule.Pattern) {
                $finding = [PSCustomObject]@{
                    File = $relativePath
                    Line = $lineNum
                    Severity = $rule.Severity
                    Category = $rule.Category
                    Message = $rule.Message
                    Snippet = $line.Trim()
                }
                $findings += $finding
                
                if ($rule.Severity -eq "CRITICAL") { $criticalCount++ }
                elseif ($rule.Severity -eq "HIGH") { $highCount++ }
                elseif ($rule.Severity -eq "MEDIUM") { $mediumCount++ }
            }
        }
    }
}

if ($findings.Count -eq 0) {
    Write-Host "[OK] RESULTADO: SEGURO Y LIMPIO" -ForegroundColor Green
    Write-Host "No se encontraron firmas de malware, reverse shells, exfiltracion ni prompt injection." -ForegroundColor Gray
    Write-Host "Total archivos analizados: $($files.Count)" -ForegroundColor Gray
    exit 0
} else {
    Write-Host "ALERTA: Se han detectado $($findings.Count) hallazgos de seguridad:" -ForegroundColor Yellow
    Write-Host "  - Criticos : $criticalCount" -ForegroundColor Red
    Write-Host "  - Altos    : $highCount" -ForegroundColor Yellow
    Write-Host "  - Medios   : $mediumCount" -ForegroundColor White
    Write-Host ""
    
    foreach ($f in $findings) {
        $color = switch ($f.Severity) {
            "CRITICAL" { "Red" }
            "HIGH"     { "Yellow" }
            "MEDIUM"   { "Cyan" }
            Default    { "White" }
        }
        Write-Host "[$($f.Severity)] $($f.Category) en $($f.File):$($f.Line)" -ForegroundColor $color
        Write-Host "  Motivo : $($f.Message)" -ForegroundColor Gray
        $snip = if ($f.Snippet.Length -gt 100) { $f.Snippet.Substring(0, 100) + "..." } else { $f.Snippet }
        Write-Host "  Codigo : $snip" -ForegroundColor DarkGray
        Write-Host ""
    }
    
    if ($criticalCount -gt 0 -or $highCount -gt 0) {
        Write-Host "[X] VEREDICTO: RIESGO DE SEGURIDAD. INSTALACION RECHAZADA O REQUIERE REVISION HUMANA." -ForegroundColor Red
        exit 1
    } else {
        Write-Host "[!] VEREDICTO: ADVERTENCIA MENOR. Revisar hallazgos antes de ejecutar." -ForegroundColor Yellow
        exit 0
    }
}

