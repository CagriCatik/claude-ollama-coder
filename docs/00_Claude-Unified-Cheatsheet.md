# Claude AI – Complete Unified Cheatsheet

Master reference for using Claude effectively. Covers prompts, API, tool use, MCP, agents, and best practices.

---

## 🚀 Quick Start (60 Seconds)

### Choose Your Model

```
✅ claude-3-5-sonnet       → 90% of use cases (fast, cheap, smart)
✅ claude-3-opus           → Complex reasoning, analysis jobs
✅ claude-3-haiku          → Real-time, simple tasks, testing
```

### Your First Prompt

```
You: Build me a Python function that:
     - Validates JSON files against a schema
     - Returns errors with file paths
     - Handles file not found gracefully

Claude: [Complete, tested code]

You: [Follow-ups] Add retry logic / Show tests / etc.
```

### Keep It Simple

```python
from anthropic import Anthropic
client = Anthropic()

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Your question"}]
)
print(response.content[0].text)
```

---

## ✍️ Prompt Structure (The Template)

Use this structure. Adapt as needed.

```
Goal:
  What you need. Why. Success criteria.

Context:
  Relevant code, data, or examples.

Constraints:
  - Format: <JSON|Markdown|XML|Code>
  - Length: <word/line limit>
  - Tone: <professional|casual>
  - Safety: Cite sources. Ask if unclear.

Examples:
  Input:  [example input]
  Output: [example output]

Output format:
  [exact template to follow]
```

**Secret:** Include Goal + Example + Output Format. Always.

---

## 🎯 Prompt Techniques (Pick 1-3)

| Technique | Example | Use For |
|-----------|---------|---------|
| **Role** | "You are a senior architect" | Expertise + perspective |
| **Step-by-step** | "Think through it step by step" | Logic, debugging |
| **Examples** | Show 2-3 input→output pairs | Consistent output |
| **Constraints** | "Under 100 words, ES6 only" | Specific requirements |
| **Chain-of-thought** | "Show reasoning before answering" | Complex analysis |
| **Structured** | "Return JSON with X, Y, Z keys" | Machine-readable |

---

## 🔧 Core API (Python)

### Single Request

```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,               # Set this! (50-4096)
    temperature=0.3,               # 0=predictable, 1=creative
    system="You are a ...",        # Optional role
    messages=[
        {"role": "user", "content": "Question"},
    ]
)

print(response.content[0].text)
print(response.usage.output_tokens)
print(response.stop_reason)        # "end_turn" or "max_tokens"
```

### Multi-Turn Conversation

```python
messages = []

# Turn 1
messages.append({"role": "user", "content": "Explain promises"})
r1 = client.messages.create(model="claude-3-5-sonnet-20241022", messages=messages)
messages.append({"role": "assistant", "content": r1.content[0].text})

# Turn 2 - Claude remembers!
messages.append({"role": "user", "content": "Show me error handling"})
r2 = client.messages.create(model="claude-3-5-sonnet-20241022", messages=messages)
```

### Streaming (Real-Time)

```python
with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)  # Real-time output
```

---

## 🔑 Tool Use (Claude's Superpowers)

### Define Tools

```python
tools = [
    {
        "name": "fetch_data",
        "description": "Get data from database",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer"}
            },
            "required": ["query"]
        }
    }
]
```

### Use Tool Loop

```python
messages = [{"role": "user", "content": "Get Q3 sales data"}]

while True:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        tools=tools,
        messages=messages
    )
    
    if response.stop_reason == "end_turn":
        print(response.content[0].text)  # Final answer
        break
    
    # Process tool calls
    for block in response.content:
        if block.type == "tool_use":
            # Call your function
            result = fetch_data(block.input["query"], block.input.get("limit"))
            
            # Tell Claude the result
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                }]
            })
```

---

## 🌐 Model Context Protocol (MCP)

### What Is MCP?

Protocol for Claude to access external tools/resources safely.

