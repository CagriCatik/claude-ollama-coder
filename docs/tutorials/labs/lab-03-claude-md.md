# Lab 03 — CLAUDE.md

**Time:** 20 min · **Module:** [02 Project Context](../02-project-context/README.md)

## Steps
1. In the `log-summarizer` project run `/init`.
2. Open `CLAUDE.md`. Check: overview, commands, architecture.
3. Add a **Rules** section yourself:
   ```markdown
   ## Rules
   - Standard library only for parsing; ask before adding dependencies.
   - Every new feature needs a pytest test.
   - Type hints on all public functions.
   ```
4. Start a **new session** and ask: *"What is this project and how do I run the tests?"* — notice Claude answers without searching.
5. Ask Claude to *"remember that I prefer short commit messages"*. Find out where it stored that (hint: probably not in the repo).
6. Ask it to store a *team* decision in the project instead: *"Add to CLAUDE.md that timestamps are always ISO 8601 UTC."*

## ✅ Done when
- [ ] `CLAUDE.md` exists with your Rules section
- [ ] A fresh session answers project questions instantly
- [ ] You know the difference between private memory and project instructions

Compare with [`examples/starter-project/CLAUDE.md`](https://github.com/CagriCatik/claude-ollama-coder/tree/main/examples/starter-project/CLAUDE.md).
