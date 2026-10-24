# Lab 09 — Learn a Topic with Collect → Understand → Own

**Time:** 60–90 min · **Module:** [06 Learning with AI](../06-learning-with-ai/README.md)

Pick a topic you actually need. Suggestions: *harness vs. loop engineering for agents*, *MCP security*, *evaluation of LLM test agents*.

## Part A — Collect (20 min)
1. Fill in [`research-brief.md`](https://github.com/CagriCatik/claude-ollama-coder/tree/main/examples/learning-archive/templates/research-brief.md) with your goal, depth, background and what counts as a good source.
2. Ask Claude to turn it into a deep-research prompt. **Cut at least one part** that over-prompts.
3. Run deep research in your research notebook (e.g. NotebookLM). Delete failed sources.
4. Export the source list to Markdown and ask Claude to audit it with the [audit prompt](../06-learning-with-ai/02-collect.md#audit-prompt).
5. Build a **new** notebook from the kept sources.

## Part B — Understand (25 min)
1. Ask Claude for questions based on your goal. Compress them to **at most 5**.
2. Ask the notebook each question, one at a time.
3. Generate **one** notebook studio output (table or deck) **from your answers**, not from the whole library.
4. Ask Claude to reshape your hardest answer into an interactive page around one concrete task of yours.

## Part C — Own (20 min)
1. Export your questions to `questions.md` and put them in a folder together with the artifact(s) you want to keep.
2. Give Claude folder access and use the "job, not structure" prompt from [Own](../06-learning-with-ai/04-own.md). Approve or adjust its plan, then let it build.
3. Compare the result with [`examples/learning-archive/`](https://github.com/CagriCatik/claude-ollama-coder/tree/main/examples/learning-archive/).
4. In a **new** chat, ask: *"What did I learn about <topic>?"*

## ✅ Done when
- [ ] Your audit removed or flagged at least one source you wouldn't have caught yourself
- [ ] You have ≤ 5 focused questions with grounded answers
- [ ] One reshaped artifact exists that's specific to your problem
- [ ] A fresh chat can tell you what you learned, show your question path, and link to the notebook

## Stretch
Turn the filing rules into a skill (`/file-session`) using [Module 03](../03-extending-claude/01-skills.md), then archive a second session with it.
