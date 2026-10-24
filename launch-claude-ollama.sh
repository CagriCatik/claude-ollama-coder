#!/usr/bin/env bash
# ==============================================================================
# launch-claude-ollama.sh
# Run Claude Code configured to use local or cloud models served by Ollama.
# ==============================================================================

# Load .env if present
if [ -f .env ]; then
    # shellcheck disable=SC1091
    set -a
    source .env
    set +a
fi

# Default model configured during setup
DEFAULT_MODEL="${CLAUDE_OLLAMA_MODEL:-gpt-oss:20b-cloud}"

# If first argument looks like a model name (not starting with -), use it
if [ -n "$1" ] && [[ "$1" != -* ]]; then
    ACTIVE_MODEL="$1"
    shift
else
    ACTIVE_MODEL="$DEFAULT_MODEL"
fi

export ANTHROPIC_BASE_URL="${ANTHROPIC_BASE_URL:-http://localhost:11434}"
export ANTHROPIC_AUTH_TOKEN="${ANTHROPIC_AUTH_TOKEN:-ollama}"
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}"

echo "🚀 Launching Claude Code with Ollama model: $ACTIVE_MODEL"
exec claude --model "$ACTIVE_MODEL" "$@"
