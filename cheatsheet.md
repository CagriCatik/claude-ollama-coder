# Claude AI – Prompt‑Engineering Cheat Sheet

A quick, practical reference you can keep open while you work with Claude. It focuses on the most effective patterns for reliable, safe, and structured output.

---

## 📌 Core Prompt Structure (the "Spec Document")

```
Goal:
    <What you need, why it matters, success criteria>

Context:
    <Relevant snippet, code, or data>

Constraints:
    - Format: <JSON|Markdown|XML|...>
    - Length: ≤ <n> words/lines
    - Tone: <professional|concise|friendly>
    - Safety: cite sources, never guess, ask if unclear

Examples:
    Input:  <example input>
    Output: <example output>

Output format:
    <precise template – e.g. JSON schema, markdown headings, XML tags>
```

*Use **all** sections that matter; omit any you don’t need.*

---

## ⚡ High‑Impact Techniques (pick 2‑3 per prompt)

| Technique | When to use | Prompt snippet |
|-----------|-------------|----------------|
| **Role prompting** | Need domain expertise or perspective | `You are a senior software architect reviewing a design.` |
| **Step‑by‑step reasoning** | Logical/diagnostic tasks | `Think through the problem step by step before answering.` |
| **Few‑shot examples** | Want consistent output style | Provide 1–3 input‑output pairs under **Examples** |
| **XML / tag‑based structuring** | Complex nested instructions | `<task>…</task><data>…</data><output_format>json</output_format>` |
| **Contract‑style system prompt** | Strict safety limits | `You must: - cite sources - never guess - ask for clarification if missing info.` |
| **Force‑structured output** | Machine‑readable results | `Return JSON with keys "summary", "risks", "recommendations".` |

**Rule of thumb:** always include Goal, at least one Example, and a concrete Output format.

---

## 📐 Common Output Schemas

### JSON Summary (most reusable)
```json
{
  "summary": "<short paragraph>",
  "key_points": ["<point>", "<point>"],
  "risks": ["<risk>"],
  "recommendations": ["<action>"]
}
```

### Markdown Report

```markdown
## Overview
<2‑3 sentence overview>

### Key Decisions
- …

### Trade‑offs
- …

### Risks & Mitigations
- …

### Action Items
- …
```

### XML Wrapper (for strict parsers)
```xml
<response>
  <summary>…</summary>
  <points><point>…</point></points>
  <risks><risk>…</risk></risks>
  <recommendations><rec>…</rec></recommendations>
</response>
```

---

## 🛡️ Safety Guardrails (always put in **Constraints**)
1. **Cite sources** – `You must cite at least one source for any factual claim.`
2. **Ask before guessing** – `If you lack information, ask the user for clarification.`
3. **No speculative advice** – `Never provide medical, legal, or financial advice unless explicitly authorized.`

---

## ✅ Quick‑Copy Template (paste & fill)
```
Goal:
    <single‑sentence task>

Context:
    <relevant snippet>

Constraints:
    - Format: <JSON|Markdown|...>
    - Length: ≤ <n> words
    - Tone: <professional|concise>
    - Safety: cite sources, never guess, ask if missing

Examples:
    Input:  <example input>
    Output: <example output>

Output format:
    <exact template>
```

Keep this sheet handy and adjust as needed. Happy prompting!
