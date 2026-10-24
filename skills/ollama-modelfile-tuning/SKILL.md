---
name: ollama-modelfile-tuning
description: Ollama Modelfile creation and optimization guidelines. Use when writing or tuning Ollama Modelfiles, configuring context window length (num_ctx), tuning sampling parameters (temperature, top_p, repeat_penalty), setting GPU layer offloading (num_gpu), crafting system prompts, or customizing local models for Claude Code tool-calling.
license: MIT
compatibility: Ollama 0.4+, Claude Code
metadata:
  author: claude-ollama-coder
  version: "1.0.0"
---

# Ollama Modelfile Tuning & Optimization

Guidelines for packaging, tuning, and operating custom models in Ollama, specifically tailored for coding workflows and Claude Code compatibility.

---

## When to Use This Skill

- **Trigger Scenarios:**
  - When authoring, editing, or auditing an Ollama `Modelfile`.
  - When configuring context window sizes (`PARAMETER num_ctx`) for Claude Code or agentic loops.
  - When tuning sampling parameters (`temperature`, `top_p`, `repeat_penalty`, `top_k`) for deterministic code generation.
  - When troubleshooting stop token runaway, hallucinated files, or prompt leakage.
  - When adjusting GPU layer offloading (`PARAMETER num_gpu`) to fit local VRAM limits.
  - When customizing system prompts (`SYSTEM """..."""`) for developer personas.

- **When NOT to Use:**
  - Do not use when working with proprietary cloud API endpoints (e.g. Anthropic direct API, OpenAI API).
  - Do not use for fine-tuning weights (LoRA / QLoRA training); this skill focuses on runtime inference configuration via Ollama Modelfile.

---

## 1. Context Window Tuning (`num_ctx`)

Claude Code requires large context windows to inspect codebases, execute tool loops, and analyze diffs.

```dockerfile
# Modelfile example: Expanding context to 64k for Claude Code
FROM qwen2.5-coder:14b

# Crucial: Default Ollama context is 2048 (too small for Claude Code)
PARAMETER num_ctx 65536

# Reduce temperature for deterministic, reliable code syntax
PARAMETER temperature 0.2
PARAMETER top_p 0.95
PARAMETER repeat_penalty 1.05
```

### Context Size vs VRAM Requirements
| `num_ctx` | Memory Overhead | Best Used For |
|---|---|---|
| **8,192 (8k)** | ~1–2 GB VRAM | Single function edits, quick unit tests |
| **32,768 (32k)** | ~3–5 GB VRAM | Small multi-file tasks, script reviews |
| **65,536 (64k)** | ~6–10 GB VRAM | **Standard Claude Code sessions**, refactoring |
| **131,072 (128k)** | ~12–18 GB VRAM | Large repo exploration, full stack debugging |

> **Tip:** If VRAM is constrained, use Flash Attention (`OLLAMA_FLASH_ATTENTION=1`) or quantize the KV cache (`PARAMETER kv_quant 1` if supported by the model).

---

## 2. Sampling Parameters for Coding

Coding models behave best with restrained sampling parameters to prevent hallucinated APIs and invalid syntax.

- **`temperature`**: Keep between `0.1` and `0.3` for coding. Use `0.0` for strict formatting or JSON tool calls.
- **`top_p`**: Keep between `0.9` and `0.95`.
- **`top_k`**: Set to `40`.
- **`repeat_penalty`**: Keep between `1.0` and `1.1`. Higher values (>1.15) can corrupt valid code repetitions like loops and import statements.

```dockerfile
PARAMETER temperature 0.2
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.05
```

---

## 3. Template and Stop Tokens

Missing stop tokens cause models to run away, generating fake user prompts or hallucinating imaginary files.

```dockerfile
# Define strict stop tokens for ChatML / Qwen templates
PARAMETER stop "<|im_start|>"
PARAMETER stop "<|im_end|>"
PARAMETER stop "<|endoftext|>"

# Example ChatML Template
TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>"""
```

---

## 4. Hardware & GPU Acceleration (`num_gpu`)

By default, Ollama attempts to offload all layers to GPU. When working with large models (e.g. 32b/70b) on mixed hardware:

- **`PARAMETER num_gpu 999`**: Forces complete offloading to GPU (best speed).
- If VRAM spills into system RAM, decrease layer count until fit:
  ```dockerfile
  PARAMETER num_gpu 32
  ```

---

## 5. Building & Deploying the Model

1. **Write the Modelfile**:
   ```bash
   cat << 'EOF' > Modelfile
   FROM qwen2.5-coder:14b
   PARAMETER num_ctx 65536
   PARAMETER temperature 0.2
   SYSTEM """You are a senior software engineer assisting in Claude Code. Output concise, production-ready code without unnecessary preamble."""
   EOF
   ```

2. **Build and register with Ollama**:
   ```bash
   ollama create my-coder:14b -f ./Modelfile
   ```

3. **Verify parameters**:
   ```bash
   ollama show my-coder:14b --modelfile
   ```

4. **Launch with Claude Code**:
   ```bash
   ./launch-claude-ollama.sh my-coder:14b
   ```

---

## Self-Verification Checklist

Before concluding Modelfile tuning or launching Claude Code:
- [ ] Base model (`FROM`) verified to exist or pulled locally with `ollama pull`.
- [ ] Context window length (`PARAMETER num_ctx`) explicitly increased beyond default 2,048 (recommend 32,768–65,536 for Claude Code).
- [ ] Temperature set to deterministic coding range (`0.1`–`0.3`).
- [ ] Appropriate stop tokens specified (`<|im_end|>`, etc.) matching the model's tokenizer family.
- [ ] Build succeeded via `ollama create <name> -f <modelfile>`.
- [ ] Verified active parameters with `ollama show <name> --modelfile`.
