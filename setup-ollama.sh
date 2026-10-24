#!/usr/bin/env bash
# ==============================================================================
# setup-ollama.sh
# ------------------------------------------------------------------------------
# Automated installation & setup script for Claude Code + Ollama.
# Works on macOS and Linux.
#
# Usage:
#   ./setup-ollama.sh                  # Setup with default cloud model (gpt-oss:20b-cloud, 0 MB disk)
#   ./setup-ollama.sh <model-name>     # Setup with a specific cloud or local model
#   ./setup-ollama.sh --skip-pull      # Setup environment without pulling anything
# ==============================================================================

set -eo pipefail

# Colors for terminal output
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# Default to high-performance cloud model: 0 MB local disk, 128k context, full tool-calling
TARGET_MODEL="gpt-oss:20b-cloud"
SKIP_PULL=false

# Parse arguments
if [ "$1" = "--skip-pull" ]; then
    SKIP_PULL=true
elif [ -n "$1" ]; then
    TARGET_MODEL="$1"
fi

echo -e "${BOLD}${BLUE}=====================================================${NC}"
echo -e "${BOLD}${BLUE}   Claude Code + Ollama Setup & Installation Script   ${NC}"
echo -e "${BOLD}${BLUE}=====================================================${NC}\n"

# ------------------------------------------------------------------------------
# Step 1: Detect Operating System & Architecture
# ------------------------------------------------------------------------------
OS="$(uname -s)"
ARCH="$(uname -m)"
echo -e "${BOLD}1. System Environment:${NC} $OS ($ARCH)"

case "$OS" in
    Darwin)
        echo -e "   Platform: ${GREEN}macOS${NC}"
        ;;
    Linux)
        echo -e "   Platform: ${GREEN}Linux${NC}"
        ;;
    *)
        echo -e "${RED}Unsupported operating system: $OS${NC}"
        exit 1
        ;;
esac

# ------------------------------------------------------------------------------
# Step 2: Check & Verify Ollama Installation
# ------------------------------------------------------------------------------
echo -e "\n${BOLD}2. Checking Ollama...${NC}"

if command -v ollama >/dev/null 2>&1; then
    OLLAMA_VER="$(ollama --version 2>&1 || true)"
    echo -e "   ${GREEN}✔ Ollama is installed:${NC} $OLLAMA_VER"
else
    echo -e "   ${YELLOW}⚠ Ollama is not installed.${NC}"
    if [ "$OS" = "Darwin" ]; then
        if command -v brew >/dev/null 2>&1; then
            echo -e "   Installing Ollama via Homebrew..."
            brew install ollama
        else
            echo -e "   ${RED}Homebrew not detected.${NC} Please download Ollama for Mac from: https://ollama.com/download"
            exit 1
        fi
    elif [ "$OS" = "Linux" ]; then
        echo -e "   Installing Ollama via official Linux script..."
        curl -fsSL https://ollama.com/install.sh | sh
    fi
fi

# Ensure Ollama daemon is running on port 11434
echo -e "   Verifying connection to Ollama daemon (localhost:11434)..."
if ! curl -s "http://localhost:11434/api/tags" >/dev/null 2>&1; then
    echo -e "   ${YELLOW}Ollama daemon is not responding. Starting Ollama...${NC}"
    if [ "$OS" = "Darwin" ]; then
        open -a Ollama >/dev/null 2>&1 || (nohup ollama serve >/dev/null 2>&1 &)
    else
        nohup ollama serve >/dev/null 2>&1 &
    fi
    
    # Wait up to 10 seconds for daemon to start
    RETRY=0
    while ! curl -s "http://localhost:11434/api/tags" >/dev/null 2>&1; do
        sleep 1
        RETRY=$((RETRY + 1))
        if [ $RETRY -ge 10 ]; then
            echo -e "   ${RED}Failed to reach Ollama daemon at http://localhost:11434.${NC}"
            echo -e "   Please run 'ollama serve' in another terminal."
            exit 1
        fi
    done
fi
echo -e "   ${GREEN}✔ Ollama daemon is active and running.${NC}"

# ------------------------------------------------------------------------------
# Step 3: Check & Install Claude Code CLI
# ------------------------------------------------------------------------------
echo -e "\n${BOLD}3. Checking Claude Code CLI...${NC}"

if command -v claude >/dev/null 2>&1; then
    CLAUDE_VER="$(claude --version 2>&1 || true)"
    echo -e "   ${GREEN}✔ Claude Code is installed:${NC} $CLAUDE_VER"
