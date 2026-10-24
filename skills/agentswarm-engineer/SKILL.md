---
name: agentswarm-engineer
description: Engineering workflow for CagriCatik/AgentSwarm, the Python smolagents, FastMCP, A2A-style JSON-RPC, Ollama, FastAPI/SSE, and React/XYFlow reference repository. Use when Claude Code must analyze, debug, extend, test, refactor, or harden AgentSwarm; add specialist agents or MCP tools; change coordinator orchestration, protocol contracts, the visual cockpit, or deployment. Enforce hexagonal architecture, inspect live source rather than trusting documentation, and verify safety and end-to-end behavior. Do not use for unrelated agent frameworks.
license: MIT
compatibility: Claude Code 1.0+, AgentSwarm
metadata:
  author: claude-ollama-coder
  version: "1.0.0"
---

# AgentSwarm Engineering

Operate on an **existing** AgentSwarm checkout. This is a Claude Code coding workflow, not an AgentSwarm runtime agent or an MCP server. Never imply that loading this skill launches a swarm. The reference analysis is grounded in `CagriCatik/AgentSwarm` `main` commit `a06afa1e73c2ed39c8bcd4470b69adab08cfa47a` (2026-10-01); actual working-tree code takes precedence.

---

## When to Use This Skill

- **Trigger Scenarios:**
  - When analyzing, debugging, extending, refactoring, or hardening AgentSwarm.
  - When adding specialist agents or FastMCP tools to an AgentSwarm deployment.
  - When modifying coordinator orchestration, A2A-style JSON-RPC protocol contracts, or SSE event telemetry.
  - When developing or testing the visual cockpit or FastAPI endpoints.
  - When verifying hexagonal architecture boundaries and fail-closed security gates.

- **When NOT to Use:**
  - Do not use for unrelated multi-agent frameworks (e.g., AutoGen, CrewAI, LangGraph standalone).
  - Do not use as a runtime agent or server launcher; this is a Claude Code engineering workflow.

---

## First: establish the local truth

1. Locate the repository root (contains `pyproject.toml`, `main.py`, `backend/`, `frontend/`, `config/config.yaml`). Check `git status --short`, `git rev-parse HEAD`, and relevant files. Respect existing user edits; do not reset, overwrite, or commit them.
2. Read `README.md`, the relevant `documentation/*.md`, **and the implementation/tests**. This repository's documentation contains material inaccuracies. Treat imported classes, endpoint handlers, actual configuration reads, and tests as authoritative.
3. Optionally run `python <skill-directory>/scripts/repo_probe.py --root .` for a read-only, no-dependency static inventory. Inspect its flagged conditions in code before drawing conclusions.
4. Identify the requested task and trace its complete data/control path. Read [architecture.md](references/architecture.md) before cross-layer edits and [review-findings.md](references/review-findings.md) when dealing with protocol, compliance, production-readiness, or documentation claims.

## Choose the task recipe

- **Add a specialist agent:** Follow [workflows.md](references/workflows.md) → "New specialist". Use `backend/agents/custom/` as the **actual** starting blueprint; it currently has `agent.py` and `server.py`, not the four-file A2A SDK layout shown in some docs. Add typed output, configuration, registrations, handler, and contract/integration coverage.
- **Add an MCP tool/resource:** Follow [workflows.md](references/workflows.md) → "New tool". Wire domain → port/adapter (if needed) → application service → `backend/mcp_server/tools/` → `backend/mcp_server/server.py` → `backend/agents/shared/mcp_factory.py` → relevant specialist. Preserve tool isolation and add direct tool-call tests.
- **Change orchestration/A2A:** Follow [workflows.md](references/workflows.md) → "Coordinator and protocol". Treat `backend/agents/coordinator/a2a_client.py`, all `backend/agents/*/server.py`, and `backend/cli/chat.py` as one distributed contract. Test both in-process and standalone HTTP; they are not interchangeable.
- **Change API, SSE, or UI:** Follow [workflows.md](references/workflows.md) → "Cockpit and events". Update typed FastAPI schemas and React types/stores together. Separate measured events from simulated/display-only events.
- **Debug, review, security hardening, or refactor:** Reproduce first, identify the owning boundary, add a regression test, implement the smallest coherent fix, and run the test matrix in [validation.md](references/validation.md).

