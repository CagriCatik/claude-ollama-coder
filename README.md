<div align="center">
  <h1>Claude-Ollama-Coder</h1>
  <p><strong>The Complete Tutorial, Hands-on Course & Architecture Reference for Claude Code with Ollama Local Models</strong></p>
  <p>
    <a href="https://cagricatik.github.io/claude-ollama-coder/">
      <img alt="Documentation" src="https://img.shields.io/badge/docs-MkDocs--Material-blue?style=flat-square">
    </a>
    <a href="https://ollama.com/">
      <img alt="Ollama" src="https://img.shields.io/badge/Ollama-local%20%26%20cloud%20models-black?style=flat-square">
    </a>
    <a href="https://docs.anthropic.com/en/docs/claude-code">
      <img alt="Claude CLI" src="https://img.shields.io/badge/Claude%20CLI-compatible-6B46C1?style=flat-square">
    </a>
    <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square">
    <img alt="Curriculum" src="https://img.shields.io/badge/course-8%20modules%20%2B%2010%20labs-success?style=flat-square">
  </p>
</div>

---

## Overview

**Claude-Ollama-Coder** unifies two essential developer resources into a single repository:

1. **The Complete Claude Code Tutorial & Course**: An 8-module progressive curriculum (Modules 00–07) paired with 10 hands-on labs, capstone project, starter templates, and an interactive browser-based progress dashboard (`progress-dashboard.html`).
2. **Local & Cloud Inference Engine via Ollama**: Complete cross-platform automation and scripts that redirect the Claude CLI / Claude Code to an Anthropic-compatible Ollama endpoint (`http://localhost:11434`), enabling zero-cost, private, offline-capable agentic coding.
3. **Deep Technical Reference Library**: An in-depth reference suite covering the Claude API, Model Context Protocol (MCP), Subagent Orchestration, and reusable Agent Skills, published via MkDocs Material to [GitHub Pages](https://cagricatik.github.io/claude-ollama-coder/).

---

## Architecture

Claude CLI normally connects to Anthropic's hosted cloud API. In this unified setup, the CLI environment is pointed at Ollama on `localhost:11434`, which serves open-weights coding models locally or connects to Ollama Cloud.

```mermaid
flowchart LR
    A["Claude CLI / Claude Code"] --> B["Anthropic-Compatible Endpoint<br/>http://localhost:11434"]
    B --> C["Ollama Daemon"]
    C --> D{"Model Target"}
    D -->|Local Offline| E["Local Models<br/>(qwen3-coder, deepseek-coder)"]
    D -->|Cloud Acceleration| F["Ollama Cloud Models<br/>(gpt-oss:20b-cloud, 128k ctx)"]

    classDef cli fill:#1e293b,stroke:#3b82f6,color:#ffffff,stroke-width:2px;
    classDef endpoint fill:#0284c7,stroke:#0369a1,color:#ffffff,stroke-width:2px;
    classDef ollama fill:#059669,stroke:#047857,color:#ffffff,stroke-width:2px;
    classDef model fill:#6366f1,stroke:#4f46e5,color:#ffffff,stroke-width:2px;

    class A cli;
    class B endpoint;
    class C ollama;
    class E,F model;
```

---

## Quick Start (Cross-Platform)

### 1. Prerequisites
- [Ollama](https://ollama.com/) installed and running
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (`claude`) installed
- Python 3.10+ (for documentation and SDK labs)

### 2. Automated Setup & Launcher

#### macOS & Linux
```bash
# Automated setup (checks Ollama, Claude CLI, pulls recommended model):
./setup-ollama.sh

# Launch Claude Code with default model (gpt-oss:20b-cloud):
./launch-claude-ollama.sh

# Or launch with a specific local model:
./launch-claude-ollama.sh qwen3-coder
```

#### Windows
```bat
:: Check prerequisites and launch Claude Code with Ollama
run-claude.bat

:: Or specify a model
run-claude.bat qwen3-coder
```

### 3. Manual Configuration

You can configure your shell environment manually or copy [`.env.example`](.env.example) to `.env`:

```bash
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""

# Run Claude Code with your chosen model
claude --model gpt-oss:20b-cloud -p "Explain this repository"
```

---

## 🎓 The Interactive Course Curriculum

A hands-on, structured learning path taking you from installation to an advanced, production-grade Claude Code workspace:

```mermaid
flowchart TD
    A["00 Getting Started"] --> B["01 Core Concepts"]
    B --> C["02 Project Context"]
    C --> D["03 Extending Claude"]
    D --> E["04 Daily Workflow"]
    E --> F["05 Beyond Code"]
    F --> H["06 Learning with AI"]
    H --> I["07 Running with Ollama"]
    I --> G["Labs & Capstone"]

    style A fill:#e8f4fd,stroke:#1e88e5
    style B fill:#e8f4fd,stroke:#1e88e5
    style C fill:#fff4e5,stroke:#fb8c00
    style D fill:#fff4e5,stroke:#fb8c00
    style E fill:#e8f5e9,stroke:#43a047
    style F fill:#e8f5e9,stroke:#43a047
    style H fill:#e0f7fa,stroke:#00838f
    style I fill:#f1f8e9,stroke:#558b2f
    style G fill:#f3e5f5,stroke:#8e24aa
```

### Module Breakdown

| Level | Module | Lessons & Integrated Deep Dives |
|---|---|---|
| 🟦 **Beginner** | [**00 Getting Started**](docs/tutorials/00-getting-started/README.md) | Where Claude runs, desktop UI tour, plans & usage limits |
| 🟦 **Beginner** | [**01 Core Concepts**](docs/tutorials/01-core-concepts/README.md) | Prompting, models, effort levels, plan mode.<br>• *Deep Dives:* [Claude 101 API](docs/tutorials/01-core-concepts/06-claude-101-api-fundamentals.md), [AI Fluency](docs/tutorials/01-core-concepts/07-ai-fluency-framework.md) |
| 🟧 **Intermediate** | [**02 Project Context**](docs/tutorials/02-project-context/README.md) | `CLAUDE.md`, memory, `settings.json`, referencing files and comments with `@` |
| 🟧 **Intermediate** | [**03 Extending Claude**](docs/tutorials/03-extending-claude/README.md) | Skills (`SKILL.md`), subagents, MCP servers, event hooks.<br>• *Deep Dives:* [MCP Guide](docs/tutorials/03-extending-claude/06-mcp-expert-guide.md), [Advanced MCP](docs/tutorials/03-extending-claude/07-mcp-advanced-patterns.md), [Agent Skills](docs/tutorials/03-extending-claude/08-agent-skills-guide.md), [Subagents](docs/tutorials/03-extending-claude/09-subagents-architecture.md), [Skills Ref](docs/tutorials/03-extending-claude/10-skills-deep-dive.md) |
| 🟩 **Advanced** | [**04 Daily Workflow**](docs/tutorials/04-daily-workflow/README.md) | Context management (`/compact`, `/clear`), `/rewind`, parallel worktrees.<br>• *Deep Dive:* [Claude Code in Action](docs/tutorials/04-daily-workflow/06-claude-code-in-action.md) |
| 🟩 **Advanced** | [**05 Beyond Code**](docs/tutorials/05-beyond-code/README.md) | Projects, connectors, Cowork, Claude Design → Claude Code.<br>• *Deep Dive:* [Building with Claude API & RAG](docs/tutorials/05-beyond-code/06-building-with-claude-api-and-rag.md) |
| 🟦 **Applied** | [**06 Learning with AI**](docs/tutorials/06-learning-with-ai/README.md) | Collect → Understand → Own: deep research with AI + notebook archives |
| 🟧 **Alternative** | [**07 Running with Ollama**](docs/tutorials/07-running-with-ollama/README.md) | Local hardware, Ollama Cloud, 64k+ context, headless CI (`--yes`), `/loop`, Telegram channels, Storybook screenshot loops |

### Hands-on Labs & Capstone

Work through matching exercises in [`docs/tutorials/labs/`](docs/tutorials/labs/README.md):

- [**Lab 01**](docs/tutorials/labs/lab-01-first-project.md): First Project setup & inspection
- [**Lab 02**](docs/tutorials/labs/lab-02-plan-mode.md): Plan Mode for non-destructive design
- [**Lab 03**](docs/tutorials/labs/lab-03-claude-md.md): `CLAUDE.md` standing instructions
- [**Lab 04**](docs/tutorials/labs/lab-04-settings.md): `.claude/settings.json` permissions
- [**Lab 05**](docs/tutorials/labs/lab-05-skill.md): Writing your first custom Skill
- [**Lab 06**](docs/tutorials/labs/lab-06-subagent.md): Creating a specialist Subagent
- [**Lab 07**](docs/tutorials/labs/lab-07-hook.md): Event Hooks for notifications and security
- [**Lab 08**](docs/tutorials/labs/lab-08-parallel.md): Parallel sessions with Git worktrees
- [**Lab 09**](docs/tutorials/labs/lab-09-learning-workflow.md): The Collect-Understand-Own learning archive
- [**Lab 10**](docs/tutorials/labs/lab-10-ollama.md): Full Ollama local integration
- [**Capstone**](docs/tutorials/labs/capstone.md): Complete end-to-end workspace build

### Interactive Course Dashboard

Track your learning progress across modules and labs in the interactive dashboard:
- File: [`progress-dashboard.html`](progress-dashboard.html)
- Open in your browser:
  ```bash
  open progress-dashboard.html       # macOS
  xdg-open progress-dashboard.html   # Linux
  start progress-dashboard.html      # Windows
  ```

---

## Reference Guides & Cheatsheets

We provide two complementary cheatsheets tailored for different tasks:

1. [**`CHEATSHEET.md`**](CHEATSHEET.md) — **Daily CLI Quick Reference**:
   Slash commands (`/init`, `/context`, `/compact`, `/rewind`, `/loop`), permission modes, Ollama CLI reference, and everyday keyboard shortcuts.
2. [**`docs/tutorials/unified-cheatsheet.md`**](docs/tutorials/unified-cheatsheet.md) — **Technical & API Reference**:
   Token budgets, prompt caching, tool use schemas, SDK parameters, and architectural decision tables.
3. [**`GLOSSARY.md`**](GLOSSARY.md) — Fast terminology lookup linking directly to course lessons.

---

## 📚 Technical Reference Documentation (MkDocs)

The comprehensive documentation suite lives in [`docs/`](docs/) and is hosted on [GitHub Pages](https://cagricatik.github.io/claude-ollama-coder/):

- **[Course Curriculum Overview](docs/tutorials/index.md)** — Full curriculum summary on the docs site
- **[Unified Cheatsheet](docs/tutorials/unified-cheatsheet.md)** — Production habits & prompt engineering
- **[Claude 101](docs/tutorials/01-core-concepts/06-claude-101-api-fundamentals.md)** — API fundamentals, multi-turn dialogues, streaming
- **[AI Fluency Framework](docs/tutorials/01-core-concepts/07-ai-fluency-framework.md)** — Cognitive model, evaluation & clarity
- **[Model Context Protocol (MCP)](docs/tutorials/03-extending-claude/06-mcp-expert-guide.md)** — MCP primitives, server architecture, resources
- **[Advanced MCP Patterns](docs/tutorials/03-extending-claude/07-mcp-advanced-patterns.md)** — Streaming, custom transports, multi-server resilience
- **[Agent Skills](docs/tutorials/03-extending-claude/08-agent-skills-guide.md)** — Extending autonomous agent behaviors
- **[Subagents & Orchestration](docs/tutorials/03-extending-claude/09-subagents-architecture.md)** — Multi-agent delegation, protocols, pipelines
- **[Skills Reference](docs/tutorials/03-extending-claude/10-skills-deep-dive.md)** — `SKILL.md` format, triggers, and marketplace patterns
- **[Claude Code in Action](docs/tutorials/04-daily-workflow/06-claude-code-in-action.md)** — Complete mechanics of coding assistants & hooks
- **[Building with the Claude API](docs/tutorials/05-beyond-code/06-building-with-claude-api-and-rag.md)** — Tool use, embeddings, RAG architectures

### Running Documentation Locally

**Using the included helper scripts (recommended):**
- **macOS / Linux**:
  ```bash
  ./run-mkdocs.sh
  ```
- **Windows**:
  ```bat
  run-mkdocs.bat
  ```

**Or manually via virtual environment:**
```bash
# 1. Activate the virtual environment
source .venv/bin/activate

# 2. Install dependencies (if not already installed)
pip install -r requirements-docs.txt

# 3. Start live preview server at http://127.0.0.1:8000
mkdocs serve
```

*(Alternatively, run directly without activating: `.venv/bin/mkdocs serve`)*

---

## Skills Library & Agent Skills

All skills conform to the [Anthropic Agent Skills standard](https://agentskills.io) and are registered in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json). Detailed authoring instructions, lifecycle diagrams, and validation details are in [`skills/README.md`](skills/README.md).

- [`skills/_template/`](skills/_template/): Canonical template for authoring new conforming skills, with validation scripts and progressive disclosure references.
- [`skills/claude-code-workflows/`](skills/claude-code-workflows/): Plan mode (`/plan`), context compacting (`/compact`), slash commands, subagents, and headless automation (`claude -p`).
- [`skills/ollama-claude-bridge/`](skills/ollama-claude-bridge/): Pointing Claude Code to local Ollama endpoints, environment setup, model tags, and tool-calling compatibility.
- [`skills/mcp-builder/`](skills/mcp-builder/): Building Model Context Protocol (MCP) servers in Python (FastMCP) or TypeScript, stdio/SSE transports.
- [`skills/ollama-modelfile-tuning/`](skills/ollama-modelfile-tuning/): Ollama Modelfile tuning (64k+ context `num_ctx`, sampling parameters, stop tokens, GPU layer offloading).
- [`skills/git-workflow/`](skills/git-workflow/): Conventional Commits, Co-Authored-By attribution, Git Worktrees for parallel sessions, PR templates.
- [`skills/secure-coding/`](skills/secure-coding/): Injection prevention, path traversal defense, secret protection, input validation with Pydantic.
- [`skills/python-modern-practices/`](skills/python-modern-practices/): Python 3.10+ typing (`X | None`), Protocols, Pydantic v2 models, async httpx, pytest fixtures.
- [`skills/api-design/`](skills/api-design/): RESTful API architecture, RFC 7807 Problem Details schemas, cursor pagination, idempotency headers.
- [`skills/karpathy-guidelines/`](skills/karpathy-guidelines/): Guidelines to reduce common LLM coding mistakes (surgical edits, explicit assumptions, test loops).
- [`skills/ros2/`](skills/ros2/): ROS2 robotics development (Python rclpy, C++ rclcpp, launch files, QoS).
- [`skills/software-architecture/`](skills/software-architecture/): System design, component boundaries, ADRs, scalability patterns.
- [`skills/software-engineering/`](skills/software-engineering/): API design, clean code practices, error handling contracts.

**Validate Conformance:**
```bash
python3 skills/_template/scripts/validate_skill.py skills
```

---

## Starter Examples

- [`examples/starter-project/`](examples/starter-project/): Complete `.claude/` template featuring `settings.json`, subagents (`code-reviewer`, `test-runner`), hooks (`notify.sh`, `block-secrets.sh`), and skills.
- [`examples/learning-archive/`](examples/learning-archive/): Ready-to-copy research archive template for Module 06.

---

## Repository Layout

```text
claude-ollama-coder/
├── README.md                      ← Master unified portal & complete curriculum map
├── CHEATSHEET.md                  ← Daily CLI slash commands & shortcuts reference
├── GLOSSARY.md                    ← Course vocabulary with module lesson links
├── progress-dashboard.html        ← Interactive visual course tracker
├── .env.example                   ← Environment template for endpoints & model selection
│
├── setup-ollama.sh                ← Automated macOS/Linux setup & verification script
├── launch-claude-ollama.sh        ← Quick macOS/Linux Claude Code launcher with Ollama
├── run-claude.bat                 ← Windows Claude Code launcher with Ollama
├── run-mkdocs.sh                  ← macOS/Linux MkDocs live preview server launcher
├── run-mkdocs.bat                 ← Windows MkDocs live documentation server launcher
│
├── requirements.txt               ← Python dependencies for Ollama SDK & lab exercises
├── requirements-docs.txt          ← Documentation build dependencies (MkDocs Material)
├── mkdocs.yml                     ← MkDocs configuration & unified navigation tree
│
├── docs/                          ← Unified documentation hub (MkDocs source)
│   ├── index.md                   ← Documentation homepage
│   └── tutorials/                 ← Complete structured course & deep dives
│       ├── index.md               ← Course overview & learning path
│       ├── unified-cheatsheet.md  ← Comprehensive technical reference
│       ├── 00-getting-started/    ← Module 00: Setup, UI, limits
│       ├── 01-core-concepts/      ← Module 01: Prompting, models + Claude 101, AI Fluency
│       ├── 02-project-context/    ← Module 02: CLAUDE.md, settings, memory, referencing
│       ├── 03-extending-claude/   ← Module 03: Skills, agents, MCP + deep specifications
│       ├── 04-daily-workflow/     ← Module 04: Context, rewind, review + Code in Action
│       ├── 05-beyond-code/        ← Module 05: Projects, connectors + Claude API & RAG
│       ├── 06-learning-with-ai/   ← Module 06: Collect → Understand → Own
│       ├── 07-running-with-ollama/← Module 07: Local models, headless, 64k+
│       └── labs/                  ← Hands-on exercises (Lab 01 to Lab 10 + Capstone)
│
├── examples/                      ← Starter project template (.claude/) & learning archive
├── skills/                        ← Reusable skills (Karpathy, ROS2, Architecture, Eng)
└── archive/                       ← Preserved legacy artifacts (e.g. archive/README_.md)
```

---

## Notes on Local Model Selection

When running Claude Code with Ollama, note that:
- **Context Window**: Claude Code requires a large context window. Ensure your model is configured with at least `64k` tokens (`num_ctx 65536` in Modelfile or Ollama configuration).
- **Tool Calling**: Ensure your chosen model supports tool use. Cloud-backed models like `gpt-oss:20b-cloud` and `gpt-oss:120b-cloud` provide 128k context and robust function calling with 0 MB disk usage.
- **Offline Local**: For local offline work, recommended models include `qwen3-coder`, `qwen2.5-coder:14b`, and `deepseek-coder`.

---

## Archive Policy

Per repository maintenance rules, files are never deleted without historical preservation. Legacy materials (such as the initial raw curriculum README `README_.md`) are safely cataloged in [`archive/`](archive/).