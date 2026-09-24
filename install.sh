#!/usr/bin/env bash
# ==============================================================================
# Antigravity Pro Suite - Automated Bootstrap Installer (macOS & Linux)
# Configuración global, herramientas de desarrollo, skills y carga progresiva
# ==============================================================================

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${MAGENTA}==================================================================${NC}"
echo -e "${MAGENTA}        🚀 ANTIGRAVITY PRO SUITE - INSTALADOR AUTOMÁTICO 🚀      ${NC}"
echo -e "${MAGENTA}==================================================================${NC}"
echo -e "Equipando tu máquina con:"
echo -e "  • Herramientas de desarrollo esenciales (Git, Node, Python3, GitHub CLI)"
echo -e "  • 45 Habilidades (Skills) globales auditadas y optimizadas"
echo -e "  • 6 Subagentes especializados de alto rendimiento"
echo -e "  • Protocolo de Ingeniería Global y Gate de Seguridad Antimalware"
echo -e "  • Arquitectura de Carga Progresiva (Cero saturación de contexto)"
echo -e "${MAGENTA}==================================================================${NC}\n"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ------------------------------------------------------------------------------
# 1. Verificación e Instalación de Herramientas Base
# ------------------------------------------------------------------------------
echo -e "${CYAN}[+] Paso 1: Verificando herramientas de desarrollo base...${NC}"

check_cmd() {
    command -v "$1" >/dev/null 2>&1
}

OS_TYPE="$(uname -s)"

if [ "$OS_TYPE" = "Darwin" ]; then
    echo -e "    [*] Detectado macOS."
    if ! check_cmd brew; then
        echo -e "    ${YELLOW}[!] Homebrew no está instalado. Te recomendamos instalarlo desde https://brew.sh${NC}"
    else
        for pkg in git gh node python@3.12; do
            if ! brew list "$pkg" >/dev/null 2>&1; then
                echo -e "    [*] Instalando $pkg vía Homebrew..."
                brew install "$pkg" || true
            else
                echo -e "    ${GREEN}[OK] $pkg ya está instalado.${NC}"
            fi
        done
    fi
elif [ "$OS_TYPE" = "Linux" ]; then
    echo -e "    [*] Detectado Linux."
    if check_cmd apt-get; then
        echo -e "    [*] Verificando paquetes en Debian/Ubuntu..."
        sudo apt-get update -y || true
        sudo apt-get install -y git gh nodejs npm python3 python3-pip || true
    else
        echo -e "    ${YELLOW}[!] Gestor de paquetes no reconocido automáticamente. Verifica tener git, node, python3 y gh.${NC}"
    fi
fi

# ------------------------------------------------------------------------------
# 2. Configuración de Directorios de Antigravity
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}[+] Paso 2: Preparando estructura de directorios en \$HOME...${NC}"

GEMINI_DIR="$HOME/.gemini"
GEMINI_CONFIG_DIR="$GEMINI_DIR/config"
GEMINI_SKILLS_DIR="$GEMINI_CONFIG_DIR/skills"

AGENTS_DIR="$HOME/.agents"
AGENTS_SKILLS_DIR="$AGENTS_DIR/skills"
AGENTS_SUBAGENTS_DIR="$AGENTS_DIR/agents"

mkdir -p "$GEMINI_CONFIG_DIR" "$GEMINI_SKILLS_DIR" "$AGENTS_DIR" "$AGENTS_SKILLS_DIR" "$AGENTS_SUBAGENTS_DIR"
echo -e "    ${GREEN}[OK] Estructura de directorios lista.${NC}"

# ------------------------------------------------------------------------------
# 3. Instalación de Configuración Global y Protocolo AGENTS.md
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}[+] Paso 3: Desplegando configuración y protocolo global...${NC}"

if [ -f "$SCRIPT_DIR/config/AGENTS.md" ]; then
    cp -f "$SCRIPT_DIR/config/AGENTS.md" "$GEMINI_CONFIG_DIR/AGENTS.md"
    cp -f "$SCRIPT_DIR/config/AGENTS.md" "$AGENTS_DIR/AGENTS.md"
    echo -e "    ${GREEN}[OK] Protocolo AGENTS.md desplegado.${NC}"
fi

if [ -f "$SCRIPT_DIR/config/config.json" ]; then
    cp -f "$SCRIPT_DIR/config/config.json" "$GEMINI_CONFIG_DIR/config.json"
    echo -e "    ${GREEN}[OK] Archivo config.json desplegado.${NC}"
fi

# ------------------------------------------------------------------------------
# 4. Despliegue de 45 Skills con Carga Progresiva
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}[+] Paso 4: Desplegando 45 habilidades globales (Skills)...${NC}"

if [ -d "$SCRIPT_DIR/skills" ]; then
    cp -Rf "$SCRIPT_DIR/skills/"* "$GEMINI_SKILLS_DIR/"
    cp -Rf "$SCRIPT_DIR/skills/"* "$AGENTS_SKILLS_DIR/"
    SKILL_COUNT=$(find "$SCRIPT_DIR/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
    echo -e "    ${GREEN}[OK] $SKILL_COUNT habilidades globales desplegadas con soporte de carga progresiva.${NC}"
fi

# ------------------------------------------------------------------------------
# 5. Despliegue de Subagentes Especializados
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}[+] Paso 5: Desplegando subagentes especializados...${NC}"

if [ -d "$SCRIPT_DIR/agents" ]; then
    cp -Rf "$SCRIPT_DIR/agents/"* "$AGENTS_SUBAGENTS_DIR/"
    AGENT_COUNT=$(find "$SCRIPT_DIR/agents" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
    echo -e "    ${GREEN}[OK] $AGENT_COUNT subagentes especializados desplegados en ~/.agents/agents/.${NC}"
fi

# ------------------------------------------------------------------------------
# 6. Resumen Final
# ------------------------------------------------------------------------------
echo -e "\n${GREEN}==================================================================${NC}"
echo -e "${GREEN}          🎉 ¡INSTALACIÓN COMPLETADA CON ÉXITO! 🎉               ${NC}"
echo -e "${GREEN}==================================================================${NC}"
echo -e "Tu entorno Antigravity cuenta ahora con:"
echo -e "  1. ${YELLOW}Carga Progresiva:${NC} Las 45 habilidades no consumen tokens innecesarios."
echo -e "  2. ${YELLOW}Protocolo Global:${NC} Flujo estructurado Brainstorming -> Planning -> TDD -> Verification."
echo -e "  3. ${YELLOW}Escudo de Seguridad:${NC} Auditoría antimalware en ~/.gemini/config/skills/skill-security-guard."
echo -e "\n¡Listo para crear software a la máxima velocidad!"
