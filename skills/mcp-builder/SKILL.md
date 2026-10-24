---
name: mcp-builder
description: Building and integrating Model Context Protocol (MCP) servers. Use when creating custom MCP servers in Python (FastMCP) or TypeScript, implementing MCP tools, resources, or prompts, configuring stdio or SSE transports in claude.json or settings.json, or debugging MCP tool-calling errors.
license: MIT
compatibility: Python >= 3.10, Node >= 18, Claude Code, Anthropic MCP SDK
metadata:
  author: claude-ollama-coder
  version: "1.0.0"
---

# MCP Server Builder & Integration Guide

Guidelines for creating, testing, and registering Model Context Protocol (MCP) servers to give Claude Code custom tools, real-time resources, and domain-specific prompts.

---

## When to Use This Skill

- **Trigger Scenarios:**
  - When building a new MCP server in Python (using FastMCP) or TypeScript (`@modelcontextprotocol/sdk`).
  - When exposing new tools (`@mcp.tool()`), resources (`@mcp.resource()`), or prompts to Claude Code.
  - When configuring `.claude.json`, `~/.claude/settings.json`, or workspace MCP configuration.
  - When deciding between `stdio` (local subprocess) and `sse` (HTTP Server-Sent Events) transports.
  - When debugging tool-call schema mismatches, serialization failures, or JSON-RPC timeouts.

- **When NOT to Use:**
  - Do not use for standard REST APIs that are not exposed via the Model Context Protocol (use `api-design`).
  - Do not use for prompt engineering alone when no external MCP server integration is required.

---

## 1. FastMCP Architecture (Python)

The modern standard for building Python MCP servers is **FastMCP**:

```python
#!/usr/bin/env python3
"""Local Database MCP Server for Claude Code."""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize server
mcp = FastMCP(
    name="Local Database Explorer",
    instructions="Provides read-only query capabilities against local SQLite database."
)

class QueryParams(BaseModel):
    query: str = Field(description="SQL SELECT query to execute (read-only)")
    max_rows: int = Field(default=50, ge=1, le=500, description="Maximum rows returned")

@mcp.tool()
def execute_sql(params: QueryParams) -> str:
    """Execute a read-only SQL query against the database."""
    # 1. Enforce read-only constraint
    cleaned = params.query.strip().upper()
    if not cleaned.startswith("SELECT") and not cleaned.startswith("PRAGMA"):
        raise ValueError("Only read-only SELECT and PRAGMA queries are allowed.")

    # 2. Execute query and serialize as markdown table or JSON
    # ... execution logic ...
    return "| id | name | status |\n|---|---|---|\n| 1 | demo | active |"

@mcp.resource("schema://main")
def get_database_schema() -> str:
    """Provide schema DDL as a dynamic context resource."""
    return "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, status TEXT);"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

## 2. Choosing Transports: `stdio` vs `sse`

| Transport | Best Used For | Configuration |
|---|---|---|
| **`stdio`** | Local developer machines, command-line tools, CLI wrappers | Claude Code spawns server as a child process via `stdin`/`stdout`. Zero network port exposure. |
| **`sse`** | Remote shared services, multi-user deployments, Docker containers | Server runs an HTTP service streaming events via SSE. |

### Registering `stdio` Server in `settings.json`

Add the server to `~/.claude/settings.json` or `.claude.json`:

```json
{
  "mcpServers": {
    "db-explorer": {
      "command": "python3",
      "args": ["/Users/username/projects/tools/mcp_db.py"],
      "env": {
        "DB_PATH": "/Users/username/data/production.db"
      }
    }
  }
}
```

---

## 3. Best Practices for MCP Tool Design

1. **Clear Descriptions Are Everything:**
   Claude selects tools based *entirely* on the tool docstring and parameter descriptions. Be explicit about prerequisites, units, and side effects.
2. **Type Annotations via Pydantic:**
   Always use typed Pydantic models or type hints. Untyped dictionary inputs cause tool invocation hallucinations.
3. **Structured Returns:**
   Return formatted markdown or compact JSON strings. Avoid emitting raw binary streams or noisy logs to standard output (it breaks `stdio` framing).
4. **Clean Stderr for Logging:**
   In `stdio` transport, `stdout` is reserved strictly for JSON-RPC messages. All debug logs **must** be written to `sys.stderr` or python `logging` with stderr handlers.

---

## 4. Debugging & Testing MCP Servers

Use the official MCP Inspector to test tools interactively before connecting Claude Code:

```bash
# Test FastMCP server with MCP Inspector
npx @modelcontextprotocol/inspector python3 my_mcp_server.py
```

Verify in Claude Code:
```bash
claude mcp list
claude mcp get db-explorer
```

---

## Self-Verification Checklist

Before concluding your MCP server development:
- [ ] Tool docstring clearly explains the tool's purpose, limitations, and side effects.
- [ ] All tool arguments have explicit types and parameter descriptions.
- [ ] All logging writes to `stderr` (`logging.basicConfig(stream=sys.stderr)`); `stdout` is reserved for JSON-RPC framing.
- [ ] Input mutations or destructive actions are guarded with explicit confirmation or safety constraints.
- [ ] Tested via `npx @modelcontextprotocol/inspector` or direct invocation before registering in `.claude.json`.
