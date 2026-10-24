# Lab 06 — Subagent

**Time:** 20 min · **Module:** [03 Extending Claude](../03-extending-claude/02-subagents.md)

## Steps
1. Run `/context` and note the current usage.
2. Ask Claude:
   ```text
   Create a project subagent "test-gap-finder" (read-only tools, sonnet model)
   that reads src/ and tests/ and lists functions without test coverage,
   with a suggested test name for each.
   ```
3. Start a new session if it isn't picked up, then: *"Use test-gap-finder."*
4. Click the running agent to watch its tool calls.
5. Run `/context` again — compare with step 1. The subagent's file reads did **not** land in your main context.
6. Ask Claude to write the missing tests based on the report.

## ✅ Done when
- [ ] `.claude/agents/test-gap-finder.md` exists
- [ ] You got a report and your main context stayed small
