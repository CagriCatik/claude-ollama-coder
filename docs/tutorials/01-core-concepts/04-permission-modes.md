# 4. Permission Modes

The **mode** decides how much Claude may do without asking you.

```mermaid
flowchart LR
    Manual[🔒 Manual<br/>asks for every tool call] --> Plan[📝 Plan<br/>read-only, writes a plan]
    Plan --> Accept[✏️ Accept edits<br/>file edits auto-approved]
    Accept --> Auto[🤖 Auto<br/>asks only for risky actions]
    Auto --> Bypass[⚠️ Bypass<br/>never asks]
    style Bypass fill:#ffebee,stroke:#c62828
    style Auto fill:#e8f5e9,stroke:#2e7d32
```

| Mode | Asks before… | When to use |
|---|---|---|
| **Manual** | every tool call | Unfamiliar codebase, learning what Claude does |
| **Plan** | — (makes no changes) | Before any non-trivial build: think first |
| **Accept edits** | commands, but not file edits | You trust edits, want to watch commands |
| **Auto** *(default)* | destructive/unusual actions: deletes, mass changes, new kinds of tool calls | ✅ 90 % of the time |
| **Bypass permissions** | nothing | Sandboxed/throwaway environments only |

## How Auto mode decides

```mermaid
flowchart TD
    A[Claude wants to act] --> B{Risky?<br/>delete, mass change,<br/>new tool type}
    B -- No --> C[Runs it]
    B -- Yes --> D[Pauses and asks you]
    D -->|Approve| C
    D -->|Deny| E[Finds another way or stops]
```

## Make it permanent per project
You can pre-approve or block specific commands for a project in `.claude/settings.json` → see [settings.json](../02-project-context/03-settings-json.md).

> ⚠️ Avoid **Bypass** on your real machine. Use **Auto** + **Plan** as your two everyday modes.

➡️ Next: [The plan-mode workflow](05-plan-mode-workflow.md)
