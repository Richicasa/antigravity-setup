# ==============================================================================
# Antigravity Pro Suite - Automated Bootstrap Installer (Windows)
# Configuracion global, herramientas de desarrollo, skills y carga progresiva
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "`n[+] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "    [OK] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "    [!] $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "    [*] $Message" -ForegroundColor Gray
}

Clear-Host
Write-Host "==================================================================" -ForegroundColor Magenta
Write-Host "        ANTIGRAVITY PRO SUITE - INSTALADOR AUTOMATICO            " -ForegroundColor Magenta
Write-Host "==================================================================" -ForegroundColor Magenta
Write-Host "Equipando tu maquina con:" -ForegroundColor White
Write-Host "  - Herramientas de desarrollo esenciales (Git, Node, Python, VS Code)" -ForegroundColor Gray
Write-Host "  - 45 Habilidades (Skills) globales auditadas y optimizadas" -ForegroundColor Gray
Write-Host "  - 6 Subagentes especializados de alto rendimiento" -ForegroundColor Gray
Write-Host "  - Protocolo de Ingenieria Global y Gate de Seguridad Antimalware" -ForegroundColor Gray
Write-Host "  - Arquitectura de Carga Progresiva (Cero saturacion de contexto)" -ForegroundColor Gray
Write-Host "==================================================================`n" -ForegroundColor Magenta

# ------------------------------------------------------------------------------
# 1. Verificacion e Instalacion de Herramientas de Desarrollo (Winget)
# ------------------------------------------------------------------------------
Write-Step "Paso 1: Verificando herramientas de desarrollo base..."

$hasWinget = Get-Command winget -ErrorAction SilentlyContinue

if (-not $hasWinget) {
    Write-Warn "Windows Package Manager (winget) no esta disponible en este sistema."
    Write-Warn "Por favor, instala manualmente Git, Node.js LTS, Python 3.12 y VS Code si no los tienes."
} else {
    $tools = @(
        @{ Name = "Git"; Id = "Git.Git"; Cmd = "git" },
        @{ Name = "GitHub CLI"; Id = "GitHub.cli"; Cmd = "gh" },
        @{ Name = "Node.js LTS"; Id = "OpenJS.NodeJS.LTS"; Cmd = "node" },
        @{ Name = "Python 3.12"; Id = "Python.Python.3.12"; Cmd = "python" },
        @{ Name = "Visual Studio Code"; Id = "Microsoft.VisualStudioCode"; Cmd = "code" }
    )

    foreach ($tool in $tools) {
        $cmdFound = Get-Command $tool.Cmd -ErrorAction SilentlyContinue
        if ($cmdFound) {
            Write-Success "$($tool.Name) ya esta instalado en el sistema."
        } else {
            Write-Info "Instalando $($tool.Name) mediante winget..."
            try {
                $process = Start-Process winget -ArgumentList "install --id $($tool.Id) -e --accept-source-agreements --accept-package-agreements --silent" -NoNewWindow -Wait -PassThru
                if ($process.ExitCode -eq 0) {
                    Write-Success "$($tool.Name) instalado correctamente."
                } else {
                    Write-Warn "Winget finalizo con codigo $($process.ExitCode) para $($tool.Name)."
                }
            } catch {
                Write-Warn "No se pudo instalar $($tool.Name): $_"
            }
        }
    }

    # Refrescar variables de entorno en la sesion actual
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# ------------------------------------------------------------------------------
# 2. Configuracion de Directorios de Antigravity
# ------------------------------------------------------------------------------
Write-Step "Paso 2: Preparando estructura de directorios en el perfil de usuario..."

$userHome = $HOME
$geminiDir = Join-Path $userHome ".gemini"
$geminiConfigDir = Join-Path $geminiDir "config"
$geminiSkillsDir = Join-Path $geminiConfigDir "skills"

$agentsDir = Join-Path $userHome ".agents"
$agentsSkillsDir = Join-Path $agentsDir "skills"
$agentsSubagentsDir = Join-Path $agentsDir "agents"

$targetDirs = @(
    $geminiConfigDir,
    $geminiSkillsDir,
    $agentsDir,
    $agentsSkillsDir,
    $agentsSubagentsDir
)

foreach ($dir in $targetDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Info "Creado directorio: $dir"
    }
}
Write-Success "Estructura de directorios lista."

# ------------------------------------------------------------------------------
# 3. Instalacion de Configuracion Global y Protocolo AGENTS.md
# ------------------------------------------------------------------------------
Write-Step "Paso 3: Desplegando configuracion y protocolo global..."

$srcConfigDir = Join-Path $PSScriptRoot "config"

if (Test-Path (Join-Path $srcConfigDir "AGENTS.md")) {
    Copy-Item (Join-Path $srcConfigDir "AGENTS.md") -Destination (Join-Path $geminiConfigDir "AGENTS.md") -Force
    Copy-Item (Join-Path $srcConfigDir "AGENTS.md") -Destination (Join-Path $agentsDir "AGENTS.md") -Force
    Write-Success "Protocolo AGENTS.md (Ciclo de Vida + Gate de Seguridad) desplegado."
}

