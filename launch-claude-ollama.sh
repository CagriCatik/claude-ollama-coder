#!/usr/bin/env bash
# ==============================================================================
# launch-claude-ollama.sh
# Run Claude Code configured to use local or cloud models served by Ollama.
# Delegates to run-claude.sh for interactive model selection and environment setup.
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/run-claude.sh" "$@"
