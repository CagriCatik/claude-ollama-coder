# Lab 04 — settings.json

**Time:** 20 min · **Module:** [02 Project Context](../02-project-context/03-settings-json.md)

## Steps
1. Create a fake secret: `echo "API_KEY=do-not-read" > .env` and add `.env` to `.gitignore`.
2. Ask Claude:
   ```text
   Create .claude/settings.json so that:
   - running pytest and the CLI never asks for permission
   - installing packages always asks
   - .env can never be read
   ```
3. Inspect the file and compare with [the example](https://github.com/CagriCatik/claude-ollama-coder/tree/main/examples/starter-project/.claude/settings.json).
4. Test each rule:
   - *"Run the tests"* → no prompt
   - *"Install rich"* → you get asked (deny it)
   - *"What's in .env?"* → blocked
5. Add your own spinner verbs for fun.

## ✅ Done when
- [ ] All three behaviors verified
- [ ] You can explain the difference between `settings.json` and `settings.local.json`
