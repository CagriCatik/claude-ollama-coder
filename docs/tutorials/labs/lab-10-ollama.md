# Lab 10 — Ollama & Local Models

**Time:** 20 min · **Module:** [07 Running with Ollama](../07-running-with-ollama/README.md)

## Steps

1. **Verify Ollama & inspect local models on your Mac:**
   ```bash
   ollama --version
   ollama list
   ```

2. **Launch Claude Code and test `--config`:**
   Configure or switch your active model:
   ```bash
   ollama launch claude --config
   ```
   Choose a model with tool-calling capabilities (e.g. `qwen2.5-coder:8b` locally, or a cloud model like `gpt-oss:20b-cloud` / `glm-4.7:cloud`).

3. **Check the connection:**
   Inside Claude Code, run:
   ```text
   /status
   ```
   Confirm that the active model name and the Base URL point to Ollama (`http://localhost:11434` or `https://ollama.com`).

4. **Test the Plan Mode + ASCII Wireframe Prompt:**
   Switch to **Plan Mode** (`Shift + Tab`) and test the local model prompt pattern:
   ```text
   Design an email verification component. Before generating any HTML or CSS, create a terminal ASCII wireframe in your plan showing the layout, header, logo, call-to-action button, and footer.
   ```
   Inspect the ASCII layout before approving code generation.

5. **Test a headless non-interactive command:**
   Exit the session (`/exit` or `Ctrl+C`), then run a one-off headless prompt:
   ```bash
   ollama launch claude --model gpt-oss:20b-cloud --yes -- -p "Count how many markdown files exist in this repo."
   ```

6. **Test an in-session `/loop`:**
   Start an interactive session again and schedule a repeating prompt:
   ```text
   /loop 5m Check if git status has changed and print a one-line summary
   ```

---

## ✅ Done when

- [ ] `ollama list` and `/status` verify Claude Code is talking to Ollama
- [ ] You switched or selected models using `ollama launch claude --config`
- [ ] You generated and inspected an ASCII wireframe in Plan Mode before generating code
- [ ] You ran at least one headless command using `--yes -- -p`
- [ ] You scheduled an in-session loop using `/loop`

---

## Reflect

- Did breaking the prompt into a single component + ASCII wireframe improve the local model's output quality?
- How did the response speed and VRAM usage on your Mac compare between local 8B models and cloud open models?
