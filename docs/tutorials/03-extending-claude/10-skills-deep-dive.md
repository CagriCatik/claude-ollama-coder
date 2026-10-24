# Claude Code Skills

## Table of contents

1. [What are skills](#what-are-skills)
2. [How skills trigger](#how-skills-trigger)
3. [The SKILL.md format](#the-skillmd-format)
4. [The marketplace system](#the-marketplace-system)
5. [Skills in this project](#skills-in-this-project)
6. [Adding a new skill with the template](#adding-a-new-skill-with-the-template)
7. [Writing effective skill descriptions](#writing-effective-skill-descriptions)
8. [Best practices](#best-practices)

---

## What are skills

Skills are reusable behavioral modules for Claude Code. A skill is a markdown file (`SKILL.md`) that contains guidelines Claude follows when a matching task is in scope. Skills do not add tools or external integrations — they shape how Claude reasons and responds within its existing capabilities.

Unlike a `CLAUDE.md` file (which is always active for a project), skills activate selectively based on the current task. A ROS2 skill fires when you are working on robot middleware code; a software architecture skill fires when you are designing systems. Unrelated work is unaffected.

```mermaid
flowchart LR
    A["User task"] --> B{"Skill match?"}
    B -->|Yes| C["Skill guidelines injected"]
    B -->|No| D["Normal Claude behavior"]
    C --> E["Response with skill context"]
    D --> E
```

Skills are distributed through a **marketplace** — a local or remote catalog of available skills. The Claude Code harness reads the marketplace, makes skills available, and handles triggering automatically.

---

## How skills trigger

Each skill has a `description` field in its YAML frontmatter. Claude Code's harness compares the current task against all enabled skill descriptions and injects the matching skill's content as behavioral context.

The description is the trigger mechanism. It must precisely name the conditions under which the skill applies. Vague descriptions cause the skill to fire too broadly or not at all.

**Examples of tight descriptions:**

- `Use when working with ROS2 nodes, packages, launch files, rclpy/rclcpp code...`
- `Use when designing APIs or interfaces, deciding on module/package structure...`
- `Use when writing, reviewing, or refactoring code to avoid overcomplication...`

Multiple skills can be active simultaneously if the task matches more than one description.

---

## The SKILL.md format

A skill file has two parts: a YAML frontmatter block and a markdown body.

```markdown
---
name: my-skill
description: One or two sentences describing exactly when this skill should activate. Be specific about the signals — file types, task types, domain concepts.
---

# Skill title

Body content: guidelines, rules, patterns, examples, tables.
Claude will follow this content when the skill is active.
```

### Frontmatter fields

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Unique identifier for the skill within its marketplace |
| `description` | Yes | Trigger condition — this is what the harness matches against |
| `license` | No | Optional license declaration |

### Body content

The body is free-form markdown. Write it as direct behavioral instructions. Use headings to organize topic areas, tables for decision matrices, and code blocks for patterns. Keep it actionable — Claude will follow these guidelines verbatim when the skill is active, so every section should say what to do, not just what to know.

---

## The marketplace system

Skills are grouped into **plugins** inside a **marketplace**. The marketplace is defined by a `marketplace.json` file.

### marketplace.json structure

```json
{
  "name": "user-skills",
  "owner": {
    "name": "Your Name"
  },
  "metadata": {
    "description": "Short description of this marketplace",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "user-skills",
      "description": "What these skills cover",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/my-skill-a",
        "./skills/my-skill-b"
      ]
    }
  ]
}
```

Each entry in `skills` is a path to a directory containing a `SKILL.md` file.

### How the harness finds the marketplace

`~/.claude/settings.json` registers marketplace sources and enables specific plugins:

```json
{
  "skills": {
    "sources": [
      {
        "type": "directory",
        "path": "/path/to/your/project"
      }
    ],
    "enabled": [
      "user-skills@user-skills"
    ]
  }
}
```

The `enabled` value uses the format `<marketplace-name>@<plugin-name>`.

```mermaid
flowchart TD
    A["~/.claude/settings.json"] -->|registers source| B[".claude-plugin/marketplace.json"]
    B -->|lists plugins| C["Plugin: user-skills"]
    C -->|references| D["skills/ros2/SKILL.md"]
    C -->|references| E["skills/software-engineering/SKILL.md"]
    C -->|references| F["skills/software-architecture/SKILL.md"]
    C -->|references| G["skills/karpathy-guidelines/SKILL.md"]
    D & E & F & G -->|activated by task match| H["Active skill context"]
```

---

## Skills in this project

This project ships 12 production skills plus a canonical template and conformance validator. They are defined in `skills/` and registered in `.claude-plugin/marketplace.json`.

| Skill | Path | Focus & Trigger Signals |
|---|---|---|
| **api-design** | `skills/api-design/SKILL.md` | REST/HTTP API design, RFC 7807 problem details, HTTP verbs and status codes, cursor vs offset pagination, idempotency keys. |
| **claude-code-workflows** | `skills/claude-code-workflows/SKILL.md` | Plan mode (`/plan`), context compacting (`/compact`), slash commands, subagents, headless runs (`claude -p`), git worktree isolation. |
| **git-workflow** | `skills/git-workflow/SKILL.md` | Conventional Commits, git worktrees for parallel Claude sessions, atomic commits, PR summaries, Co-Authored-By attribution. |
| **karpathy-guidelines** | `skills/karpathy-guidelines/SKILL.md` | Andrej Karpathy's LLM coding pitfalls: think before coding, simplicity first, surgical changes, verifiable success criteria. |
| **mcp-builder** | `skills/mcp-builder/SKILL.md` | Building MCP servers in Python (FastMCP) or TypeScript, tool/resource/prompt design, stdio vs SSE, testing with MCP Inspector. |
| **ollama-claude-bridge** | `skills/ollama-claude-bridge/SKILL.md` | Pointing Claude Code to local Ollama endpoints, environment variables, context sizing, model tags, tool-calling compatibility. |
| **ollama-modelfile-tuning** | `skills/ollama-modelfile-tuning/SKILL.md` | Ollama Modelfiles, expanding `num_ctx` to 64k, tuning sampling parameters, stop tokens, GPU layer offloading (`num_gpu`). |
| **python-modern-practices** | `skills/python-modern-practices/SKILL.md` | Modern Python 3.10+ typing, Pydantic v2 data models, async `httpx`, `pytest` fixtures and parametrization, `pyproject.toml`. |
| **ros2** | `skills/ros2/SKILL.md` | ROS2 Python/C++ development, node design, QoS profiles, launch files, colcon builds, TF2 transforms, lifecycle nodes. |
| **secure-coding** | `skills/secure-coding/SKILL.md` | Subprocess shell injection defense, canonical path traversal prevention, secret masking, input validation. |
| **software-architecture** | `skills/software-architecture/SKILL.md` | Macro patterns (monolith, microservices, hexagonal, CQRS), ADRs, cohesion vs coupling, state ownership, operations. |
| **software-engineering** | `skills/software-engineering/SKILL.md` | Multi-file interfaces, error hierarchies, domain organization, test strategy, structured observability, dependency injection. |
| **_template** | `skills/_template/SKILL.md` | Canonical authoring template conforming to `agentskills.io`, with progressive disclosure references and validation scripts. |

---

## Adding a new skill with the template

Adding a conforming skill takes three simple steps:

### Step 1: Copy the canonical template

```bash
cp -r skills/_template skills/my-new-skill
```

### Step 2: Edit `skills/my-new-skill/SKILL.md`

Configure the YAML frontmatter and author the instructions:

```markdown
---
name: my-new-skill
description: Precise trigger description. Use when working on X, editing files Y, or troubleshooting Z.
license: MIT
compatibility: Python >= 3.10, Claude Code
metadata:
  author: your-name
  version: "1.0.0"
---

# Skill Title

## When to Use This Skill
- **Trigger Scenarios:** ...
- **When NOT to Use:** ...

## Core Principles & Patterns
...

## Self-Verification Checklist
- [ ] Requirements verified.
```

### Step 3: Validate and register

1. **Run the built-in conformance linter:**
   ```bash
   python3 skills/_template/scripts/validate_skill.py skills/my-new-skill
   ```
2. **Register in `.claude-plugin/marketplace.json`:**
   Add `"./skills/my-new-skill"` to the `skills` array:
   ```json
   {
     "plugins": [
       {
         "name": "claude-ollama-coder-skills",
         "skills": [
           "...",
           "./skills/my-new-skill"
         ]
       }
     ]
   }
   ```

That is all. Claude Code will pick up the new skill on the next session start.

---

## Writing effective skill descriptions

The `description` field is the most important part of a skill. It is the only signal the harness uses to decide whether to activate the skill. A bad description means the skill never fires, fires constantly, or fires at the wrong time.

### Describe signals, not topics

Name the concrete signals that indicate the skill is relevant. File names, framework identifiers, task verbs, and domain nouns are all good signals. Abstract topic names are not.

| Weak | Strong |
|------|--------|
| "Software development" | "Use when designing APIs or interfaces, deciding on module/package structure..." |
| "Robotics" | "Use when working with ROS2 nodes, packages, launch files, rclpy/rclcpp code, CMakeLists.txt with ament..." |
| "Code quality" | "Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes..." |

### Be specific about task types

Name the task verbs that should trigger the skill: *designing*, *reviewing*, *debugging*, *choosing between*, *writing production code across multiple files*. This prevents the skill from activating on shallow mentions of the domain.

### Cover the full signal surface

List enough signals that a task in scope will match. A ROS2 skill that only mentions "ROS2 nodes" will miss tasks involving "launch files" or "colcon builds". Cover the realistic range of entry points into that domain.

### Avoid overlap with always-on context

Skills work alongside `CLAUDE.md`. Do not duplicate project-level context in a skill description. Skills are for domain-specific behavioral modes, not for project facts.

---

## Best practices

### Skill content

- Write instructions, not explanations. Each section should say what to do.
- Use tables for decision matrices (when to use X vs Y).
- Include code patterns where the correct form is non-obvious.
- Keep the file focused. One responsibility per skill.
- Name tradeoffs explicitly. A guideline without its tradeoff is incomplete.

### Skill organization

- One directory per skill. Do not put multiple skills in one `SKILL.md`.
- Name directories to match the `name` frontmatter field.
- Group related skills in the same plugin within `marketplace.json`.

### Skill maintenance

- Update descriptions when the domain grows. If the skill now covers new frameworks or file types, add them to the description.
- Version `marketplace.json` with the rest of the project. Skill changes are code changes.
- Test a new skill by running a task that should trigger it and confirming the behavior changed as expected.

---

## Related resources

- [Claude Code in Action](../04-daily-workflow/06-claude-code-in-action.md)
- [Agent Skills reference](08-agent-skills-guide.md)
- [MCP integration](06-mcp-expert-guide.md)
