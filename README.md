# Claude-Ollama-Coder

> Use the **Claude CLI** with **local models served by Ollama**.

This setup redirects the Anthropic-compatible endpoint used by Claude CLI to a **local Ollama server**, so you can keep the Claude CLI workflow while running open models on your own machine.

## Why this exists

This is useful when you want:

* local LLM inference
* Claude CLI workflow
* coding models such as **Qwen3-Coder** or **GPT-OSS**
* no external API dependency for requests

---

## Requirements

* **Ollama** installed and running
* **Claude CLI** installed
* at least one model available in Ollama, such as:

  * `qwen3-coder`
  * `gpt-oss:120b-cloud`

---

## How it works

Claude CLI normally talks to Anthropic's API.
In this setup, you point it at **Ollama running on `localhost:11434`** instead.

```mermaid
flowchart LR
    A[Claude CLI] --> B[Anthropic-Compatible API]
    B --> C[Ollama Local Server]
    C --> D[Local Model]

    classDef cli fill:#1f2937,stroke:#111827,color:#ffffff,stroke-width:2px;
    classDef api fill:#2563eb,stroke:#1d4ed8,color:#ffffff,stroke-width:2px;
    classDef ollama fill:#059669,stroke:#047857,color:#ffffff,stroke-width:2px;
    classDef model fill:#7c3aed,stroke:#6d28d9,color:#ffffff,stroke-width:2px;

    class A cli;
    class B api;
    class C ollama;
    class D model;
```

The mildly sneaky part: Claude CLI still thinks it is using an Anthropic-style API, but the actual model is local. Same doorway, different creature behind it.

---

## Architecture

### Default behavior

```mermaid
flowchart LR
    A[Claude CLI] --> B[Anthropic API]

    classDef cli fill:#1f2937,stroke:#111827,color:#ffffff,stroke-width:2px;
    classDef remote fill:#dc2626,stroke:#991b1b,color:#ffffff,stroke-width:2px;

    class A cli;
    class B remote;
```

### With Ollama redirect

```mermaid
flowchart LR
    C[Claude CLI] --> E[Anthropic-Compatible Endpoint<br/>localhost:11434]
    E --> O[Ollama Server]
    O --> M[Local Model<br/>qwen3-coder / gpt-oss / other]

    classDef cli fill:#1f2937,color:#ffffff,stroke:#111827
    classDef api fill:#2563eb,color:#ffffff,stroke:#1d4ed8
    classDef ollama fill:#059669,color:#ffffff,stroke:#047857
    classDef model fill:#7c3aed,color:#ffffff,stroke:#6d28d9

    class C cli
    class E api
    class O ollama
    class M model
```

---

## Setup

### 1. Start Ollama

```bash
ollama serve
```

Check installed models:

```bash
ollama list
```

### 2. Set environment variables

These variables make Claude CLI use your local Ollama endpoint.

#### PowerShell

```powershell
$env:ANTHROPIC_BASE_URL="http://localhost:11434"
$env:ANTHROPIC_AUTH_TOKEN="ollama"
$env:ANTHROPIC_API_KEY=""
```

### 3. Run Claude with a local model

```bash
claude --model qwen3-coder
```

or:

```bash
claude --model gpt-oss:120b-cloud
```

---

## Setup flow diagram

```mermaid
flowchart TD
    A[Install Ollama] --> B[Start Ollama Server]
    B --> C[Verify with ollama list]
    C --> D[Set Anthropic Environment Variables]
    D --> E[Run Claude CLI]
    E --> F[Use Local Model Through Ollama]

    classDef install fill:#0f766e,stroke:#115e59,color:#ffffff,stroke-width:2px;
    classDef verify fill:#2563eb,stroke:#1d4ed8,color:#ffffff,stroke-width:2px;
    classDef config fill:#ca8a04,stroke:#a16207,color:#ffffff,stroke-width:2px;
    classDef run fill:#7c3aed,stroke:#6d28d9,color:#ffffff,stroke-width:2px;
    classDef done fill:#059669,stroke:#047857,color:#ffffff,stroke-width:2px;

    class A,B install;
    class C verify;
    class D config;
    class E run;
    class F done;
```

---

## Usage

Once the environment variables are set, Claude CLI will send requests to Ollama instead of Anthropic.

### Example

```bash
claude --model qwen3-coder
```

### Another example

```bash
claude --model gpt-oss:120b-cloud
```

---

## Request flow

