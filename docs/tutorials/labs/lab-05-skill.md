# Lab 05 — Your First Skill

**Time:** 20 min · **Module:** [03 Extending Claude](../03-extending-claude/01-skills.md)

## Steps
1. Ask Claude:
   ```text
   Make a global skill called "changelog" that reads git log since the last
   tag (or the last 20 commits if there's no tag) and writes a CHANGELOG
   entry grouped into Added / Changed / Fixed. Keep the instructions short.
   ```
2. Find it in `~/.claude/skills/changelog/SKILL.md` and read it. Improve the `description` so Claude knows when to use it.
3. Run `/changelog` in `log-summarizer`.
4. Open a **different** project and confirm `/changelog` is available there too.
5. Now move it into `log-summarizer/.claude/skills/`. Confirm it disappears from the other project.

## ✅ Done when
- [ ] `/changelog` produces a sensible entry
- [ ] You've seen global vs. project scope in action

## Stretch
Add a `scripts/` file to the skill (e.g. a script that finds the last tag) and reference it from `SKILL.md`.
