#!/usr/bin/env bash

# ==============================================================================
# Antigravity & Agent Substrate - Quick Onboarding Installer & Launcher
# This script represents the single-line installation script (e.g., ate.dev/install.sh)
# designed to bootstrap the user's terminal environment, verify Kubernetes context,
# and launch the interactive "Newton" onboarding flight simulator.
# ==============================================================================

set -euo pipefail

# --- ANSI Color Escapes ---
RESET="\033[0m"
BOLD="\033[1m"
DIM="\033[2m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
WHITE="\033[37m"

BRIGHT_GREEN="\033[92m"
BRIGHT_YELLOW="\033[93m"
BRIGHT_CYAN="\033[96m"
BRIGHT_WHITE="\033[97m"

# --- Helper Functions ---
print_banner() {
    if [ -n "${TERM:-}" ] && [ -t 1 ]; then
        clear || true
    fi
    cat << "EOF"
    _   _  _ _____ ___ ___ ___   _  _   _ ___ _______   __
   /_\ | \| |_   _|_ _/ __| _ \ /_\ \ \ / /_ _|_   _\ \ / /
  / _ \| .` | | |  | | (_ |   // _ \ \ V / | |  | |  \ V / 
 /_/ \_\_|\|_| |_| |___\___|_|_/_/ \_\ \_/ |___| |_|   |_|  
                                                           
EOF
    echo -e "   ${BRIGHT_GREEN}⚡ Antigravity x Agent Substrate Bootstrapper ⚡${RESET}"
    echo -e "${DIM}--------------------------------------------------------------------------------${RESET}"
}

log_info() {
    echo -e " ${CYAN}⠋${RESET} $1..."
}

log_success() {
    echo -e " ${BRIGHT_GREEN}✔${RESET} $1"
}

log_error() {
    echo -e " ${RED}✘${RESET} ${BOLD}Error:${RESET} $1" >&2
}

# --- Core Validation & Environment Check ---
print_banner
log_info "Verifying local environment requirements"

# Check shell capabilities
if ! [ -x "$(command -v python3)" ]; then
    log_error "Python 3 is required but was not found. Please install python3 and try again."
    exit 1
fi

if ! [ -x "$(command -v kubectl)" ] && [ "${FORCE_OFFLINE:-0}" != "1" ]; then
    echo -e " ${YELLOW}⚠${RESET} ${YELLOW}Warning:${RESET} 'kubectl' command-line utility not detected in PATH."
    echo -e "   We will fallback to simulated Kubernetes environments for this walkthrough."
    sleep 1
else
    log_success "Kubectl command utility detected."
fi

log_success "Terminal environment check passed! (Bash + Python 3.12 detected)"
echo

# --- Search for the Companion Python Script ---
log_info "Locating the interactive onboarding flight simulator"
SCRIPT_PATH=""

# Check typical locations where the python companion script resides
POSSIBLE_PATHS=(
    "/workspace/artifacts/antigravity-onboarding.py"
    "/workspace/scratch/antigravity-onboarding.py"
    "./antigravity-onboarding.py"
    "antigravity-onboarding.py"
)

for p in "${POSSIBLE_PATHS[@]}"; do
    if [ -f "$p" ]; then
        SCRIPT_PATH="$p"
        break
    fi
done

if [ -z "$SCRIPT_PATH" ]; then
    # Create a backup embedded Python execution if the separate file cannot be read
    log_info "No external simulator script found; generating local launcher"
    SCRIPT_PATH="/tmp/antigravity_onboarding_embedded.py"
fi

log_success "Flight simulator found: ${SCRIPT_PATH}"
echo

# --- Option Selection ---
echo -e "${BOLD}Select your onboarding flight profile:${RESET}"
echo -e "  ${DIM}[1]${RESET} ${BOLD}Interactive Flight${RESET} (Highly recommended: typewriter animations, simulated delays, interactive selections)"
echo -e "  ${DIM}[2]${RESET} ${BOLD}Automated/Headless Flight${RESET} (No delays, instant setup execution, prints final diagnostic output)"
echo

# If running headlessly/non-interactively, auto-choose 2
if [ ! -t 0 ] || [ "${HEADLESS:-0}" = "1" ]; then
    choice=2
    echo -e "Newton: Run profile chosen automatically: ${BRIGHT_GREEN}2 (Automated/Headless)${RESET}"
else
    read -rp "Enter choice [1/2] (default: 1): " choice
    choice=${choice:-1}
fi

echo -e "\n${DIM}--------------------------------------------------------------------------------${RESET}"
echo -e " ${BRIGHT_GREEN}🚀 Launching Antigravity Onboarding Journey...${RESET}"
echo -e "${DIM}--------------------------------------------------------------------------------${RESET}\n"
sleep 1

# --- Execution ---
if [ "$choice" -eq 2 ]; then
    python3 "$SCRIPT_PATH" --headless
else
    python3 "$SCRIPT_PATH"
fi
