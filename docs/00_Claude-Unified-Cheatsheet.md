# Claude Unified Cheatsheet

This is the compact reference I would want open while using Claude for real work: prompting, Claude Code, API calls, tools, MCP, review workflows, and production habits. It avoids hype and focuses on patterns that hold up after many sessions.

Last reviewed: 2026-05-13.

---

## Fast Defaults

Use these defaults unless you have a reason not to.

| Situation | Default choice | Why |
|-----------|----------------|-----|
| General coding and writing | Sonnet | Best balance of speed, quality, and cost |
| Hard architecture or agent planning | Opus | Stronger reasoning for ambiguous work |
| Cheap classification, extraction, routing, drafts | Haiku | Fastest and cheapest useful tier |
| Production API model IDs | Pin a specific model ID | Avoid silent behavior changes |
| Claude Code model picker | Use `/model` | Change model without restarting |
| Long coding sessions | Keep context curated | More context is not always better context |
| Factual or current questions | Ask Claude to use sources or tools | Claude's memory is not live data |
| Machine output | Specify exact schema | Never trust formatting by implication |

Current Claude family names change over time. Check the official model list before publishing model tables. As of this review, the practical defaults are Opus 4.7 for the hardest work, Sonnet 4.6 for most work, and Haiku 4.5 for fast work.

---

## How I Prompt Claude

The best prompt is usually not long. It is specific, grounded, and testable.

Use this structure:

```text
Goal:
What I want done and what success looks like.

Context:
Relevant files, constraints, users, environment, examples, or prior decisions.

Task:
The exact work to perform.

Constraints:
- Format:
- Length:
- Style:
- Must include:
- Must avoid:

Output:
The exact shape I want back.
```

Example:

```text
Goal:
Improve this API documentation so a backend engineer can implement the endpoint without asking follow-up questions.

Context:
The endpoint creates customer webhooks. It is used by partner integrations. Security matters more than brevity.

Task:
Rewrite the docs for clarity and completeness.

Constraints:
- Keep Markdown.
- Do not invent fields.
- Mark missing information as "Needs confirmation".
- Include one successful request and one error response.

Output:
Return the rewritten Markdown only.
```

---

## Prompt Patterns That Work

| Pattern | Use it for | Prompt fragment |
|---------|------------|-----------------|
| Plan first | Large changes | "Read the relevant files, then propose a short plan before editing." |
| Review mode | Quality checks | "Review this like a senior maintainer. Findings first, then summary." |
| Patch mode | Code edits | "Make the smallest safe change and run the relevant tests." |
| Comparison | Design choices | "Give me three viable approaches with tradeoffs and a recommendation." |
| Schema output | Automation | "Return valid JSON matching this schema. No prose." |
| Critique pass | Improving drafts | "Identify unclear claims, missing assumptions, and weak structure." |
| User empathy | Product text | "Rewrite for a tired user trying to finish the task quickly." |
| Source-grounded | Research | "Use only the provided sources. Cite each claim." |

Avoid asking for hidden chain of thought. Ask for the useful artifact instead:

```text
Bad:
Think step by step and show all reasoning.

Good:
Give the decision, the key assumptions, and the checks that would change the decision.
```

---

## Claude Code Workflow

Claude Code is strongest when you treat it like a careful engineer, not a command autocomplete.

### Starting a Session

```bash
claude
```

Useful first requests:

```text
Read the README, package files, and test setup. Summarize how this project is built and tested.
```

```text
Inspect the relevant files for the bug below. Do not edit yet. Tell me the smallest safe fix.
```

```text
Implement the fix, keep the patch scoped, and run the relevant tests.
```

### Model Selection

Inside Claude Code:

```text
/model
```

Practical rule:

- Use Sonnet for normal implementation.
- Use Opus for unclear design, deep debugging, or high-risk refactors.
- Use Haiku for quick checks, background tasks, and simple classification.
- Use `opusplan` where available when you want Opus for planning and Sonnet for execution.

For teams, pin defaults through configuration rather than relying on whatever "default" resolves to that week.

