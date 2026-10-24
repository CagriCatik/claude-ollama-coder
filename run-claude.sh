#!/usr/bin/env bash
# ==============================================================================
# run-claude.sh
# Interactive launcher for Claude Code with local or cloud models served by Ollama.
# ==============================================================================

set -e

# Load .env if present
if [ -f .env ]; then
    # shellcheck disable=SC1091
    set -a
    source .env
    set +a
fi

OLLAMA_URL="${ANTHROPIC_BASE_URL:-http://localhost:11434}"
DEFAULT_MODEL="${CLAUDE_OLLAMA_MODEL:-gpt-oss:20b-cloud}"
AUTH_TOKEN="${ANTHROPIC_AUTH_TOKEN:-ollama}"

# Colors (ANSI)
BOLD="\033[1m"
GREEN="\033[0;32m"
CYAN="\033[0;36m"
YELLOW="\033[0;33m"
TERRACOTTA="\033[38;2;217;119;87m"
DIM="\033[2m"
RESET="\033[0m"

# Display help
if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    cat << EOF
Usage: $0 [model_name] [claude_options...]

Interactive launcher for Claude Code using Ollama models.

Arguments:
  model_name          Optional model tag (e.g. beam:cloud, gpt-oss:20b-cloud).
                      If omitted in an interactive terminal, a menu is shown.
  claude_options      Any additional options passed directly to Claude Code
                      (e.g. -p "prompt", --resume, --verbose).

Options:
  -h, --help          Show this help message and exit.

