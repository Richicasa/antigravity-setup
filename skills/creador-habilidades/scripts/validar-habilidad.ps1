<#
.SYNOPSIS
    Validador de conformidad de habilidades para Google Antigravity.
.DESCRIPTION
    Inspecciona la carpeta de una habilidad para verificar:
    1. Existencia del archivo SKILL.md.
    2. Validez del frontmatter YAML (campos 'name' y 'description').
    3. Formato del campo 'name' (minúsculas y guiones).
    4. Criterios de longitud del campo 'description'.
    5. Integridad de los enlaces relativos a archivos locales (references, templates, scripts, etc.).
.PARAMETER RutaHabilidad
    Ruta a la carpeta de la habilidad a inspeccionar. Por defecto es el directorio actual o padre del script.
#>

param(
    [string]$RutaHabilidad = ""
)

if ([string]::IsNullOrWhiteSpace($RutaHabilidad)) {
    # Por defecto, evaluar la carpeta contenedora de scripts/ (la raíz de la habilidad)
    $RutaHabilidad = Split-Path -Parent $PSScriptRoot
    if (-not (Test-Path (Join-Path $RutaHabilidad "SKILL.md"))) {
        $RutaHabilidad = Get-Location
    }
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Validador de Habilidades para Google Antigravity" -ForegroundColor Cyan
Write-Host "  Ruta analizada: $RutaHabilidad" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$errores = 0
$advertencias = 0

# 1. Verificar existencia de SKILL.md
$skillMdPath = Join-Path $RutaHabilidad "SKILL.md"
if (-not (Test-Path $skillMdPath)) {
    Write-Host "[ERROR] No se encontró el archivo obligatorio SKILL.md en: $RutaHabilidad" -ForegroundColor Red
    exit 1
} else {
    Write-Host "[OK] Archivo SKILL.md encontrado." -ForegroundColor Green
}

$contenido = Get-Content -Raw -Encoding UTF8 -Path $skillMdPath

# 2. Verificar delimitadores de YAML Frontmatter
if (-not ($contenido -match "^---\r?\n([\s\S]*?)\r?\n---")) {
    Write-Host "[ERROR] El archivo SKILL.md no comienza con un bloque de frontmatter YAML delimitado por '---'." -ForegroundColor Red
    $errores++
} else {
    Write-Host "[OK] Delimitadores YAML frontmatter presentes." -ForegroundColor Green
    $yamlBlock = $matches[1]

    # 3. Validar campo 'name'
    if ($yamlBlock -match "name:\s*([^\r\n]+)") {
        $name = $matches[1].Trim()
        if ($name -match "^[a-z0-9-]+$") {
            Write-Host "[OK] Campo 'name' valido: '$name'" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] El campo 'name' ('$name') debe contener solo minúsculas, números y guiones (sin espacios ni mayúsculas)." -ForegroundColor Red
            $errores++
        }
    } else {
        Write-Host "[ERROR] Falta el campo obligatorio 'name' en el frontmatter." -ForegroundColor Red
        $errores++
    }

    # 4. Validar campo 'description'
    if ($yamlBlock -match "description:\s*(?:>-|\|-|>|\|)?\s*\r?\n?([\s\S]+?)(?=\n[a-z0-9_-]+:|\Z)") {
        $desc = $matches[1].Trim()
        if ($desc.Length -ge 30) {
            Write-Host "[OK] Campo 'description' presente ($($desc.Length) caracteres)." -ForegroundColor Green
        } else {
            Write-Host "[ADVERTENCIA] La descripción es muy corta ($($desc.Length) caracteres). Debe ser lo bastante detallada para que el agente la active correctamente." -ForegroundColor Yellow
            $advertencias++
        }
    } else {
        Write-Host "[ERROR] Falta el campo obligatorio 'description' en el frontmatter." -ForegroundColor Red
        $errores++
    }
}

# 5. Validar enlaces relativos a archivos locales en SKILL.md
$enlaces = [regex]::Matches($contenido, '\[([^\]]+)\]\((?!https?:\/\/)([^)#\s]+)(?:#[^\)]*)?\)')
Write-Host "`nVerificando enlaces relativos en SKILL.md..." -ForegroundColor Cyan

$enlacesValidados = 0
foreach ($enlace in $enlaces) {
    $texto = $enlace.Groups[1].Value
    $rutaRelativa = $enlace.Groups[2].Value

    # Normalizar separadores de ruta
    $rutaNormalizada = $rutaRelativa.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
    $rutaDestino = Join-Path $RutaHabilidad $rutaNormalizada

    if (Test-Path $rutaDestino) {
        Write-Host "  [OK] Enlace '$texto' -> '$rutaRelativa'" -ForegroundColor Green
        $enlacesValidados++
    } else {
        Write-Host "  [ERROR] Enlace roto: '$texto' apunta a '$rutaRelativa', pero el archivo no existe en '$rutaDestino'" -ForegroundColor Red
        $errores++
    }
}

Write-Host "`n--------------------------------------------------"
if ($errores -eq 0) {
    Write-Host "Resultado: HABILIDAD VALIDA ($enlacesValidados enlaces comprobados, $advertencias advertencias)." -ForegroundColor Green
    exit 0
} else {
    Write-Host "Resultado: SE ENCONTRARON $errores ERRORES en la habilidad." -ForegroundColor Red
    exit 1
}
