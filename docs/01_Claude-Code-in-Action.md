# Claude Code in Action: Complete Guide

## Table of Contents

1. [Understanding Coding Assistants](#understanding-coding-assistants)
2. [Claude Code Fundamentals](#claude-code-fundamentals)
3. [Context Management](#context-management)
4. [Making Effective Changes](#making-effective-changes)
5. [Controlling Context Flow](#controlling-context-flow)
6. [Custom Commands](#custom-commands)
7. [MCP Server Integration](#mcp-server-integration)
8. [GitHub Integration](#github-integration)
9. [Hooks System](#hooks-system)
10. [Advanced Hook Patterns](#advanced-hook-patterns)
11. [Claude Code SDK](#claude-code-sdk)

---

## Understanding Coding Assistants

### What is a Coding Assistant?

A coding assistant is an AI-powered tool that leverages language models to automate software development tasks. Unlike traditional IDEs, coding assistants understand context, reason about problems, and execute complex workflows autonomously.

### Core Architecture

```mermaid
graph LR
    A["User Task<br/>(e.g., fix bug)"] --> B["Language Model"]
    B --> C["Context Gathering<br/>(read files)"]
    C --> D["Analysis & Planning<br/>(understand problem)"]
    D --> E["Action Execution<br/>(edit files, run tests)"]
    E --> F["Result Delivery"]
    
    style A fill:#0d2718,stroke:#00a67e,color:#e2e8f0
    style F fill:#0d2718,stroke:#00a67e,color:#e2e8f0
```

### Tool Use System: How It Works

The fundamental advantage of Claude Code lies in its **tool use system**:

```mermaid
sequenceDiagram
    participant User
    participant LLM as Language Model
    participant System as Claude Code System
    participant Filesystem

    User->>LLM: Task request
    LLM->>LLM: Evaluate task requirements
    LLM->>System: Request to read file X
    System->>Filesystem: Read file X
    Filesystem-->>System: File content
    System-->>LLM: Return content
    LLM->>LLM: Analyze and plan solution
    LLM->>System: Request to edit file Y
    System->>Filesystem: Write changes
    Filesystem-->>System: Confirm success
    System-->>LLM: Confirmation
    LLM-->>User: Task complete with results
```

### Key Advantages

**Claude's Tool Use Superiority:**
- ✅ Superior understanding of function contexts
- ✅ Better at combining multiple tools for complex tasks  
- ✅ Extensible architecture for custom tools
- ✅ Direct code search instead of external indexing (better security)
- ✅ Adaptive to development changes

---

## Claude Code Fundamentals

### Real-World Examples

#### Example 1: Performance Optimization

Claude analyzed the **Chalk JavaScript library** (429M weekly downloads):

```
Step 1: Analyzed benchmarks and profiling data
Step 2: Identified performance bottlenecks
Step 3: Implemented optimizations
Step 4: Verified improvements with tests

Result: 3.9x throughput improvement
```

#### Example 2: Data Analysis Workflow

```python
# Claude's workflow for churn analysis
1. Load CSV data from S3
2. Explore data structure and patterns
3. Execute analysis in Jupyter notebook cells
4. Visualize findings with charts
5. Iterate on hypotheses based on results
6. Generate final report
```

#### Example 3: Browser Automation with Playwright

```mermaid
graph LR
    A["Claude Code"] -->|Controls| B["Playwright MCP Server"]
    B -->|Automates| C["Browser"]
    C -->|Renders| D["UI Components"]
    D -->|Analyzed by| A
    A -->|Updates prompts| E["Generation Logic"]
    E -->|Improves| D
```

### Default Tools

Claude Code ships with essential tools:

| Tool | Purpose | Example |
|------|---------|---------|
| `read` | Read file contents | `read src/index.ts` |
| `edit` | Create/modify files | `edit src/app.tsx` |
| `grep` | Search across files | `grep "function" --include="*.js"` |
| `run` | Execute commands | `run npm test` |
| `bash` | Shell operations | `bash -c "git status"` |

---

## Context Management

### The Problem: Context Quality

Too much irrelevant context degrades Claude's performance. The solution: **strategic context provision**.

```mermaid
graph TB
    A["Irrelevant Context"] -->|Decreases| B["Model Performance"]
    C["Optimal Context"] -->|Increases| B
    
    style A fill:#2d1212,stroke:#ef4444,color:#e2e8f0
    style C fill:#0d2718,stroke:#00a67e,color:#e2e8f0
```

### The `/init` Command

The `/init` command analyzes your entire codebase and creates a `Claude.md` summary:

```bash
/init
```

**Generated file includes:**
- Project summary
- Architecture overview
- Key files and their purposes
- Dependencies and relationships

### Three-Level Claude.md Strategy

```mermaid
graph LR
    A["Global<br/>Machine Level"] -->|Lowest Priority| D["Context Stack"]
    B["Project<br/>Team Level"] -->|Medium Priority| D
    C["Local<br/>Personal Level"] -->|Highest Priority| D
    
```

**Implementation:**

```markdown
# Claude.md - Project Level

## Overview
Backend API for e-commerce platform

## Architecture
- Express.js server
- PostgreSQL database
- Redis cache
- Stripe integration

## Key Files
- `src/server.ts` - Main server
- `src/database.ts` - Database layer
- `src/api/routes.ts` - API endpoints

## Critical Schema
@database.ts - Contains core data models
```

### Context Commands

```bash
# Mention specific files for targeted context
@src/database.ts
@src/server.ts

# Or use file patterns
@src/**/*.ts
```

**Best Practices:**
- Include database schemas in Claude.md
- Reference architecture diagrams
- Link critical configuration files
- Update before major refactors

---

## Making Effective Changes

### Screenshot Integration

Paste screenshots directly to help Claude understand UI context:

```
Keyboard: Ctrl+V (Windows/Linux) or Cmd+V (macOS)
```

### Performance Boosting Modes

#### Plan Mode

Enables extended research and planning:

```
Keyboard Shortcut: Shift+Tab twice
Effect: Claude researches files and creates detailed plans before executing
Use Case: Multi-step tasks, significant refactors
```

**Plan Mode Workflow:**

```mermaid
graph LR
    A["Task Request"] --> B["Plan Mode<br/>Shift+Tab x2"]
    B --> C["Extensive<br/>File Research"]
    C --> D["Create Detailed<br/>Implementation Plan"]
    D --> E["Execute Plan<br/>Step by Step"]
    E --> F["Verify Results"]
```

#### Thinking Mode

Provides extended reasoning for complex logic:

```
Trigger Phrases: "Ultra think", "Deep analysis"
Effect: Claude gets extended token budget for complex reasoning
Use Case: Debugging, algorithm design, architectural decisions
```

### Git Integration

Claude Code can manage version control automatically:

```bash
# Claude can:
1. Examine git diff
2. Stage changes
3. Create commits with descriptive messages
4. Push to remote repository
```

---

## Controlling Context Flow

### Context Control Commands

```mermaid
graph TB
    A["Press Escape"] -->|Single| B["Stop & Redirect"]
    A -->|Double| C["Conversation Rewind"]
    
    D["Escape + Memory"] -->|Prevent| E["Repeated Mistakes"]
    
    F["/compact"] -->|Summarize| G["Preserve Knowledge"]
    
    H["/clear"] -->|Fresh Start| I["New Task"]
    
    style E fill:#2d1212,stroke:#ef4444,color:#e2e8f0
    style G fill:#0d2718,stroke:#00a67e,color:#e2e8f0
```

### Practical Usage

**Escape (Single Press):**
```
User: "Claude, let me interrupt here..."
Effect: Claude stops mid-response, awaits new direction
```

**Escape + Memory (# shortcut):**
```
/memory
Note: Claude frequently forgets to update related files.
Always check for dependent functions after signature changes.

Effect: Prevents repeated mistake in future interactions
```

**Double Escape (Conversation Rewind):**
```
Effect: 
- Shows all previous messages
- Skip debugging/back-and-forth
- Jump to earlier point with context intact
```

**Compact Command:**
```
/compact
Effect:
- Summarizes conversation history
- Preserves Claude's learned knowledge
- Removes clutter from context
```

---

## Custom Commands

### What Are Custom Commands?

Custom commands are reusable workflows stored in your project:

```mermaid
graph LR
    A["Create Command<br/>.Claude/commands/"] --> B["command.md<br/>with instructions"]
    B --> C["Run with /command"]
    C --> D["Pass arguments<br/>if needed"]
    
```

### Implementation

**File Structure:**
```
project/
├── .Claude/
│   ├── commands/
│   │   ├── audit.md
│   │   ├── test-gen.md
│   │   └── security-check.md
│   └── settings.local.json
```

**Example: Dependency Audit Command**

```markdown
# audit.md

You are a dependency auditor. Your task is to:

1. Examine package.json for all dependencies
2. Check for outdated packages
3. Identify security vulnerabilities
4. Suggest updates with compatibility notes

Focus on: $arguments

Run commands:
- npm outdated
- npm audit
- npm audit fix --dry-run

Report findings with:
- Critical vulnerabilities first
- Suggested version updates
- Breaking change warnings
```

**Usage:**
```bash
/audit frontend
/audit backend
/audit all
```

---

## MCP Server Integration

### What is MCP?

**Model Context Protocol (MCP)** extends Claude Code with external capabilities:

```mermaid
graph LR
    A["Claude Code"] -->|Communicates via| B["MCP Client"]
    B -->|Connects to| C["MCP Server"]
    C -->|Controls| D["External System"]
    
    subgraph "Examples"
        E["Playwright Server<br/>Browser Automation"]
        F["GitHub Server<br/>Repository Access"]
        G["Database Server<br/>Query Execution"]
    end
    
    D -.->|Examples| E
    D -.->|Examples| F
    D -.->|Examples| G
    
```

### Installing MCP Servers

```bash
# Add Playwright server for browser automation
claude mcp add playwright "npx @claudeai/playwright-mcp"

# Add GitHub server for repository operations
claude mcp add github "npx @claudeai/github-mcp"
```

### Playwright MCP Workflow

```mermaid
sequenceDiagram
    participant Claude as Claude Code
    participant Playwright as Playwright MCP
    participant Browser
    participant App as Web App

    Claude->>Playwright: navigate(localhost:3000)
    Playwright->>Browser: Open URL
    Browser->>App: Load page
    App-->>Browser: Render UI
    Browser-->>Playwright: Screenshot
    Playwright-->>Claude: Image data
    Claude->>Claude: Analyze styling
    Claude->>Playwright: Update CSS
    Playwright->>App: Modify styles
    App-->>Browser: Rerender
    Claude->>Playwright: Take screenshot
    Playwright-->>Claude: Verify changes
```

### Permission Management

```json
// settings.local.json
{
  "allowTools": [
    "read",
    "edit",
    "run"
  ],
  "autoApproveMCP": {
    "MCP__playwright": true,
    "MCP__github": false
  }
}
```

---

## GitHub Integration

### Setup Process

```bash
/install GitHub
```

**Steps:**
1. Install Claude Code GitHub App
2. Add API key
3. Auto-generates workflow files

### GitHub Actions Workflow

```mermaid
graph TD
    A["PR Created"] -->|Trigger| B["@Claude Mentioned"]
    A -->|or| C["Automatic Review"]
    
    B --> D["Claude Code Runs"]
    C --> D
    
    D --> E{"Task Type"}
    
    E -->|Issue Fix| F["Code Generation"]
    E -->|Review| G["Analysis"]
    E -->|Test| H["Validation"]
    
    F --> I["Create Commit"]
    G --> I
    H --> I
    
    I --> J["Push Changes"]
    J --> K["Update PR"]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e8f5e9
    style K fill:#c8e6c9
```

### Workflow File Example

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Claude Code Review
        uses: claudeai/claude-code@v1
        with:
          api-key: ${{ secrets.CLAUDE_API_KEY }}
          instructions: |
            Review this PR for:
            - Code quality issues
            - Security vulnerabilities
            - Performance problems
          mcp-servers:
            - playwright
            - github
```

---

## Hooks System

### What Are Hooks?

```mermaid
graph LR
    A["Tool Request"] --> B{"Pre-Tool<br/>Hook"}
    B -->|Block| C["Stop Execution"]
    B -->|Allow| D["Execute Tool"]
    D --> E["Post-Tool<br/>Hook"]
    E --> F["Log/Verify"]
    E --> G["Feedback"]
    
    style C fill:#2d1212,stroke:#ef4444,color:#e2e8f0
    style D fill:#0d2718,stroke:#00a67e,color:#e2e8f0
```

### Hook Types

| Hook Type | Executes | Can Block? | Use Case |
|-----------|----------|-----------|----------|
| **Pre-Tool** | Before execution | ✅ Yes | Restrict file access |
| **Post-Tool** | After execution | ❌ No | Run tests, format code |

### Configuration

```json
// .clod/settings.local.json
{
  "hooks": {
    "preToolUse": {
      "matcher": "read|grep",
      "command": "node ./hooks/read_hook.js"
    },
    "postToolUse": {
      "matcher": "edit",
      "command": "npm run format"
    }
  }
}
```

### Hook Input Format

Hooks receive JSON data via stdin:

```json
{
  "sessionId": "session-123",
  "toolName": "read",
  "toolInput": {
    "path": "/path/to/file.ts"
  }
}
```

### Exit Codes

| Code | Meaning | Hook Type |
|------|---------|-----------|
| `0` | Allow/Success | Pre & Post |
| `2` | Block | Pre only |

---

## Advanced Hook Patterns

### Pattern 1: Block Sensitive Files

```javascript
// hooks/read_hook.js
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

let data = '';

rl.on('line', (line) => {
  data += line;
});

rl.on('close', () => {
  try {
    const input = JSON.parse(data);
    const filePath = input.toolInput.path || '';
    
    // Block .env files
    if (filePath.includes('.env')) {
      console.error('❌ Access denied: .env files are protected');
      process.exit(2);
    }
    
    // Block secrets
    if (filePath.includes('secret') || filePath.includes('private')) {
      console.error('❌ Access denied: Secret files cannot be read');
      process.exit(2);
    }
    
    process.exit(0); // Allow
  } catch (error) {
    console.error('Hook error:', error.message);
    process.exit(0);
  }
});
```

### Pattern 2: TypeScript Type Checking

```javascript
// hooks/typescript_checker.js
const { execSync } = require('child_process');

// Post-tool hook: Run type checking after edits
try {
  const result = execSync('tsc --no-emit', {
    encoding: 'utf8',
    stdio: 'pipe'
  });
  
  console.log('✅ TypeScript check passed');
  process.exit(0);
} catch (error) {
  console.error('❌ Type errors detected:');
  console.error(error.stdout || error.message);
  process.exit(0); // Don't block, just report
}
```

### Pattern 3: Code Duplication Detection

```mermaid
sequenceDiagram
    participant Claude as Claude Code<br/>Main Instance
    participant Hook as Post-Tool Hook
    participant Secondary as Secondary Claude<br/>Instance
    participant Files

    Claude->>Files: Create new function
    Files-->>Hook: File written
    Hook->>Secondary: Analyze file at queries/
    Secondary->>Files: Review existing functions
    Files-->>Secondary: List all queries
    Secondary->>Secondary: Check for duplicates
    
    alt Duplicate Found
        Secondary-->>Hook: "Duplicate detected: use existing query_x"
        Hook->>Claude: Block + feedback
        Claude->>Claude: Reuse existing function
    else No Duplicates
        Secondary-->>Hook: "Unique - OK to proceed"
        Hook-->>Claude: Allow
    end
```

**Implementation:**

```javascript
// hooks/dedup_hook.js
const { query } = require('../claude-sdk');
const { readdir, readFile } = require('fs').promises;

async function checkDuplicates(changedFile) {
  // Get all existing queries
  const queries = await readdir('./src/queries');
  const existing = await Promise.all(
    queries.map(f => readFile(`./src/queries/${f}`, 'utf8'))
  );
  
  // Launch secondary Claude instance
  const analysis = await query(
   `Compare this new query against existing ones:\n\nNew:\n${changedFile}\n\nExisting:\n${existing.join('\n---\n')}\n\nAre there duplicates?`,
    { allowTools: ['read'] }
  );
  
  if (analysis.includes('duplicate')) {
    console.error('Duplicate detected. Reuse the existing function.');
    process.exit(2);
  }
  
  process.exit(0);
}

// Listen for stdin and execute
checkDuplicates(process.argv[2]);
```

---

## Claude Code SDK

### Overview

The Claude Code SDK provides programmatic access to Claude Code capabilities:

```mermaid
graph TB
    A["Claude Code SDK"] -->|TypeScript| B["ts-sdk"]
    A -->|Python| C["py-sdk"]
    A -->|CLI| D["command-line"]
    
    B --> E["Integration<br/>Pipelines"]
    C --> E
    D --> E
    
    E -->|Used in| F["Custom Scripts"]
    E -->|Used in| G["Hooks"]
    E -->|Used in| H["Automation"]
    
```

### TypeScript Example

```typescript
import { query } from '@claude/code-sdk';

// Read-only query (default)
const result = await query(
  'List all functions in src/api'
);

// Query with write permissions
const codeGen = await query(
  'Generate unit tests for src/auth.ts',
  {
    allowTools: ['read', 'edit', 'run'],
    cwd: './project',
    systemPrompt: 'You are an expert test writer.'
  }
);

// Access conversation
console.log(codeGen.conversation);
console.log(codeGen.finalMessage);
```

### Python Example

```python
from claude_code import query

# Simple read-only query
result = query("What testing frameworks are used?")

# Query with context
with_context = query(
    "Refactor the database layer for performance",
    allowTools=["read", "edit", "run"],
    cwd="./backend",
    context_files=[
        "src/database/schema.ts",
        "src/database/queries.ts"
    ]
)

print(with_context.final_message)
```

### Permission Model

```json
// Default: Read-only
{
  "allowTools": ["read", "grep"]
}

// With writes
{
  "allowTools": ["read", "grep", "edit", "run"]
}

// Custom permissions
{
  "allowTools": ["read"],
  "blockTools": ["run", "bash"],
  "restrictedPaths": [".env", "secrets/"]
}
```

### Use Cases

```mermaid
graph LR
    A["Custom Scripts"] --> B["SDK"]
    C["CI/CD Pipelines"] --> B
    D["Automated Testing"] --> B
    E["Code Generation"] --> B
    
    B --> F["Enhanced<br/>Workflows"]
    B --> G["Integrated<br/>Tools"]
    B --> H["Automated<br/>Tasks"]
    
    style F fill:#0d2718,stroke:#00a67e,color:#e2e8f0
```

---

## Complete Workflow Example

### Scenario: Add Feature with Validation

```mermaid
graph TD
    A["Developer Request<br/>Add user authentication"] --> B["Plan Mode<br/>Shift+Tab x2"]
    B --> C["Claude researches<br/>codebase"]
    C --> D["Create implementation<br/>plan"]
    D --> E["Execute changes"]
    
    E --> F["Pre-Hook<br/>Block .env access"]
    F --> G{"Allowed?"}
    G -->|Yes| H["Edit files"]
    G -->|No| I["Request redirect"]
    
    H --> J["Post-Hook<br/>Run TypeScript check"]
    J --> K{"Type Errors?"}
    K -->|Yes| L["Highlight errors"]
    L --> E
    K -->|No| M["Format code"]
    
    M --> N["Run tests"]
    N --> O["Git commit"]
    O --> P["Complete"]
    
    style P fill:#0d2718,stroke:#00a67e,color:#e2e8f0
```

---

## Best Practices

### ✅ Do

- Use `/init` at project start
- Include critical files in Claude.md
- Enable hooks for type checking
- Use Plan Mode for complex tasks
- Screenshot UI elements for changes
- Leverage MCP servers for external tools

### ❌ Don't

- Overload context with irrelevant files
- Store secrets in Claude.md
- Skip hook setup in team projects
- Use Post-Tool hooks to block operations
- Mix multiple unrelated tasks in one session

---

## Related Resources

- [MCP Integration Guide](05_MCP.md)
- [GitHub Actions Setup](https://github.com/docs/actions)
- [Claude API Documentation](04_Building-with-the-Claude-API.md)
- [Custom Commands Reference](#custom-commands)