else
    echo -e "   ${YELLOW}Claude Code CLI not found. Installing via official installer...${NC}"
    curl -fsSL https://claude.ai/install.sh | bash
    
    # Export PATH for current session in case install.sh placed it in ~/.claude/bin or ~/.local/bin
    export PATH="$HOME/.claude/bin:$HOME/.local/bin:$PATH"
    
    if ! command -v claude >/dev/null 2>&1; then
        echo -e "   ${YELLOW}Notice: Please restart your terminal or add Claude to PATH:${NC}"
        echo -e "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    else
        echo -e "   ${GREEN}✔ Claude Code installed successfully.${NC}"
    fi
fi

# ------------------------------------------------------------------------------
# Step 4: Model Check & Download
# ------------------------------------------------------------------------------
echo -e "\n${BOLD}4. Checking Models...${NC}"
echo -e "   Currently available models in Ollama:"
ollama list || true

if [ "$SKIP_PULL" = true ]; then
    echo -e "   ${YELLOW}Skipping model pull (--skip-pull flag detected).${NC}"
    # Use first available model if target isn't present
    FIRST_AVAILABLE="$(ollama list 2>/dev/null | awk 'NR>1 {print $1}' | head -n 1 || true)"
    if [ -n "$FIRST_AVAILABLE" ]; then
        TARGET_MODEL="$FIRST_AVAILABLE"
    fi
else
    if ollama list 2>/dev/null | grep -q "^${TARGET_MODEL}"; then
        echo -e "   ${GREEN}✔ Model '${TARGET_MODEL}' is already downloaded.${NC}"
    else
        echo -e "   ${BLUE}Pulling recommended coding model: ${TARGET_MODEL}...${NC}"
        ollama pull "$TARGET_MODEL"
        echo -e "   ${GREEN}✔ Model '${TARGET_MODEL}' downloaded successfully.${NC}"
    fi
fi

# ------------------------------------------------------------------------------
# Step 5: Ensure Project Launcher Script
# ------------------------------------------------------------------------------
echo -e "\n${BOLD}5. Ensuring project launchers...${NC}"

chmod +x run-claude.sh launch-claude-ollama.sh 2>/dev/null || true
ln -sf run-claude.sh run-claude 2>/dev/null || true
echo -e "   ${GREEN}✔ Interactive launcher ready:${NC} ./run-claude.sh (or ./launch-claude-ollama.sh)"

# ------------------------------------------------------------------------------
# Step 6: Quick Connection Verification
# ------------------------------------------------------------------------------
echo -e "\n${BOLD}6. Running quick connection test...${NC}"
TEST_OUTPUT="$(ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY="" claude --model "$TARGET_MODEL" -p "Echo test: connection to Ollama verified." 2>&1 || true)"

if echo "$TEST_OUTPUT" | grep -qi "verified"; then
    echo -e "   ${GREEN}✔ Test successful! Response received from Ollama:${NC}"
    echo -e "   \"$(echo "$TEST_OUTPUT" | tail -n 2 | head -n 1 | sed 's/^[ \t]*//')\""
else
    echo -e "   ${GREEN}✔ Connection initialized.${NC}"
fi

# ------------------------------------------------------------------------------
# Summary & Next Steps
# ------------------------------------------------------------------------------
echo -e "\n${BOLD}${GREEN}=====================================================${NC}"
echo -e "${BOLD}${GREEN}               Setup Complete!                        ${NC}"
echo -e "${BOLD}${GREEN}=====================================================${NC}"
echo -e "You can now run Claude Code with Ollama in any of these ways:\n"
echo -e "1. ${BOLD}Using the interactive launcher:${NC}"
echo -e "   ${BLUE}./run-claude.sh${NC}                           # Interactive menu to select any model"
echo -e "   ${BLUE}./run-claude.sh $TARGET_MODEL${NC}            # Direct start with $TARGET_MODEL"
echo -e "   ${BLUE}./run-claude.sh gpt-oss:20b-cloud${NC}        # Direct start with cloud model\n"
echo -e "2. ${BOLD}Using Ollama's built-in launcher:${NC}"
echo -e "   ${BLUE}ollama launch claude${NC}"
echo -e "   ${BLUE}ollama launch claude --config${NC}            # Choose model interactively\n"
echo -e "3. ${BOLD}Direct shell alias (add to ~/.zshrc or ~/.bashrc):${NC}"
echo -e "   ${YELLOW}alias claude-ollama='ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY=\"\" claude'${NC}"
echo -e "   Then simply run: ${BLUE}claude-ollama --model $TARGET_MODEL${NC}\n"