| Component | Purpose |
|-----------|---------|
| **MCP Server** | Provides tools (database, filesystem, APIs) |
| **Tool** | Function Claude can call (fetch_data, analyze, etc.) |
| **Resource** | Data Claude can read (file content, DB records) |
| **Prompt** | Dynamic instructions Claude receives |

### Tool Composition Example

```python
# Chain multiple MCP tools
tools = [
    {"name": "read_file", ...},
    {"name": "analyze_data", ...},
    {"name": "generate_report", ...}
]

# Claude orchestrates them automatically
```

---

## 🤖 Agents & Skills

### Custom Skills

Specialized capabilities for specific tasks.

```python
class DataSkill:
    def analyze(self, data):
        """Analyze data and return insights"""
        return {"trends": [...], "anomalies": [...]}

class ReportSkill:
    def generate(self, analysis):
        """Generate report from analysis"""
        return report_markdown

# Register with agent
agent.add_skill("analysis", DataSkill())
agent.add_skill("reporting", ReportSkill())

# Agent uses automatically
agent.run("Analyze Q3 sales and generate report")
```

### Subagents (Parallel Execution)

Delegate complex tasks to specialized agents.

```python
# Create specialist subagents
data_agent = SubagentPool.get("DataSpecialist")
analysis_agent = SubagentPool.get("Analyst")  
viz_agent = SubagentPool.get("Visualizer")

# Run in parallel
results = await Orchestrator().run_parallel({
    "load": {"agent": data_agent, "task": "Load Q3 data"},
    "analyze": {"agent": analysis_agent, "task": "Analyze trends"},
    "visualize": {"agent": viz_agent, "task": "Create charts"}
})
```

---

## 📊 Usage Patterns

### Pattern: Code Review

```
You: Review this code for security + performance:
     [paste code]

Claude: ✓ Good practices
        ✗ Issues
        💡 Improvements
```

### Pattern: Learning

```
You: Explain TypeScript generics like I'm learning

Claude: [explanation + examples]

You: Show me a real-world use case

Claude: [practical scenario]
```

### Pattern: Debugging

```
You: Error: "Cannot read property 'map' of undefined"
     Code: [paste]

Claude: Issue: ...
        Solution: [fixed code]

You: Why does that happen?

Claude: [explains mechanism]
```

### Pattern: Analysis

```
You: Analyze this engagement data: [data]

Claude: Findings:
        - Trend 1: ...
        - Trend 2: ...
        - Anomaly: ...

You: What caused Monday dip?

Claude: [hypothesis]
```

---

## ✅ Best Practices

✅ **DO:**

- Use Sonnet by default
- Set explicit `max_tokens`
- Use `temperature=0.3` for analysis
- Include examples (few-shot)
- Follow up with questions
- Test with Haiku first
- Use tool use for logic ops
- Implement retry with backoff

❌ **DON'T:**

- Use Opus for simple tasks
- Leave `max_tokens` open
- Use `temperature=1.0` for facts
- Ignore `stop_reason`
- Process sensitive data unsecured
- Assume response format
- Create infinite loops
- Retry immediately on rate limit

---

## 🚨 Error Handling

### Retry with Backoff

```python
import time
from anthropic import RateLimitError

for attempt in range(3):
    try:
        response = client.messages.create(...)
        return response
    except RateLimitError:
        wait = 2 ** attempt  # 1, 2, 4 seconds
        time.sleep(wait)
```

### Handle All Stop Reasons

```python
if response.stop_reason == "end_turn":
    # Normal completion ✓
    print(response.content[0].text)
elif response.stop_reason == "max_tokens":
    # Incomplete response - increase max_tokens ⚠️
    print("Response cut off - need longer response")
elif response.stop_reason == "tool_use":
    # Process tool calls 🔧
    for block in response.content:
        if block.type == "tool_use":
            # Handle tool call
```

---

## 💰 Cost Optimization

### Token Math

