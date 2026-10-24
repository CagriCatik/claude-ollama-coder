#!/bin/sh
# Register Ollama cloud models locally (metadata only; inference stays in the cloud).
# Compatible with macOS / Linux POSIX sh.

set -u

MODELS='beam:cloud
gpt-oss:120b-cloud
gpt-oss:20b-cloud
gemma4:31b-cloud
nemotron-3-ultra:cloud
nemotron-3-super:cloud
nemotron-3-nano:30b-cloud'

REFRESH=0
case "${1:-}" in
  '') ;;
  --refresh) REFRESH=1 ;;
  --list)
    printf '%s\n' "$MODELS"
    exit 0
    ;;
  -h|--help)
    printf 'Usage: sh %s [--refresh|--list|--help]\n' "$0"
    printf '  (default)  Skip already registered models\n'
    printf '  --refresh  Pull every model again to update it\n'
    printf '  --list     Show cloud model names\n'
    exit 0
    ;;
  *)
    printf 'Unknown argument: %s\n' "$1" >&2
    exit 2
    ;;
esac

if ! command -v ollama >/dev/null 2>&1; then
  printf 'Error: Ollama CLI not found. Install Ollama from https://ollama.com/download first.\n' >&2
  exit 1
fi

# On macOS, try opening the app if its background server is not running.
if ! ollama list >/dev/null 2>&1; then
  if [ "$(uname -s)" = Darwin ] && command -v open >/dev/null 2>&1; then
    printf 'Starting the Ollama application...\n'
    open -a Ollama >/dev/null 2>&1 || true
    attempt=0
    while [ "$attempt" -lt 10 ]; do
      if ollama list >/dev/null 2>&1; then break; fi
      sleep 1
      attempt=$((attempt + 1))
    done
  fi
fi

if ! ollama list >/dev/null 2>&1; then
  printf 'Error: Ollama service is not reachable. Start the Ollama app (macOS) or run "ollama serve" (Linux).\n' >&2
  exit 1
fi

printf '\nSigning in to Ollama Cloud (may open a browser)...\n'
if ! ollama signin; then
  printf 'Error: Sign-in failed. Run "ollama signin" manually and retry.\n' >&2
  exit 1
fi

EXISTING=$(ollama list | awk 'NR > 1 { print $1 }')
success=0
skipped=0
failed=0
failed_models=''

printf '\nRegistering cloud models...\n'
for model in $MODELS; do
  if [ "$REFRESH" -eq 0 ] && printf '%s\n' "$EXISTING" | grep -Fxq "$model"; then
    printf '[SKIP] %s (already registered)\n' "$model"
    skipped=$((skipped + 1))
    continue
  fi

  printf '\n[PULL] %s\n' "$model"
  if ollama pull "$model"; then
    printf '[OK]   %s\n' "$model"
    success=$((success + 1))
  else
    printf '[FAIL] %s\n' "$model" >&2
    failed_models="${failed_models}${model}\n"
    failed=$((failed + 1))
  fi
done

printf '\nFinished: %s pulled, %s skipped, %s failed.\n' "$success" "$skipped" "$failed"
if [ "$failed" -gt 0 ]; then
  printf 'Failed model(s):\n'
  printf '%b' "$failed_models"
  printf 'Failures may be due to connectivity, access, or changed model availability.\n'
  exit 1
fi

printf '\nAvailable Ollama models:\n'
ollama list
printf '\nRun one with: ollama run beam:cloud\n'
printf 'Cloud inference uses your account allowance; pulling does not download model weights.\n'