```mermaid
sequenceDiagram
    participant U as User
    participant C as Claude CLI
    participant O as Ollama Server
    participant M as Local Model

    U->>C: Run command / send prompt
    C->>O: Request via ANTHROPIC_BASE_URL
    O->>M: Forward prompt to selected model
    M-->>O: Generate response
    O-->>C: Return model output
    C-->>U: Display answer

    Note over C,O: Endpoint redirected to localhost:11434
```

---

## Example workflow

### Check installed models

```bash
ollama list
```

### Start Claude with Qwen3-Coder

```bash
claude --model qwen3-coder
```

### Start Claude with GPT-OSS

```bash
claude --model gpt-oss:120b-cloud
```

---

## Supported models

Any model installed in Ollama can be used, provided Claude CLI can access it through the compatible endpoint.

Examples:

* `qwen3-coder`
* `gpt-oss:120b-cloud`
* `codellama`
* `deepseek-coder`

List what is available:

```bash
ollama list
```

---

## Environment variables explained

| Variable               | Purpose                                               |
| ---------------------- | ----------------------------------------------------- |
| `ANTHROPIC_BASE_URL`   | points Claude CLI to your local Ollama server         |
| `ANTHROPIC_AUTH_TOKEN` | placeholder token expected by the compatibility layer |
| `ANTHROPIC_API_KEY`    | left empty in this local setup                        |

---

## Config diagram

```mermaid
flowchart LR
    A[ANTHROPIC_BASE_URL] --> A1[Anthropic-Compatible Endpoint<br/>localhost:11434]
    B[ANTHROPIC_AUTH_TOKEN] --> B1[ollama]
    C[ANTHROPIC_API_KEY] --> C1[empty string]

    classDef var fill:#374151,stroke:#111827,color:#ffffff,stroke-width:2px;
    classDef val1 fill:#2563eb,stroke:#1d4ed8,color:#ffffff,stroke-width:2px;
    classDef val2 fill:#059669,stroke:#047857,color:#ffffff,stroke-width:2px;
    classDef val3 fill:#9ca3af,stroke:#6b7280,color:#111827,stroke-width:2px;

    class A,B,C var;
    class A1 val1;
    class B1 val2;
    class C1 val3;
```

---

## Troubleshooting

### Model not found

Run:

```bash
ollama list
```

Make sure the model name in `claude --model ...` exactly matches the installed model name.

### Connection error

Make sure Ollama is running:

```bash
ollama serve
```

And verify the endpoint is reachable at:

```text
http://localhost:11434
```

### Claude still tries to use Anthropic

Double-check that the environment variables are set in the same shell session where you run `claude`.

---

## Claude CLI Cheatsheet

Common commands and usage patterns for development work.

### Start an interactive session

```bash
claude
```

### Use a specific model

```bash
claude --model qwen3-coder
```

```bash
claude --model gpt-oss:120b-cloud
```

### Ask a one-off question

```bash
claude "explain this codebase"
```

```bash
claude "optimize this python function"
```

### Ask about a file

```bash
claude "explain main.py"
```

```bash
claude "refactor server.js"
```

### Generate code

```bash
claude "write a REST API in FastAPI"
```

```bash
claude "create a React login component"
```

### Improve existing code

```bash
claude "improve performance of this script"
```

```bash
claude "add error handling to this file"
```

### Generate tests

```bash
claude "write unit tests for this module"
```

### Summarize a project

Run this from the project root:

```bash
claude "summarize this project"
```

### Debug an error

```bash
claude "fix this error"
```

Paste the stack trace or failing code into the session.

---

## Claude usage map

```mermaid
flowchart TD
    A[claude] --> A1[Interactive Session]
    B[claude --model qwen3-coder] --> B1[Use Specific Local Model]
    C[claude explain main.py] --> C1[Explain File]
    D[claude refactor server.js] --> D1[Refactor Code]
    E[claude write unit tests] --> E1[Generate Tests]
    F[claude fix this error] --> F1[Debugging Help]

    classDef cmd fill:#1f2937,stroke:#111827,color:#ffffff,stroke-width:2px;
    classDef action fill:#2563eb,stroke:#1d4ed8,color:#ffffff,stroke-width:2px;

    class A,B,C,D,E,F cmd;
    class A1,B1,C1,D1,E1,F1 action;
```

---

## Notes

* Ollama must be running on **port `11434`** unless you change the base URL.
* Model names must match the output of `ollama list`.
* Claude CLI must support overriding the Anthropic base URL.
* This setup depends on Anthropic-compatible request handling exposed by Ollama.

---

## Conceptual note

This pattern is a neat little software illusion. The CLI cares less about the metaphysics of the model and more about the shape of the API. Match the shape, and the tool keeps humming. Interfaces are masks; the machine behind the mask can change.