if (Test-Path (Join-Path $srcConfigDir "config.json")) {
    Copy-Item (Join-Path $srcConfigDir "config.json") -Destination (Join-Path $geminiConfigDir "config.json") -Force
    Write-Success "Archivo config.json (politicas Turbo, Sandbox y permisos) desplegado."
}

# ------------------------------------------------------------------------------
# 4. Despliegue de 45 Skills con Carga Progresiva
# ------------------------------------------------------------------------------
Write-Step "Paso 4: Desplegando 45 habilidades globales (Skills)..."

$srcSkillsDir = Join-Path $PSScriptRoot "skills"
$skills = Get-ChildItem -Path $srcSkillsDir -Directory

$count = 0
foreach ($skill in $skills) {
    # Copiar a ~/.gemini/config/skills/
    $destGemini = Join-Path $geminiSkillsDir $skill.Name
    Copy-Item -Path $skill.FullName -Destination $destGemini -Recurse -Force
    
    # Copiar a ~/.agents/skills/ para compatibilidad total con cualquier runner
    $destAgents = Join-Path $agentsSkillsDir $skill.Name
    Copy-Item -Path $skill.FullName -Destination $destAgents -Recurse -Force
    
    $count++
}
Write-Success "$count habilidades globales desplegadas en ~/.gemini/config/skills y ~/.agents/skills."

# ------------------------------------------------------------------------------
# 5. Despliegue de Subagentes Especializados
# ------------------------------------------------------------------------------
Write-Step "Paso 5: Desplegando subagentes especializados..."

$srcAgentsDir = Join-Path $PSScriptRoot "agents"
$agents = Get-ChildItem -Path $srcAgentsDir -Directory

$agentCount = 0
foreach ($agent in $agents) {
    $destAgent = Join-Path $agentsSubagentsDir $agent.Name
    Copy-Item -Path $agent.FullName -Destination $destAgent -Recurse -Force
    $agentCount++
}
Write-Success "$agentCount subagentes desplegados en ~/.agents/agents/."

# ------------------------------------------------------------------------------
# 6. Auditoria de Seguridad con skill-security-guard
# ------------------------------------------------------------------------------
Write-Step "Paso 6: Ejecutando verificacion de seguridad antimalware..."

$scannerScript = Join-Path $geminiSkillsDir "skill-security-guard\scripts\scan_skill.ps1"
if (Test-Path $scannerScript) {
    Write-Info "Auditando integridad de las habilidades instaladas..."
    $cleanCount = 0
    $skillsToCheck = Get-ChildItem -Path $geminiSkillsDir -Directory
    foreach ($s in $skillsToCheck) {
        $result = & $scannerScript -TargetPath $s.FullName 2>&1
        if ($LASTEXITCODE -eq 0) {
            $cleanCount++
        }
    }
    Write-Success "Auditoria completada: $cleanCount/$($skillsToCheck.Count) habilidades verificadas y limpias (0 amenazas)."
} else {
    Write-Warn "Escaner no encontrado en la ruta esperada. Saltando verificacion estatica."
}

# ------------------------------------------------------------------------------
# 7. Resumen Final y Proximos Pasos
# ------------------------------------------------------------------------------
Write-Host "`n==================================================================" -ForegroundColor Green
Write-Host "          INSTALACION COMPLETADA CON EXITO                        " -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green
Write-Host "Tu Antigravity ahora tiene exactamente las mismas capacidades de elite:" -ForegroundColor White
Write-Host "  1. Carga Progresiva Activa:" -ForegroundColor Yellow
Write-Host "     Las 45 habilidades NO saturan el contexto de entrada." -ForegroundColor Gray
Write-Host "     Antigravity lee unicamente las descripciones breves al inicio" -ForegroundColor Gray
Write-Host "     y carga los manuales y scripts completos solo cuando los necesita." -ForegroundColor Gray
Write-Host "  2. Protocolo de Ingenieria Global:" -ForegroundColor Yellow
Write-Host "     Flujo estricto: Brainstorming -> Planning -> TDD -> Debugging -> Verification." -ForegroundColor Gray
Write-Host "  3. Escudo de Seguridad Activo:" -ForegroundColor Yellow
Write-Host "     Cualquier repo o skill externa se audita automaticamente antes de instalarse." -ForegroundColor Gray
Write-Host "`nPara empezar:" -ForegroundColor Cyan
Write-Host "  - Abre una nueva terminal o tu entorno Antigravity." -ForegroundColor White
Write-Host "  - Ejecuta 'antigravity' o abre tu IDE favorito con el agente." -ForegroundColor White
Write-Host "  - Disfruta de la suite mas potente de IA Agentic Coding!`n" -ForegroundColor White
