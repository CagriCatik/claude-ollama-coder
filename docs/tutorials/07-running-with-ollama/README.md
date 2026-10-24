# Module 07 — Running with Ollama

**Goal:** connect Claude Code to local and cloud open-weights models through Ollama's Anthropic-compatible API for private, offline, or alternative-model workflows.

| # | Lesson | Time |
|---|---|---|
| 1 | [Quickstart & setup](01-quickstart-and-setup.md) | 10 min |
| 2 | [Selecting models & context](02-selecting-models-and-context.md) | 15 min |
| 3 | [Headless automation & `/loop`](03-headless-and-automation.md) | 10 min |
| 4 | [Cloud models & channels](04-cloud-and-channels.md) | 10 min |
| 5 | [Local model tactics & Storybook](05-local-model-tactics-and-storybook.md) | 15 min |
| 6 | [CLI tools & Python SDK](06-cli-tools-and-python-sdk.md) | 10 min |
| 7 | [Alternative providers & gateways](07-alternative-providers-and-gateways.md) | 10 min |

## How Ollama fits into Claude Code

Claude Code communicates using Anthropic's Messages API. Ollama provides an Anthropic-compatible API layer, allowing Claude Code to run against either local models running on your machine or Ollama Cloud models without changing how Claude Code works.

```mermaid
flowchart TD
    CC[Claude Code CLI / Desktop]
    
    subgraph Backends["Inference Backends"]
        direction TB
        Anthropic["☁️ Anthropic Cloud<br/>(Claude Opus / Sonnet / Haiku)"]
        OllamaLocal["💻 Local Ollama Daemon<br/>http://localhost:11434<br/>(Qwen, Llama, DeepSeek)"]
        OllamaCloud["🌐 Ollama Cloud<br/>https://ollama.com<br/>(Kimi, Gemma, GLM)"]
    end

    CC -->|Default| Anthropic
    CC -->|ANTHROPIC_BASE_URL=localhost:11434| OllamaLocal
    CC -->|ANTHROPIC_BASE_URL=ollama.com| OllamaCloud

    style OllamaLocal fill:#e8f5e9,stroke:#43a047
    style OllamaCloud fill:#e0f7fa,stroke:#00838f
    style Anthropic fill:#fff3e0,stroke:#fb8c00
```

## Supported capabilities

| Capability | Supported with Ollama | Notes |
|---|---|---|
| **Chat & code reasoning** | ✅ | Ask questions about codebases and architectures |
| **Command-line execution** | ✅ | Runs build, test, and shell commands with standard permission checks |
| **Tool calling** | ✅ | Works with compatible models (e.g. Qwen 2.5/3.5, Llama 3.3) |
| **File edits** | ✅ | Reading, diffing, and writing files |
| **Subagents** | ✅ | Delegating subtasks with separate context windows |
| **Web search & fetch** | ✅ | Uses Ollama's web search API |
| **Vision** | ✅ | Analyze images and UI screenshots with multimodal models |
| **Thinking** | ✅ | Supported on thinking-enabled models |
| **Scheduled tasks** | ✅ | Native `/loop` command for recurring prompts |
| **Channels** | ✅ | Remote access via Telegram bot integration |

## Why run with Ollama?

```mermaid
flowchart LR
    A["🔒 Complete Privacy<br/>Code never leaves your machine"] --> Y((Why Ollama?))
    B["💸 No Usage Caps<br/>Run unlimited queries locally"] --> Y
    C["✈️ Offline Work<br/>Code on flights or without internet"] --> Y
    D["🧪 Alternative Models<br/>Test Qwen, DeepSeek, Kimi, Gemma"] --> Y
```

**Checkpoint:** understand how to launch Claude Code with local models, configure environment variables, choose high-context models, and automate tasks with `/loop`.

➡️ Practice: [Lab 10 — Ollama & Local Models](../labs/lab-10-ollama.md)
