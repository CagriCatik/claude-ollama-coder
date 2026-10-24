# Reference Specification: Progressive Disclosure Deep Dive

This document demonstrates the **Progressive Disclosure** pattern recommended by Anthropic for Claude Code agent skills.

## Why Progressive Disclosure?

1. **Context Window Preservation:**
   When Claude Code discovers available skills at session launch, it reads *only* each skill's `name` and `description` frontmatter. This consumes minimal context window budget (~50–100 tokens per skill) regardless of how many skills are registered.

2. **Conditional Activation:**
   When the user's intent or files match a skill's description, Claude loads the primary `SKILL.md` body into context.

3. **On-Demand Deep Dives:**
   If the task involves rare edge cases, extensive API schemas, or multi-page documentation, Claude reads supplementary files in `references/` only when actually needed during execution.

---

## Example Reference Document Structure

```text
skills/my-domain-skill/
├── SKILL.md                 # Primary instructions & decision rules (< 200 lines)
├── references/              # Loaded on-demand
│   ├── api-schemas.md       # Full OpenAPI/JSON schemas
│   └── error-catalog.md     # Error codes and remediation steps
└── scripts/                 # Executed deterministically
    └── verify_schema.py     # Fast validation script
```

---

## Best Practices for Reference Files

- Keep them focused on specific sub-topics or reference tables.
- Use explicit filenames indicating their purpose (e.g. `error_catalog.md`, `cli_cheatsheet.md`).
- Cross-reference them from `SKILL.md` using relative paths:
  ```markdown
  For complete error code mappings, see `references/error-catalog.md`.
  ```
