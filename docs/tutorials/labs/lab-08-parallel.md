# Lab 08 — Parallel Work, Context & Safety Nets

**Time:** 30 min · **Module:** [04 Daily Workflow](../04-daily-workflow/README.md)

## Part A — Two sessions, two worktrees
1. Commit everything on `main`.
2. Start **Session A** with worktrees enabled: *"Add an --html output option."*
3. Start **Session B** with worktrees enabled: *"Add a --since <timestamp> filter."*
4. Split panes and watch both.
5. Merge both branches. Resolve conflicts if any (ask Claude to help).

## Part B — Context hygiene
1. In a long session, run `/context`.
2. Run `/compact`, then `/context` again.
3. Run `/clear`. Note the baseline token count that remains.

## Part C — Rewind
1. Ask Claude to *"rewrite the parser using regex only"*.
2. Don't like it? `/rewind` → pick the prompt before → restore **code and conversation**.

## Part D — Review
Run `/code-review` on the merged result. Fix one finding.

## ✅ Done when
- [ ] Both features merged on `main`
- [ ] You used `/compact`, `/clear`, `/rewind` and `/code-review` at least once