Environment Variables:
  CLAUDE_OLLAMA_MODEL   Default fallback model (default: gpt-oss:20b-cloud)
  ANTHROPIC_BASE_URL    Ollama URL (default: http://localhost:11434)
  ANTHROPIC_AUTH_TOKEN  Auth token (default: ollama)

Examples:
  $0                                # Interactive selection menu
  $0 beam:cloud                     # Direct launch with beam:cloud
  $0 gemma4:31b-cloud -p "Review code"
EOF
    exit 0
fi

# Check if an explicit model flag was passed (--model or -m)
has_model_flag=0
for arg in "$@"; do
    if [ "$arg" = "--model" ] || [ "$arg" = "-m" ]; then
        has_model_flag=1
        break
    fi
done

ACTIVE_MODEL=""

# Case 1: First argument is a model name (does not start with -)
if [ -n "${1:-}" ] && [[ "$1" != -* ]]; then
    ACTIVE_MODEL="$1"
    shift
# Case 2: User explicitly passed --model in arguments
elif [ $has_model_flag -eq 1 ]; then
    ACTIVE_MODEL="" # Claude CLI will consume the --model argument from "$@"
# Case 3: Interactive selection or fallback to DEFAULT_MODEL
else
    # Determine if we can prompt interactively
    is_interactive=0
    if [ -t 0 ] || [ -r /dev/tty ]; then
        is_interactive=1
    fi

    if [ $is_interactive -eq 1 ]; then
        # Check if Ollama service is reachable, attempt to start on macOS if needed
        if ! curl -s --max-time 2 "$OLLAMA_URL/api/tags" >/dev/null 2>&1; then
            if [ "$(uname -s)" = "Darwin" ] && command -v open >/dev/null 2>&1; then
                printf "%bAttempting to start Ollama application...%b\n" "$DIM" "$RESET"
                open -a Ollama >/dev/null 2>&1 || true
                for _ in 1 2 3; do
                    if curl -s --max-time 1 "$OLLAMA_URL/api/tags" >/dev/null 2>&1; then break; fi
                    sleep 1
                done
            fi
        fi

        # Dynamically fetch available models from Ollama
        MODELS=()
        if command -v ollama >/dev/null 2>&1; then
            while IFS= read -r line; do
                [ -n "$line" ] && MODELS=("${MODELS[@]}" "$line")
            done <<EOF
$(ollama list 2>/dev/null | awk 'NR>1 && $1 != "" {print $1}')
EOF
        fi

        if [ ${#MODELS[@]} -gt 0 ]; then
            printf "\n%b┌────────────────────────────────────────────────────────┐%b\n" "$TERRACOTTA" "$RESET"
            printf "%b│        Claude Code + Ollama Interactive Launcher       │%b\n" "$TERRACOTTA" "$RESET"
            printf "%b└────────────────────────────────────────────────────────┘%b\n" "$TERRACOTTA" "$RESET"
            printf " %bEndpoint:%b %s\n\n" "$DIM" "$RESET" "$OLLAMA_URL"
            printf "%bAvailable Ollama Models:%b\n" "$BOLD" "$RESET"

            default_index=1
            for i in "${!MODELS[@]}"; do
                idx=$((i + 1))
                m="${MODELS[$i]}"
                if [ "$m" = "$DEFAULT_MODEL" ]; then
                    default_index=$idx
                    printf "  %b[%d]%b %b%-28s%b %b(default)%b\n" "$GREEN" "$idx" "$RESET" "$BOLD" "$m" "$RESET" "$CYAN" "$RESET"
                else
                    printf "  %b[%d]%b %-28s\n" "$BOLD" "$idx" "$RESET" "$m"
                fi
            done

            printf "  %b────────────────────────────────────────────────────────%b\n" "$DIM" "$RESET"
            printf "  %b[c]%b Custom model name (type any Ollama tag)\n" "$BOLD" "$RESET"
            printf "  %b[q]%b Quit\n\n" "$BOLD" "$RESET"

            default_model_name="${MODELS[$((default_index - 1))]}"
            prompt_text="Select a model [1-${#MODELS[@]}, default: $default_index ($default_model_name)]: "

            # Read user input (from terminal or stdin)
            printf "%b%s%b" "$BOLD" "$prompt_text" "$RESET"
            read -r choice || choice=""

            case "$choice" in
                q|Q)
                    printf "\n%bSession cancelled.%b\n" "$YELLOW" "$RESET"
                    exit 0
                    ;;
                c|C)
                    printf "Enter model tag (e.g. qwen2.5-coder:14b): "
                    read -r custom_model || custom_model=""
                    ACTIVE_MODEL="${custom_model:-$DEFAULT_MODEL}"
                    ;;
                "")
                    ACTIVE_MODEL="$default_model_name"
                    ;;
                *)
                    # Check if user entered a number in range
                    if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#MODELS[@]}" ]; then
                        ACTIVE_MODEL="${MODELS[$((choice - 1))]}"
                    else
                        # Check if user entered a model name directly
                        matched=0
                        for m in "${MODELS[@]}"; do
                            if [ "$m" = "$choice" ]; then
                                ACTIVE_MODEL="$m"
                                matched=1
                                break
                            fi
                        done
                        if [ $matched -eq 0 ]; then
                            printf "%bUnknown option '%s'; falling back to default: %s%b\n" "$YELLOW" "$choice" "$default_model_name" "$RESET"
                            ACTIVE_MODEL="$default_model_name"
                        fi
                    fi
                    ;;
            esac
        else
            # No models returned by ollama list
            printf "\n%b[WARN] No models found via 'ollama list' at %s.%b\n" "$YELLOW" "$OLLAMA_URL" "$RESET"
            printf "Enter model tag to use [default: %s]: " "$DEFAULT_MODEL"
            read -r manual_model || manual_model=""
            ACTIVE_MODEL="${manual_model:-$DEFAULT_MODEL}"
        fi
    else
        # Non-interactive shell
        ACTIVE_MODEL="$DEFAULT_MODEL"
    fi
fi

# Configure environment variables for Anthropic compatibility with Ollama
export ANTHROPIC_BASE_URL="$OLLAMA_URL"
export ANTHROPIC_AUTH_TOKEN="$AUTH_TOKEN"
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}"

# Verify claude command is present
if ! command -v claude >/dev/null 2>&1; then
    printf "%b[ERROR] Claude CLI ('claude') not found in PATH.%b\n" "$YELLOW" "$RESET"
    printf "Install Claude Code first: npm install -g @anthropic-ai/claude-code\n"
    exit 1
fi

if [ -n "$ACTIVE_MODEL" ]; then
    printf "\n%b🚀 Launching Claude Code with model:%b %b%s%b\n" "$BOLD" "$RESET" "$GREEN" "$ACTIVE_MODEL" "$RESET"
    printf "%b📍 Ollama Endpoint:%b %s\n\n" "$DIM" "$RESET" "$ANTHROPIC_BASE_URL"
    exec claude --model "$ACTIVE_MODEL" "$@"
else
    printf "\n%b🚀 Launching Claude Code...%b\n" "$BOLD" "$RESET"
    printf "%b📍 Ollama Endpoint:%b %s\n\n" "$DIM" "$RESET" "$ANTHROPIC_BASE_URL"
    exec claude "$@"
fi
