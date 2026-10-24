# 2. Choosing a Model

The model is the "brain" answering you. You can switch it at any time, even mid-session.

> Model lineup at the time of the videos (Oct 2026). Names and versions will change; the logic won't.

```mermaid
flowchart LR
    H[Haiku<br/>fast & cheap] --> S[Sonnet<br/>balanced] --> O[Opus<br/>default for serious work] --> F[Fable<br/>most powerful]
    style H fill:#e8f5e9
    style S fill:#e3f2fd
    style O fill:#fff3e0
    style F fill:#fce4ec
```

## Decision guide

```mermaid
flowchart TD
    Start{What kind of task?}
    Start -->|Small, repetitive, long-running,<br/>doesn't need deep reasoning| Haiku
    Start -->|Needs some logic, long-running,<br/>you want to save usage| Sonnet
    Start -->|Normal serious work<br/>on Max plans| Opus
    Start -->|Rare: hardest problems where<br/>Opus isn't enough| Fable
```

| Model | Use it when | Usage cost |
|---|---|---|
| **Haiku** | Bulk renames, simple edits, repetitive steps | Lowest |
| **Sonnet** | Everyday work on lower plans; long tasks where you want to conserve usage | Medium |
| **Opus** | The default for most real work if your plan allows | Higher |
| **Fable** | Occasional, very demanding workflows | Highest |

**Rule of thumb:**
- On **Max** plans: leave it on Opus.
- On **Pro/Free**: default to Sonnet, drop to Haiku for simple stuff, step up to Opus when quality really matters.

> **Want to run open-weights or local models?** See [Module 07 — Running with Ollama](../07-running-with-ollama/README.md) to use models like Qwen, Llama, Kimi, and DeepSeek via Ollama's Anthropic-compatible API.

➡️ Next: [Effort levels](03-effort-levels.md)
