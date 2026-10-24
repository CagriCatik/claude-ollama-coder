---
name: git-workflow
description: Git best practices and workflow guidelines for AI coding assistants. Use when creating git commits, formatting commit messages, preparing pull requests, creating branches, configuring git worktrees for parallel sessions, resolving merge conflicts, or cleaning up git history.
license: MIT
compatibility: Git 2.25+, Claude Code
metadata:
  author: claude-ollama-coder
  version: "1.0.0"
---

# Git Workflow & Commit Guidelines

Standardized practices for version control, branching, atomic commits, and parallel worktrees with Claude Code.

---

## When to Use This Skill

- **Trigger Scenarios:**
  - When committing code, writing commit messages, or staging files with git.
  - When creating or reviewing pull requests (PR descriptions, changelogs).
  - When establishing branch naming conventions (`feat/`, `fix/`, `refactor/`).
  - When setting up Git Worktrees to isolate concurrent Claude Code sessions.
  - When resolving merge conflicts or rebasing feature branches.

- **When NOT to Use:**
  - Do not use for non-git VCS tools (SVN, Mercurial).
  - Do not use when working solely on CI/CD runner YAML files unless git actions/hooks are involved.

---

## 1. Conventional Commits Standard

Every commit message must follow the Conventional Commits specification:

```text
<type>(<optional scope>): <short description in present tense>

[optional body explaining why the change was made and key tradeoffs]

[optional footer(s), e.g. Co-Authored-By, Fixes #123]
```

### Commit Types
| Type | Purpose | Example |
|---|---|---|
| `feat` | New user-facing feature or API capability | `feat(auth): add OAuth2 refresh token rotation` |
| `fix` | Bug fix | `fix(parser): handle trailing commas in json payloads` |
| `docs` | Documentation only changes | `docs(readme): update quickstart installation steps` |
| `refactor` | Code restructuring without changing external behavior | `refactor(db): extract connection pool into singleton` |
| `test` | Adding missing tests or correcting existing tests | `test(client): add unit tests for retry backoff` |
| `chore` | Maintenance, dependencies, build scripts | `chore(deps): bump pydantic from 2.9 to 2.10` |
| `perf` | Performance improvement | `perf(query): index user_id column on sessions table` |

### Formatting Rules
- **Use imperative, present tense**: "add", not "added" or "adds".
- **Don't capitalize the first letter** after the colon.
- **No trailing period** in the summary line.
- **Explain *why*, not *what*** in the commit body: the git diff already shows *what* changed.

---

## 2. Co-Authored-By Attribution

When Claude Code creates commits on behalf of a user, include clean attribution in the commit trailer:

```text
feat(ollama): add custom modelfile validator

Validate num_ctx minimum threshold (64k) before launching Claude Code session.

Co-Authored-By: Claude Code <noreply@anthropic.com>
```

---

## 3. Atomic & Surgical Commits

- **One logical change per commit**: Do not mix refactoring with new feature additions or bug fixes.
- **Never commit secrets**: Verify `git status` and staged diffs before committing (`.env`, private keys, tokens).
- **Match existing branch naming**:
  - `feat/<short-description>`
  - `fix/<issue-number>-<short-description>`
  - `refactor/<module-name>`

---

## 4. Parallel Sessions with Git Worktrees

Claude Code works best in isolated sessions. When working on two distinct tasks simultaneously, use **Git Worktrees** instead of switching branches in the same working directory:

```bash
# 1. Create a worktree for a new feature branch
git worktree add ../feature-auth -b feat/oauth-login

# 2. Open a separate terminal or Claude Code session in the worktree
cd ../feature-auth
claude -p "Implement OAuth login routes"

# 3. Once feature is merged and done, remove the worktree
cd ../claude-ollama-coder
git worktree remove ../feature-auth
git branch -d feat/oauth-login
```

### Worktree Benefits
- No stash/pop required when switching tasks.
- No risk of uncommitted edits conflicting between parallel Claude sessions.
- Clean isolation of temporary virtual environments and build artifacts.

---

## 5. Pull Request (PR) Summaries

When generating PR descriptions for GitHub or GitLab, use this structured template:

```markdown
## Summary of Changes
- Concise bullet points summarizing key capabilities added or bugs fixed.

## Motivation & Architecture
- Why this approach was chosen over alternatives.
- Tradeoffs or notable design decisions.

## Verification & Testing
- Steps taken to verify correctness (unit tests, manual curl commands, browser preview).
- [ ] Tests passing locally
- [ ] Linting and formatting verified
```

---

## Self-Verification Checklist

Before committing or pushing git changes:
- [ ] Staged diff (`git diff --staged`) inspected line-by-line; no accidental files or debug statements included.
- [ ] No secrets, `.env` files, or API credentials staged.
- [ ] Commit message conforms to `<type>(<scope>): <imperative summary>`.
- [ ] Commit message summary is under 72 characters and lowercase after the colon.
- [ ] Co-Authored-By attribution included when committing on behalf of an agent workflow.
- [ ] Branch name adheres to repository naming conventions (`feat/`, `fix/`, `refactor/`).
