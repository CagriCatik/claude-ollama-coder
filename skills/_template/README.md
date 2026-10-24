# Agent Skill Template & Authoring Quickstart

This directory provides the canonical template and validation tools for creating conforming Claude Code and Anthropic Agent Skills (`agentskills.io` specification).

---

## Quickstart: Creating a New Skill

### Step 1: Copy the Template
Copy `_template` to a new directory under `skills/` named with lowercase alphanumeric characters and single hyphens:

```bash
cp -r skills/_template skills/my-new-skill
rm -rf skills/my-new-skill/README.md  # Optional
```

### Step 2: Configure YAML Frontmatter
Open `skills/my-new-skill/SKILL.md` and set:
1. `name`: Must match the directory name exactly (`my-new-skill`).
2. `description`: Explain **what** the skill does and **when** Claude should trigger it (`Use when...`). Keep under 1024 characters.
3. `license`: (e.g. `Apache-2.0` or `MIT`).
4. `compatibility`: Environment requirements (e.g. `Python >= 3.10, Claude Code`).

### Step 3: Write Actionable Instructions
In `SKILL.md`:
- **When to Use:** Concrete file extensions, keywords, and triggers.
- **Core Principles:** Direct, imperative guidelines.
- **Code Patterns:** Good vs bad examples.
- **Self-Verification Checklist:** Clear checklist items for Claude to verify before completion.

### Step 4: Validate Conformance
Run the included validator:

```bash
python3 skills/_template/scripts/validate_skill.py skills/my-new-skill
```

---

## Directory Layout

```text
skills/my-new-skill/
├── SKILL.md                 # Required: YAML frontmatter + instructions
├── scripts/                 # Optional: Executable automation scripts
│   └── helper.py
└── references/              # Optional: Deep-dive documentation
    └── spec.md
```
