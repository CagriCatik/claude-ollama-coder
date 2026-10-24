# Claude Code Cheatsheet

## Slash commands

| Command | Does |
|---|---|
| `/init` | Generate `CLAUDE.md` for the project |
| `/context` | Show context-window usage & breakdown |
| `/usage` | Show plan usage limits |
| `/compact` | Summarize conversation to free context |
| `/clear` | Start fresh in the same window |
| `/rewind` | Jump back to a checkpoint (conversation, code, or both) |
| `/code-review` | Review current changes without editing |
| `/status` | Show model, API base URL, and context window |
| `/loop <int> <cmd>` | Run prompt/command on a recurring schedule (Ollama) |
| `/skills` | Browse, view and install skills |
| `/mcp` | Manage MCP servers |
| `/plugins` | Browse and install plugins |
| `/<skill-name>` | Run a skill |
| `↑` / `↓` | Cycle through previous prompts |
| `@file` | Reference a file, folder or session |

## Decision tables

**Model** — Haiku (simple/bulk) · Sonnet (balanced, save usage) · **Opus (default)** · Fable (rare, hardest)

**Effort** — Low (prototype) · **Medium (default)** · High (tricky) · Extra/Max (critical) · Ultra (audits, overnight)

**Mode** — Manual · **Plan (new work)** · Accept edits · **Auto (default)** · Bypass (sandbox only)

## File locations

| What | Project (shared) | Global (just you) |
|---|---|---|
| Instructions | `CLAUDE.md`, `sub/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| Settings | `.claude/settings.json` (+ `settings.local.json`) | `~/.claude/settings.json` |
| Skills | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| Subagents | `.claude/agents/<name>.md` | `~/.claude/agents/<name>.md` |
| Hooks | in `settings.json` → scripts in `.claude/hooks/` | in `~/.claude/settings.json` |
| MCP | `.mcp.json` | user config via `claude mcp add` |
| Memory | ask to store "in the project" | `~/.claude/projects/<project>/memory/` |

## Snippets

```json
// .claude/settings.json — permissions
{ "permissions": {
    "allow": ["Bash(npm test:*)", "Edit(src/**)"],
    "ask":   ["Bash(npm install:*)"],
    "deny":  ["Read(.env)"] } }
```

```json
// .claude/settings.json — hook
{ "hooks": { "Stop": [ { "hooks": [
    { "type": "command", "command": ".claude/hooks/notify.sh" } ] } ] } }
```

```markdown
<!-- .claude/skills/<name>/SKILL.md -->
---
name: my-skill
description: What it does and WHEN Claude should use it.
---
Step-by-step instructions…
```

```markdown
<!-- .claude/agents/<name>.md -->
---
name: reviewer
description: When to delegate to this agent.
tools: Read, Grep, Glob
model: sonnet
---
System instructions for the subagent…
```

```bash
# Ollama — One-liner launch or headless run
ollama launch claude
ollama launch claude --model gemma4:cloud --yes -- -p "how does this repo work?"

# Ollama — Manual environment variables (local or cloud)
export ANTHROPIC_BASE_URL=http://localhost:11434  # or https://ollama.com
export ANTHROPIC_AUTH_TOKEN=ollama               # or "$OLLAMA_API_KEY"
export ANTHROPIC_API_KEY=""
claude --model qwen3.5
```

## Ollama CLI Quick Reference (Module 07)

| Command | Action |
|---|---|
| `ollama list` | List installed and cloud models |
| `ollama ps` | Show active models loaded in memory |
| `ollama launch claude` | Launch Claude Code with Ollama model |
| `ollama launch claude --config` | Interactively select/switch model |
| `ollama run <model>` | Direct terminal chat without Claude Code |
| `ollama rm <model>` | Delete model to free disk space |
| `ollama show <model> --modelfile` | Inspect context window (`num_ctx`) & parameters |

## Learning workflow (Module 06)

| Stage | You | Claude | Research notebook |
|---|---|---|---|
| **Collect** | Goal, depth, background, good-source criteria | Drafts prompt, audits source list | Deep research → curated library |
| **Understand** | Compress to ≤ 5 questions, pick a format | Suggests questions, builds interactive pages | Answers from the library; tables & decks *from your answers* |
| **Own** | Decide what to keep: questions, artifacts, link | Designs & builds the archive, answers "what did I learn?" | Source of truth via link |

Audit flags: duplicates · possibly fabricated · SEO/marketing · wrong focus · missing primary sources.

## Habits
1. Open a **folder** first.
2. **Plan mode** + "ask me questions" for anything new.
3. Name your **stack** explicitly.
4. `/init` once the project has a shape.
5. **One task per session**; `/clear` between topics.
6. Repeated instructions → **skill**. Must-always-happen → **hook**. Context-heavy side job → **subagent**.
7. Commit often; `/rewind` is a safety net, not a VCS.
8. You don't need to memorize anything — **ask Claude to set it up**.
9. When learning, be the **client, not the audience**: AI carries the load, you choose the focus.
