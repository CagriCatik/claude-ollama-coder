---
name: skill-template
description: Standardized template for authoring Claude Code conforming agent skills. Use when creating new skills, structuring SKILL.md frontmatter, adding executable scripts, defining progressive disclosure references, or establishing verification checklists.
license: Apache-2.0
compatibility: Claude Code, Anthropic Agent Skills Specification (agentskills.io)
metadata:
  author: claude-ollama-coder
  version: "1.0.0"
---

# Skill Name: Concise Descriptive Title

A clear, one-paragraph summary of what this skill does, its core philosophy, and what capability or behavioral standard it provides to the agent.

---

## 1. When to Use This Skill

Specify exact conditions, file patterns, commands, and scenarios when Claude Code should activate this skill:

- **Trigger Scenarios:**
  - When working on `[domain task, e.g. creating MCP servers, designing APIs, tuning models]`.
  - When editing files matching `[glob pattern, e.g. *.launch.py, Modelfile, pyproject.toml]`.
  - When encountering errors related to `[error symptoms, e.g. context overflow, QoS mismatch]`.
  - When the user asks to `[user intent, e.g. refactor database schema, review commit messages]`.

- **When NOT to Use:**
  - Do not use for simple one-off questions where standard knowledge suffices.
  - Do not use if the task is better handled by `[alternative skill, e.g. api-design vs software-architecture]`.

---

## 2. Core Principles & Rules

State the non-negotiable rules and mental model in imperative, direct language:

1. **Rule 1: Direct Actionable Guideline**
   - Explain *why* this rule exists.
   - Specify the concrete practice to follow.
2. **Rule 2: Boundary & Constraint**
   - State what the agent must *never* do.
   - Explain the failure mode avoided.
3. **Rule 3: Deterministic Execution**
   - Prefer deterministic scripts in `scripts/` over guessing or hallucinating commands.

---

## 3. Code Patterns & Best Practices

Provide copy-pasteable, concrete examples illustrating good practices vs anti-patterns:

### Recommended Pattern (DO THIS)
```python
# GOOD: Explicit, typed, resilient, and well-tested
def handle_event(payload: dict[str, Any]) -> Result:
    # 1. Validate inputs early
    if not payload.get("id"):
        raise ValueError("Missing required id field")
    
    # 2. Execute business logic cleanly
    return Result(success=True, data=payload)
```

### Anti-Pattern (AVOID THIS)
```python
# BAD: Silent failure, untyped, fragile
def handle_event(payload):
    try:
        return payload["data"]
    except Exception:
        return None  # Swallows root cause
```

---

## 4. Progressive Disclosure: References & Scripts

To preserve context window tokens, keep the primary `SKILL.md` body concise and delegate heavy reference material or deterministic workflows to subdirectories:

- **Reference Documentation:**
  - Read `references/detailed-guide.md` for in-depth protocol specifications and edge cases.
- **Deterministic Scripts:**
  - Run `python3 scripts/validate.py <input>` to mechanically test compliance before marking a task complete.

---

## 5. Self-Verification Checklist

Before concluding your task or presenting results to the user, verify every item:

- [ ] **Input Validation:** All user inputs and edge cases are safely sanitized and handled.
- [ ] **Type Safety:** Type hints and schemas are strictly specified without legacy fallbacks.
- [ ] **Surgical Edits:** Touched only the files and lines necessary to solve the user's request.
- [ ] **Tests & Verification:** Tested the changes locally (unit tests, command execution, or build).
- [ ] **Documentation:** Updated relevant documentation or comments without breaking existing formatting.
