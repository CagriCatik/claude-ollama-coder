# 2. Memory

To make Claude remember something, just say so:

```text
Remember that our CI runs on Python 3.11 and we deploy every Thursday.
```

## Where it goes

```mermaid
flowchart TD
    A["You: 'Remember X'"] --> B{Private or shared?}
    B -->|Default: private| C["~/.claude/projects/&lt;project&gt;/memory/<br/>on your machine only<br/>NOT in git"]
    B -->|"You say: 'store this in the project'"| D["Inside the project folder<br/>(e.g. CLAUDE.md or a memory file)<br/>committed with the repo"]
    C --> E[Loaded in future sessions of this project]
    D --> E
```

| Kind | Location | Who sees it | Use for |
|---|---|---|---|
| **Private memory** | Your user `.claude` directory, per project | Only you, on this machine | Your name, personal preferences, local paths |
| **Project memory** | Inside the repo (`CLAUDE.md` or a memory file) | Everyone who clones | Team decisions, conventions |

> The video's surprise moment: Claude said "remembered", but no file appeared in the project — because the default memory is stored **outside** the repo. Ask explicitly if you want it in the project.

## Memory vs. CLAUDE.md

| | CLAUDE.md | Memory |
|---|---|---|
| Written by | You (or Claude via `/init`) | Claude, when you ask it to remember |
| Purpose | Rules and project description | Facts and preferences picked up along the way |
| Shared | Yes (in repo) | Private by default |

## Chat app memory (claude.ai)
The regular Claude app also has memory: it learns from your chats, you can edit it in **Settings → Memory**, import memory from other assistants, and use **incognito chats** that don't read or write memory. See [Projects & memory](../05-beyond-code/01-projects-and-memory.md).

➡️ Next: [settings.json](03-settings-json.md)
