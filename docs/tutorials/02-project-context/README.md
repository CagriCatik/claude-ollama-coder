# Module 02 — Project Context

**Goal:** teach Claude your project once, so every new session starts informed instead of re-exploring the codebase.

| # | Lesson | Time |
|---|---|---|
| 1 | [CLAUDE.md](01-claude-md.md) | 15 min |
| 2 | [Memory](02-memory.md) | 10 min |
| 3 | [settings.json](03-settings-json.md) | 15 min |
| 4 | [Referencing files, images & comments](04-referencing-context.md) | 10 min |

## Where everything lives

```mermaid
flowchart TB
    subgraph Global["🏠 Global — ~/.claude/  (your machine, all projects)"]
        GC[CLAUDE.md<br/>personal instructions]
        GS[settings.json]
        GSK[skills/]
        GA[agents/]
        GM[projects/&lt;project&gt;/memory/<br/>private memory]
    end
    subgraph Project["📁 Project — my-app/  (shared via git)"]
        PC[CLAUDE.md]
        subgraph Dot[".claude/"]
            PS[settings.json]
            PL[settings.local.json<br/>personal, not committed]
            PSK[skills/]
            PA[agents/]
            PH[hooks/]
            LJ[launch.json]
        end
        MCP[.mcp.json]
        SUB[src/CLAUDE.md<br/>nested, optional]
    end
    Global -. applies everywhere .-> Project
```

**Global vs. project** is the most important distinction in this module and the next one: almost everything (instructions, skills, subagents, hooks, settings) can live *globally* (just for you, everywhere) or *in the project* (for everyone who clones it).

➡️ Practice: [Lab 03 — CLAUDE.md](../labs/lab-03-claude-md.md) and [Lab 04 — settings.json](../labs/lab-04-settings.md)
