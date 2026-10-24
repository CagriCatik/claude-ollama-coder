# Glossary

| Term | Meaning | Lesson |
|---|---|---|
| **ANTHROPIC_BASE_URL** | Environment variable pointing Claude Code to an alternative API endpoint (e.g. Ollama) | [07-1](docs/tutorials/07-running-with-ollama/01-quickstart-and-setup.md) |
| **Artifact** | Something Claude builds that you can view, use and share (page, app, document) | [05-3](docs/tutorials/05-beyond-code/) |
| **Attention zone** | The small set of questions you choose to focus on out of everything AI suggests | [06-3](docs/tutorials/06-learning-with-ai/03-understand.md) |
| **Auto mode** | Default permission mode; asks only for risky actions | [01-4](docs/tutorials/01-core-concepts/04-permission-modes.md) |
| **CLAUDE.md** | Markdown file of standing instructions loaded into every session | [02-1](docs/tutorials/02-project-context/01-claude-md.md) |
| **Client mindset** | Directing AI tools and making the judgments yourself, instead of watching AI learn for you | [06-1](docs/tutorials/06-learning-with-ai/01-client-mindset.md) |
| **Compact** | Summarize the conversation to shrink context (`/compact`) | [04-1](docs/tutorials/04-daily-workflow/01-context-management.md) |
| **Connector** | An app integration in the Claude app, built on MCP | [05-2](docs/tutorials/05-beyond-code/02-connectors.md) |
| **Context window** | Everything Claude currently sees, measured in tokens | [04-1](docs/tutorials/04-daily-workflow/01-context-management.md) |
| **Deep research** | A research-tool mode that gathers and reads many sources for a prompt | [06-2](docs/tutorials/06-learning-with-ai/02-collect.md) |
| **Effort level** | How long Claude thinks and how much it self-checks | [01-3](docs/tutorials/01-core-concepts/03-effort-levels.md) |
| **Harness** | The Claude Code program around the model: runs tools, fires hooks, enforces permissions | [03-4](docs/tutorials/03-extending-claude/04-hooks.md) |
| **Hook** | Shell command the harness runs automatically on an event | [03-4](docs/tutorials/03-extending-claude/04-hooks.md) |
| **/loop** | In-session scheduled prompt runner provided by Ollama integration | [07-3](docs/tutorials/07-running-with-ollama/03-headless-and-automation.md) |
| **MCP** | Model Context Protocol — standard for connecting external tools/data | [03-3](docs/tutorials/03-extending-claude/03-mcp.md) |
| **Memory** | Facts Claude stores for future sessions (private by default) | [02-2](docs/tutorials/02-project-context/02-memory.md) |
| **Mod** | Plugin-shipped customization of the Claude Code UI/harness | [03-5](docs/tutorials/03-extending-claude/05-plugins-and-mods.md) |
| **Model** | The AI "brain": Haiku, Sonnet, Opus, Fable, or Ollama local/cloud models | [01-2](docs/tutorials/01-core-concepts/02-models.md) |
| **num_ctx (64k+)** | Ollama parameter setting context window length (64k+ required for Claude Code) | [07-2](docs/tutorials/07-running-with-ollama/02-selecting-models-and-context.md) |
| **Ollama launch** | One-liner command configuring and launching Claude Code with local or cloud models | [07-1](docs/tutorials/07-running-with-ollama/01-quickstart-and-setup.md) |
| **Permission mode** | How much Claude may do without asking | [01-4](docs/tutorials/01-core-concepts/04-permission-modes.md) |
| **Plan mode** | Read-only mode where Claude writes a plan for approval | [01-5](docs/tutorials/01-core-concepts/05-plan-mode-workflow.md) |
| **Plugin** | Bundle of skills, agents, hooks, MCP config, mods | [03-5](docs/tutorials/03-extending-claude/05-plugins-and-mods.md) |
| **Project (Code)** | A folder Claude works in | [00-3](docs/tutorials/00-getting-started/03-desktop-ui-tour.md) |
| **Project (app)** | Chat workspace with knowledge files and instructions | [05-1](docs/tutorials/05-beyond-code/01-projects-and-memory.md) |
| **Research notebook** | A source-grounded tool (e.g. Gemini NotebookLM) that holds your library and answers from it | [06-2](docs/tutorials/06-learning-with-ai/02-collect.md) |
| **Rewind** | Restore conversation and/or code to a checkpoint | [04-2](docs/tutorials/04-daily-workflow/02-rewind.md) |
| **Routine** | Prompt that runs on a schedule in a fresh session | [04-5](docs/tutorials/04-daily-workflow/05-routines.md) |
| **Session** | One conversation inside a project | [00-3](docs/tutorials/00-getting-started/03-desktop-ui-tour.md) |
| **settings.json** | Project/global config: permissions, hooks, behavior | [02-3](docs/tutorials/02-project-context/03-settings-json.md) |
| **Source audit** | Having a second AI review an AI-gathered source list for duplicates, fabrications and wrong focus | [06-2](docs/tutorials/06-learning-with-ai/02-collect.md) |
| **Skill** | Reusable Markdown instructions, invoked with `/name` or automatically | [03-1](docs/tutorials/03-extending-claude/01-skills.md) |
| **Subagent** | Specialist Claude worker with its own context window | [03-2](docs/tutorials/03-extending-claude/02-subagents.md) |
| **Token** | Unit of text the model processes; drives context size and usage | [04-1](docs/tutorials/04-daily-workflow/01-context-management.md) |
| **Worktree** | Separate git checkout so parallel sessions don't clash | [04-3](docs/tutorials/04-daily-workflow/03-parallel-sessions-worktrees.md) |
