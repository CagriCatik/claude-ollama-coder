# 3. Stage 2 — Understand: Ask, Focus, Reshape

AI explains brilliantly. It can turn a pile of text into a summary, report or deck faster than you can absorb it. So the output itself matters less than **the choices you make around it**.

## The mini loop

```mermaid
flowchart LR
    Ask["❓ Ask<br/>Claude proposes questions<br/>from your goal"] --> Focus["🎯 Focus<br/>you compress them to the few<br/>that deserve attention"]
    Focus --> Answer["📚 Answer<br/>notebook answers each one<br/>grounded in the library"]
    Answer --> Reshape["🔁 Reshape<br/>turn answers into a form<br/>that helps YOU understand"]
    Reshape -.new questions.-> Ask
```

### Ask → Focus
Tell Claude your purpose and goal and let it suggest questions. In the video Claude produced six blocks of questions. Don't copy them blindly. **Compress them into a small "attention zone"** of about five questions that you actually care about.

```text
My goal: <goal>. My background: <background>.
Suggest the questions I should answer to reach this goal, grouped by theme.
```

### Answer
Ask the notebook your questions **one at a time**, so each answer is grounded in your curated library.

## Reshape: pick the right format

```mermaid
flowchart TD
    Q{What do you need?}
    Q -->|Fast overview of dense,<br/>technical material| T[📊 Data table<br/>notebook studio]
    Q -->|A different structure /<br/>new perspective| S[🖼️ Slide deck<br/>notebook studio]
    Q -->|Something specific to MY problem,<br/>many moving parts| C[🧩 Interactive page<br/>built by Claude]
    Q -->|Hard to read long reports<br/>accessibility, 2nd language| G[🕸️ Context graph +<br/>reading hub, built by Claude]
```

| Format | Tool | Best for |
|---|---|---|
| **Data table** | Notebook studio output | Condensing dense technical material without getting overwhelmed |
| **Slide deck** | Notebook studio output | Seeing the same information in another structure |
| **Interactive page** | Claude | Applying concepts to *your* specific problem |
| **Context graph + reading hub** | Claude | Navigating a long report visually: the map shows structure, the hub gives detail |

> 💡 **Generate decks from your *answers*, not the whole library.** If you use the whole library, the notebook decides what matters and you get a generic summary. Your answers already reflect your focus.

## Example: when text answers stop working

Question: *"For one specific task, how does the setup change across prompt, context, harness and loop design?"*

The prompt and context layers are easy to follow in text. The harness and loop layers bring in tools, agents and feedback, and become hard to hold in your head. So ask Claude to reshape the answer into an interactive page:

```mermaid
flowchart TB
    subgraph L1[Prompt layer]
        P1[System prompt] --> P2[Task instructions]
    end
    subgraph L2[Context layer]
        C1[Skill file] --> C2[Retrieved docs]
        C2 --> C3[Memory]
    end
    subgraph L3[Harness layer]
        H1[Tools] --> H2[Error channel]
        H2 --> H3[Agent]
    end
    subgraph L4[Loop layer]
        R1[Run] --> R2[Evaluate] --> R3[Feedback] --> R1
    end
    L1 --> L2 --> L3 --> L4
```

On the page, every box can be clicked to reveal a concrete example: what the skill file contains, or what an error message looks like when it flows back to the agent. Each abstract concept is tied to something concrete.

```text
Here are my answers on <topic>. Reshape them into an interactive page
around MY task: <task>. Show each layer as a workflow; clicking a box
should reveal a concrete example (file contents, message format, etc.).
```

➡️ Next: [Stage 3 — Own](04-own.md)