## Non-negotiable architecture contracts

- Keep `backend/domain/` framework-independent and `backend/ports/` abstract. Place I/O in adapters; business rules in `backend/application/`; MCP/FastAPI/A2A/CLI in transport boundaries.
- Do not import specialist implementation classes, the MCP server, or raw storage into `backend/agents/coordinator/`. Specialists must not directly import one another. Run `tests/backend/unit/test_architecture_rules.py` on such edits.
- Keep output schemas in `backend/agents/shared/result_models.py` consistent with actual agent responses, A2A payloads, API models, and frontend event consumers. Validate unknown/malformed inputs explicitly.
- Introduce **no live production action** through `MockActionDispatcher` by silently swapping adapters. Implement deny-by-default authorization, target/parameter allowlists, explicit approval, idempotency, timeouts, audit-before-action, and safe rollback boundaries first. Distinguish `proposed`, `approved`, `simulated`, and `executed` states.
- Never claim standards compliance based solely on file names, JSON-RPC framing, installed dependencies, or a passing mock test. Verify against the SDK/spec version in use.
- Never call the Markdown keyword search implementation a vector index or embedding RAG unless the implementation changes and tests prove it.
- Never replace errors or model failures with a reported real-world success. Preserve explicit fallback/source provenance in tests and UI.

## Implementation sequence

1. **Map:** State the affected packages/interfaces and test surface, plus risks and assumptions. Prefer cohesive vertical slices over scattered patches.
2. **Reproduce:** Create a minimal failing test or direct protocol request before fixing an observed bug. For feature work, define acceptance examples including failure and timeout paths.
3. **Change:** Make the narrowest consistent edits, preserving public API compatibility unless intentionally versioning it. Update documentation when behavior changes.
4. **Validate:** Start with focused unit and contract tests; then integration/e2e, frontend build, and optional live services. Follow [validation.md](references/validation.md). Do not assert anything ran unless it did.
5. **Review:** Check protocol symmetry, data provenance, safety-before-execution, concurrency, cleanup, UI consistency, and unexpected changes using `git diff --check` and `git diff`.
6. **Report:** Summarize files changed, behavior, exact verification commands/results, untested dependencies, remaining risks, and next action. For reviews, rank findings by severity with file paths and minimal reproduction steps. Never invent benchmark numbers or green CI.

## Local commands (verify environment first)

```bash
python -m pip install -e '.[dev]'
python -m pytest tests/backend/unit tests/backend/contract
python -m pytest tests/backend/integration tests/backend/e2e
npm --prefix frontend ci
npm --prefix frontend run build
python main.py --mode chat                  # actual interactive CLI mode
python main.py --mode cockpit               # FastAPI :8006
python main.py --mode mcp-server            # MCP :8000
```

Ollama-dependent tests may need a reachable model; never turn an unavailable model into a claimed test pass. `dev.bat` targets Windows; use Python/npm commands on macOS or Linux. The isolated Docker deployment builds the cockpit but does not itself prove distributed A2A interoperability.

## References (load only as relevant)

- [architecture.md](references/architecture.md): package ownership, topology, entrypoints, actual protocols.
- [workflows.md](references/workflows.md): implementation recipes for agents, tools, orchestration, UI, and config.
- [validation.md](references/validation.md): coverage matrix, smoke commands, release gates.
- [review-findings.md](references/review-findings.md): verified snapshot-specific mismatches and corrective priorities.

---

## Self-Verification Checklist

Before merging, releasing, or concluding an AgentSwarm engineering task:
- [ ] Hexagonal architecture is preserved: `domain/` and `ports/` have zero framework imports.
- [ ] Pre-execution safety gate is verified: review & audit checks occur before any execution step.
- [ ] Fail-closed authorization: `authorized` and `signoff_approved` default strictly to `False`.
- [ ] Protocol symmetry: coordinator and specialist handlers match JSON-RPC 2.0 `SendMessage` contracts.
- [ ] Discovery route `GET /.well-known/agent-card.json` is registered and functional.
- [ ] Simulated outcomes are explicitly flagged (`is_simulated=True`) with no fake production mutation claims.
- [ ] All unit, contract, integration, and frontend build tests pass cleanly.

