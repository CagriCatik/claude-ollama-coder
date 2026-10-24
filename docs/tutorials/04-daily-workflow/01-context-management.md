# 1. Context Management

The **context window** is everything Claude currently "sees": system prompt, tools, skills, `CLAUDE.md`, and the whole conversation including tool output. It's measured in tokens (the version shown had a 1M-token window).

## Why it matters

```mermaid
flowchart LR
    Big[Context grows] --> Cost[💸 Each message costs more usage]
    Big --> Err[🐛 Near the limit, more mistakes]
```

Every message re-sends the context, so a bloated session is both **expensive** and **less accurate**.

## What fills it

```mermaid
pie showData
    title Example session (tokens, thousands)
    "System prompt, tools, skills (fixed)" : 37
    "CLAUDE.md & memory" : 5
    "Conversation" : 40
    "Tool output (file reads, logs)" : 72
```

Click the context indicator at the bottom of the session (or run `/context`) for a detailed breakdown.

## The three commands

| Command | Effect | When |
|---|---|---|
| `/context` | Show usage % and breakdown | Anytime you're curious |
| `/compact` | Summarize the conversation, replace history with the summary | Long session, same task, getting heavy |
| `/clear` | Wipe the conversation, start fresh in the same window | Switching to an unrelated task |

```mermaid
flowchart TD
    Q{Next thing you'll do}
    Q -->|Same task, continue| K{Context > ~70%?}
    K -->|yes| Compact["/compact"]
    K -->|no| Go[Keep going]
    Q -->|Different task| Clear["/clear (or new session)"]
```

> Claude auto-compacts near the limit, so `/compact` is optional — but doing it yourself at a natural break gives a better summary.
> In the video, `/clear` dropped the session to ~37k tokens: that's the fixed baseline from tools and skills.

## Habits
- **One task per session.** New topic → `/clear` or a new session.
- **Use subagents** for exploration-heavy side tasks ([Subagents](../03-extending-claude/02-subagents.md)).
- **Keep `CLAUDE.md` lean** — it's in every session.
- **Disconnect unused MCP servers** — their tool descriptions cost tokens.
- `/usage` shows your plan's usage limits.

➡️ Next: [Rewind](02-rewind.md)
