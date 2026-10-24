#!/usr/bin/env bash
# ==============================================================================
# run-mkdocs.sh
# Start local MkDocs preview server with automatic virtual environment handling.
# Works on macOS and Linux.
# ==============================================================================

set -e

# Navigate to script directory
cd "$(dirname "$0")"

# Create .venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment in .venv..."
    python3 -m venv .venv
fi

# Ensure mkdocs is installed
if ! .venv/bin/python -c "import mkdocs" 2>/dev/null; then
    echo "⬇️ Installing documentation dependencies from requirements-docs.txt..."
    .venv/bin/pip install -r requirements-docs.txt
fi

echo "🚀 Starting MkDocs server at http://127.0.0.1:8000"
echo "Press Ctrl+C to stop."
echo ""

exec .venv/bin/python -m mkdocs serve "$@"