### Context Hygiene

Good Claude Code sessions are mostly about context control.

Do:

- Point Claude at the relevant files.
- Ask for a plan before broad edits.
- Keep one task per session when possible.
- Ask it to run tests after implementation.
- Ask for file and line references in reviews.
- Reset or compact when the thread becomes noisy.

Avoid:

- Pasting huge logs without the failing section.
- Mixing unrelated tasks in one request.
- Asking for broad refactors without ownership boundaries.
- Letting Claude edit before it has read the project conventions.

---

## API Basics

Install:

```bash
pip install anthropic
```

Set the key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Minimal request:

```python
import os
from anthropic import Anthropic


client = Anthropic()
MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

message = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    temperature=0.2,
    system="You are a concise technical assistant.",
    messages=[
        {"role": "user", "content": "Explain retry with exponential backoff."}
    ],
)

print(message.content[0].text)
print(message.stop_reason)
print(message.usage)
```

### Multi-Turn State

Claude does not remember API turns unless you send the conversation history.

```python
messages = [
    {"role": "user", "content": "Explain Python context managers in one paragraph."}
]

first = client.messages.create(
    model=MODEL,
    max_tokens=512,
    messages=messages,
)

messages.append({"role": "assistant", "content": first.content})
messages.append({"role": "user", "content": "Now show a file handling example."})

second = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    messages=messages,
)
```

### Streaming

Use streaming for long responses, interactive UIs, and avoiding HTTP timeouts on large outputs.

```python
with client.messages.stream(
    model=MODEL,
    max_tokens=2048,
    messages=[{"role": "user", "content": "Draft a migration checklist."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

---

## Tool Use

Tools let Claude request external actions. Your application still executes the tools and sends results back.

### Tool Schema

```python
tools = [
    {
        "name": "get_order_status",
        "description": "Read the status of one customer order. This is read-only.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The public order ID, for example ord_123"
                }
            },
            "required": ["order_id"]
        }
    }
]
```

### Tool Loop

```python
messages = [
    {"role": "user", "content": "What is the status of order ord_123?"}
]

while True:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason != "tool_use":
        print(response.content[0].text)
        break

    tool_results = []

    for block in response.content:
        if block.type != "tool_use":
            continue

        if block.name == "get_order_status":
            result = get_order_status(block.input["order_id"])
        else:
            result = {"error": f"Unknown tool: {block.name}"}

        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": str(result),
        })

    messages.append({"role": "user", "content": tool_results})
```

### Tool Design Rules

- Prefer narrow tools over one giant tool.
- Put side effects in the name and description.
- Validate every argument.
- Return compact structured data.
- Include stable IDs and URLs when useful.
- Make errors actionable so Claude can retry.
- Put permission checks in code, not in the prompt.

Good:

```text
create_refund_draft
```

Risky:

```text
run_customer_action
```

---

## MCP With Claude

Model Context Protocol is how Claude hosts connect to reusable external tools, resources, and prompts.

Think of MCP like this:

| Primitive | Who controls it | Use for |
|-----------|-----------------|---------|
| Tool | Claude decides when to call | Actions and queries |
| Resource | Host decides what to attach | Files, docs, schemas, records |
| Prompt | User triggers a workflow | Reusable commands |

### Add an MCP Server in Claude Code

Remote HTTP server:

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

Local stdio server:

```bash
claude mcp add --transport stdio docs -- uv run python server.py
```

Manage servers:

```bash
claude mcp list
claude mcp get docs
claude mcp remove docs
```

Inside Claude Code:

```text
/mcp
```

### Reference MCP Resources

Use `@` mentions when the MCP server exposes resources:

```text
Review @docs:file://api/authentication and identify missing setup steps.
```

Resource references are best for large context. Tool calls are best for actions.

---

## Output Formats

Claude is good at following formats when the format is explicit.

### JSON

```text
Return valid JSON only:

{
  "summary": "string",
  "risks": ["string"],
  "next_actions": ["string"],
  "confidence": "low|medium|high"
}
```

### Markdown Review

```text
Return:

