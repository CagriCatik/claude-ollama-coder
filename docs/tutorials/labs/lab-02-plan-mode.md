# Lab 02 — Plan Mode

**Time:** 30 min · **Module:** [01 Core Concepts](../01-core-concepts/README.md)

## Steps
1. Switch mode to **Plan**.
2. Send:
   ```text
   I want a Python CLI "logsum" that reads a log file and writes a Markdown
   summary: counts per level, top 5 error messages, first/last timestamp,
   errors per component.

   Stack: Python 3.11, standard library only for parsing, pytest for tests,
   uv or pip for packaging. Keep the layout small: src/logsum/, tests/.

   Before planning, ask me any questions you need.
   ```
3. Answer Claude's questions. Note at least one question you hadn't thought of.
4. Read the plan. Request one change (e.g. *"add a --json output option"*).
5. Accept the plan (switches to Auto mode) and let it build.
6. Run it on `logs/sample.log`.

## ✅ Done when
- [ ] `logsum logs/sample.log` (or `python -m logsum …`) prints/writes a summary
- [ ] Tests exist and pass
- [ ] You changed the plan at least once before accepting

## Stretch
Re-run the same build request with effort **low** in a throwaway folder. Compare speed and quality.
