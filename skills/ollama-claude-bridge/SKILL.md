---
name: ollama-claude-bridge
description: Configuring and operating Claude Code with local Ollama models. Use when pointing Claude Code to local endpoints, setting ANTHROPIC_BASE_URL, configuring mock API keys, troubleshooting connection refused errors, tuning context limits, or managing local tool-calling compatibility.
license: MIT
compatibility: Ollama 0.4+, Claude Code 1.0+, curl, zsh/bash
metadata:
  author: claude-ollama-coder
  version: "1.0.0"
---

# Ollama & Claude Code Integration Bridge

Comprehensive operational guide for proxying, configuring, and troubleshooting Claude Code sessions powered entirely by local models running on Ollama.

---

## When to Use This Skill

- **Trigger Scenarios:**
  - When configuring environment variables (`ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`, `OLLAMA_HOST`) to route Claude Code locally.
  - When troubleshooting connection refused errors on `http://127.0.0.1:11434`.
  - When diagnosing tool-calling issues, malformed JSON function calls, or context truncation with local models.
  - When setting up multi-channel routing (local Ollama for exploration, cloud endpoints for complex code reviews).
  - When automating headless batch coding runs with `claude -p` using local models.

- **When NOT to Use:**
  - Do not use when authoring Modelfiles syntax (use `ollama-modelfile-tuning`).
  - Do not use for pure remote Anthropic cloud subscriptions where no local Ollama proxy is involved.

---

## 1. Environment Configuration

Claude Code can communicate with OpenAI/Anthropic-compatible endpoints by overriding standard environment variables.

### Environment Setup (`.env` or shell export)
```bash
# Point Claude Code to Ollama's OpenAI-compatible or Anthropic proxy endpoint
export ANTHROPIC_BASE_URL="http://localhost:11434/v1"

# Claude Code requires a non-empty API key string; any dummy string works for local Ollama
export ANTHROPIC_API_KEY="ollama-local"

# Set default model name (must match your installed Ollama model tag)
export CLAUDE_OLLAMA_MODEL="qwen2.5-coder:14b"
export ANTHROPIC_MODEL="qwen2.5-coder:14b"
```

---

## 2. Launching Claude Code with Local Models

Use the provided launch script in this repository:

```bash
# Interactive coding session with local 14b model
./launch-claude-ollama.sh qwen2.5-coder:14b

# Run a single non-interactive task and exit
./launch-claude-ollama.sh qwen2.5-coder:14b -p "Add unit tests for src/auth.py"
```

### Windows Batch Launcher
```bat
run-claude.bat
```

---

## 3. Recommended Local Coding Models

| Model | Parameters | Required VRAM | Strengths |
|---|---|---|---|
| **`qwen2.5-coder:14b`** | 14 Billion | ~9 GB VRAM | **Recommended default:** Excellent balance of speed, code accuracy, and tool calling. |
| **`qwen2.5-coder:32b`** | 32 Billion | ~20 GB VRAM | Near-cloud reasoning; excels at deep refactorings and subtle bug fixes. |
| **`qwen2.5-coder:7b`** | 7 Billion | ~5 GB VRAM | Fast iteration on laptops; best for simple edits and scripts. |
| **`deepseek-coder-v2:16b`** | 16 Billion | ~10 GB VRAM | Mixture-of-Experts architecture; high math and coding benchmark performance. |

---

## 4. Troubleshooting Local Execution

### Issue 1: Connection Refused (`127.0.0.1:11434`)
```bash
# Verify Ollama service is active
curl -s http://127.0.0.1:11434/api/tags | grep -q "models" && echo "Ollama OK" || echo "Ollama Down"

# If down, launch Ollama
ollama serve &
```

### Issue 2: Context Length Overflow
Local models default to a 2,048 token context window if not explicitly overridden in their Modelfile. Claude Code requires larger context to read repository files:
- Verify active context: `ollama show qwen2.5-coder:14b --modelfile | grep num_ctx`
- Expand context: use `skills/ollama-modelfile-tuning` to set `PARAMETER num_ctx 65536`.

### Issue 3: Invalid Tool Call Syntax
Smaller local models (<14b) may occasionally emit markdown backticks around JSON tool calls.
- Remedy: Reduce temperature (`0.1` or `0.0`), or use higher parameter models (`qwen2.5-coder:14b` or `32b`).

---

## Self-Verification Checklist

Before launching or concluding local Claude Code workflows:
- [ ] Ollama service verified active on `http://127.0.0.1:11434`.
- [ ] Target model verified locally via `ollama list`.
- [ ] `ANTHROPIC_BASE_URL` and dummy `ANTHROPIC_API_KEY` exported in environment.
- [ ] Target model context size (`num_ctx`) verified to be at least 32k.
- [ ] Tool execution verified with a smoke test prompt (`claude -p "What files are in this directory?"`).