## Findings

Each finding must include severity, file, line, impact, and fix.

## Open Questions

Only include questions that block a safe recommendation.

## Summary

Two sentences max.
```

### Patch Request

```text
Make the smallest safe code change.

Requirements:
- Preserve public behavior except for the bug fix.
- Follow existing project style.
- Add or update tests if behavior changes.
- Run the relevant test command.

Return:
- Files changed
- Tests run
- Any remaining risk
```

---

## High-Value Workflows

### Code Review

```text
Review this change as a maintainer.

Prioritize:
1. Bugs and regressions.
2. Security issues.
3. Missing tests.
4. Maintainability issues that will hurt soon.

Give findings first. Include file and line references. Skip praise unless it affects the recommendation.
```

### Debugging

```text
I am seeing this failure:

[paste exact error]

Relevant code:

[paste or reference files]

Please:
1. Identify the most likely cause.
2. Show the smallest fix.
3. Explain what test would prove it.
```

### Refactoring

```text
Refactor this module for readability without changing behavior.

Before editing:
1. Identify the public behavior that must stay stable.
2. Identify the tests that should catch regressions.
3. Propose the smallest sequence of changes.
```

### Documentation Rewrite

```text
Rewrite this documentation for an experienced developer who wants to implement quickly.

Keep:
- Accurate technical details
- Commands and examples
- Existing links when still valid

Improve:
- Structure
- Missing prerequisites
- Ambiguous wording
- Outdated model or tool names

Remove:
- Marketing language
- Decorative symbols
- Redundant explanations
```

### Research

```text
Use only the sources I provide.

For each claim:
- Cite the source.
- Say when you are inferring.
- Mark anything not supported as "not established".

Return a concise synthesis, not a source-by-source summary.
```

---

## Production Habits

### Request Settings

| Setting | Practical guidance |
|---------|--------------------|
| `model` | Pin in production; use aliases only for experiments |
| `max_tokens` | Set it explicitly |
| `temperature` | Lower for factual or code tasks; higher for brainstorming |
| `system` | Use for durable role and policy, not task details |
| `messages` | Include only context needed for the current turn |
| `tools` | Keep schemas focused and clear |
| `stream` | Use for long or interactive responses |

### Error Handling

Handle these cases deliberately:

```python
if response.stop_reason == "end_turn":
    handle_final_answer(response)
elif response.stop_reason == "max_tokens":
    handle_truncated_answer(response)
elif response.stop_reason == "tool_use":
    handle_tool_requests(response)
elif response.stop_reason == "stop_sequence":
    handle_stop_sequence(response)
else:
    handle_unknown_stop_reason(response)
```

Use backoff for transient failures:

```python
import time
from anthropic import APIConnectionError, APITimeoutError, RateLimitError


for attempt in range(5):
    try:
        return client.messages.create(...)
    except (APIConnectionError, APITimeoutError, RateLimitError):
        if attempt == 4:
            raise
        time.sleep(2 ** attempt)