- 1 token ≈ 4 characters
- 750 words ≈ 1,000 tokens
- Your budget = tokens × price

### Pricing (per 1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| Haiku | $0.80 | $4.00 |
| Sonnet | $3.00 | $15.00 |
| Opus | $15.00 | $75.00 |

### Save Money

1. Use Sonnet (best value)
2. Set reasonable `max_tokens`
3. Cache system prompts
4. Use Haiku for testing
5. Batch requests

---

## 📝 Output Formats (Copy & Paste)

### JSON

```json
{
  "summary": "Brief overview",
  "key_points": ["Point 1", "Point 2"],
  "recommendations": ["Action 1"],
  "confidence": 0.95
}
```

### Markdown

```markdown
## Summary
Overview here

## Key Findings
- Finding 1: Details
- Finding 2: Details

## Actions
1. Action 1
2. Action 2
```

### XML

```xml
<response>
  <summary>...</summary>
  <findings>
    <finding>...</finding>
  </findings>
  <actions>...</actions>
</response>
```

---

## 🎓 Advanced Patterns

### Decomposition

Break complex tasks into parallel subtasks.

### Chaining

Sequential tasks where each builds on previous.

### Branching

Explore multiple approaches, select best.

### Feedback Loops

Claude reviews own output, improves iteratively.

### RAG (Retrieval-Augmented Generation)

Combine Claude with vector databases for custom knowledge.

---

## 📚 Task Reference

| What You Want | Ask | Model |
|---------------|-----|-------|
| General help | "Help me with..." | Sonnet |
| Code review | "Review this code: [paste]" | Sonnet |
| Learning | "Explain X like I'm..." | Sonnet |
| Analysis | "Analyze this: [data]" | Opus |
| Quick test | "Simple test of..." | Haiku |
| Writing | "Write me a..." | Sonnet |
| Debugging | "Fix this error: [paste]" | Sonnet |
| Design | "Design a system for..." | Opus |
| Real-time | "Real-time analysis of..." | Haiku |

---

## 🔗 Pro Tips by Scenario

### Stuck on Problem?

```
You: I'm stuck. Walk me through how YOU would solve this.

Claude: [Thinks through step-by-step]

Result: Often reveals what you missed!
```

### Need Options?

```
You: Show me 3 approaches to this problem

Claude:
1. Approach A: [code + explanation]
2. Approach B: [code + explanation]
3. Approach C: [code + explanation]
```

### Get Feedback?

```
You: Pretend you're a code reviewer. Review my code.

Claude: ✓ Good practices
        ✗ Issues
        💡 Improvements
```

### Build Iteratively?

```
Step 1: Get basic version
Step 2: Add feature X
Step 3: Add security
Step 4: Add tests
Step 5: Optimize
```

---

## ⚡ Command Shortcuts

```bash
# Install
pip install anthropic

# Set key
export ANTHROPIC_API_KEY="sk-ant-..."

# Test
python -c "from anthropic import Anthropic; c = Anthropic(); print(c.messages.create(model='claude-3-5-sonnet-20241022', max_tokens=100, messages=[{'role': 'user', 'content': 'test'}]).content[0].text)"
```

---

## 🔗 Learn More

- [Claude Code in Action](01_Claude-Code-in-Action.md) — Real workflows
- [Claude 101](02_Claude-101.md) — API fundamentals  
- [AI Fluency Framework](03_AI-Fluency-Framework-Foundations.md) — Mental models
- [Building with APIs](04_Building-with-the-Claude-API.md) — Tool use
- [Model Context Protocol](05_MCP.md) — External integration
- [Advanced MCP](06_MCP-Advanded.md) — Production patterns
- [Agent Skills](07_Agent-Skills.md) — Custom capabilities
- [Subagents](08_Subagents.md) — Orchestration

---

**Last Updated:** March 2026 | **Current Models:** claude-3-5-sonnet, claude-3-opus, claude-3-haiku
