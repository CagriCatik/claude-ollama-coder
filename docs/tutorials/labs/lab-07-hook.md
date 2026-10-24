# Lab 07 — Hooks

**Time:** 25 min · **Module:** [03 Extending Claude](../03-extending-claude/04-hooks.md)

## Part A — "Done" notification
1. Copy [`examples/starter-project/.claude/hooks/notify.sh`](https://github.com/CagriCatik/claude-ollama-coder/tree/main/examples/starter-project/.claude/hooks/notify.sh) (or `notify.ps1` on Windows) into `log-summarizer/.claude/hooks/`.
2. Add a `Stop` hook in `.claude/settings.json` that runs it.
3. Send *"hello"* — you should get a desktop notification when Claude finishes. (Check OS notification permissions if not.)

## Part B — Auto-format on edit
1. Ask Claude: *"Add a PostToolUse hook for Edit|Write that runs `ruff format` on changed Python files."* (Install ruff if needed.)
2. Ask Claude to add a deliberately badly formatted function. Verify it's formatted automatically.

## Part C — Guardrail
1. Copy `block-secrets.sh` from the example and wire it as a `PreToolUse` hook.
2. Ask *"show me .env"* — the hook should block it even if `settings.json` didn't.

## ✅ Done when
- [ ] All three hooks fire as expected
- [ ] You can explain why a hook is more reliable than a rule in `CLAUDE.md`