```

### Security

Do not treat the model as the security boundary.

Checklist:

- Keep secrets out of prompts and logs.
- Validate tool inputs server-side.
- Require confirmation for destructive actions.
- Scope API keys narrowly.
- Redact sensitive tool results.
- Use read-only credentials for analysis tools.
- Treat retrieved web pages, tickets, issues, and docs as untrusted input.
- Log tool calls with request IDs.

---

## Cost and Context Control

The cheapest token is the one you do not send.

Practical rules:

- Summarize old context before it becomes huge.
- Use retrieval instead of pasting entire folders.
- Use resources for large reference documents.
- Use Haiku for extraction and routing.
- Use Sonnet for most execution.
- Use Opus when wrong answers cost more than extra tokens.
- Cache stable system prompts and large repeated context where supported.
- Avoid returning giant tool payloads; return IDs plus summaries.

Token intuition:

- A token is roughly a few characters of English text.
- Long code, logs, JSON, and tables can be token-heavy.
- Output tokens often cost more than input tokens.
- `max_tokens` is a budget, not a target.

---

## Common Mistakes

| Mistake | Better habit |
|---------|--------------|
| "Fix everything in this repo" | Give one scoped task and relevant files |
| "Make it better" | Define success criteria |
| Pasting stale docs | Ask Claude to verify against current source |
| Trusting generated JSON blindly | Validate with a parser |
| Tool descriptions as policy | Enforce policy in code |
| Huge context dumps | Use targeted files and summaries |
| Ignoring `stop_reason` | Branch on it explicitly |
| Using Opus for every task | Save it for high-risk reasoning |
| Skipping tests | Ask Claude to run or explain the relevant tests |
| Letting a session sprawl | Start fresh when context becomes noisy |

---

## Task Reference

| Task | Best prompt shape | Model bias |
|------|-------------------|------------|
| Implement a feature | Goal, relevant files, constraints, tests | Sonnet |
| Debug failing tests | Exact error, test command, changed files | Sonnet or Opus |
| Architecture decision | Requirements, tradeoffs, constraints | Opus |
| Code review | Diff, risk areas, review criteria | Sonnet or Opus |
| Data extraction | Schema, examples, validation rules | Haiku or Sonnet |
| Summarization | Audience, length, must-keep details | Haiku or Sonnet |
| Documentation | Audience, scope, source material | Sonnet |
| Brainstorming | Goal, constraints, examples to avoid | Sonnet |
| Classification | Labels, definitions, examples | Haiku |
| Long agentic coding | Plan, checkpoints, test command | Sonnet with Opus planning |

---

## Claude Code Commands I Actually Use

```text
/model
```

Change model for the current session.

```text
/mcp
```

Inspect and authenticate MCP servers.

```text
/compact
```

Compress a long conversation when useful context is getting buried.

```text
/clear
```

Start fresh when the session has drifted.

```text
/help
```

Check available commands in your installed Claude Code version.

---

## Local Ollama Setup Notes

This repository is about using a Claude-style workflow with local models through Ollama. When working locally, separate three things:

| Layer | Example | Responsibility |
|------|---------|----------------|
| CLI | `claude` | Developer workflow |
| API compatibility | `ANTHROPIC_API_URL=http://localhost:11434/v1` | Request routing |
| Model runtime | Ollama | Local inference |

Typical setup:

```bash
ollama serve
ollama pull qwen3-coder

export ANTHROPIC_API_KEY=sk-dummy
export ANTHROPIC_API_URL=http://localhost:11434/v1

claude -p "Explain this repository structure"
```

When using local models, expect differences from Anthropic-hosted Claude:

- Tool behavior may vary.
- Long context behavior may vary.
- Coding quality depends heavily on the local model.
- Model IDs may need to match your gateway or Ollama compatibility layer.

---

## Experienced User Rules

1. Start with the smallest clear task.
2. Give Claude the files it needs, not the whole world.
3. Ask for a plan before broad edits.
4. Make output formats explicit.
5. Treat tools as code paths with permissions, not magic.
6. Prefer resources over huge pasted context.
7. Use Sonnet as the daily driver.
8. Save Opus for the hard thinking.
9. Use Haiku where speed matters more than nuance.
10. Verify anything current, legal, financial, medical, or security-sensitive.
11. Run tests after code changes.
12. Reset the session when context quality drops.

---

## Learn More

- [Claude Code in Action](01_Claude-Code-in-Action.md)
- [Claude 101](02_Claude-101.md)
- [AI Fluency Framework](03_AI-Fluency-Framework-Foundations.md)
- [Building with the Claude API](04_Building-with-the-Claude-API.md)
- [Model Context Protocol](05_MCP.md)
- [Advanced MCP Patterns](06_MCP-Advanded.md)
- [Agent Skills](07_Agent-Skills.md)
- [Subagents and Orchestration](08_Subagents.md)

Official references:

- [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Streaming Messages API](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config)
- [Claude Code MCP](https://code.claude.com/docs/en/mcp)
