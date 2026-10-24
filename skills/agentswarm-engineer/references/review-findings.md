# Pinned repository review findings

Repository: https://github.com/CagriCatik/AgentSwarm
Revision: `a06afa1e73c2ed39c8bcd4470b69adab08cfa47a` (2026-10-01).

These findings are **source-inspection conclusions, not runtime-tested failures** in this skill package. Verify each against current local HEAD. Prioritize the first three before connecting production infrastructure.

## Critical — no pre-execution audit gate

`backend/agents/coordinator/orchestrator.py::run()` calls `request_execution(user_query)` before `request_review(user_query)`. `backend/api/runner.py::execute_run()` does the same. `backend/application/audit_service.py` defaults `authorized` and `signoff_approved` to `True` if absent. A downstream audit cannot prevent an action already dispatched. Introduce proposal/preflight permission and policy checks, fail-closed defaults, explicit approval, then execution and independent verification. Add denial and regression tests. This is an unsafe architecture if a real dispatcher is introduced.

## High — coordinator/specialist A2A request mismatch

`backend/agents/coordinator/a2a_client.py::send_message()` sends JSON-RPC method `SendMessage` to `/`. Only `backend/agents/knowledge/server.py` handles `SendMessage`; `analyst/server.py`, `executor/server.py`, `reviewer/server.py` and `custom/server.py` handle different methods. `backend/cli/chat.py::create_cli_coordinator()` overrides delivery using per-server `TestClient`, so successful in-process behavior is not proof of network interoperability. Make method, request and response schemas symmetric and add real HTTP tests.

## High — claimed standard A2A discovery not actually exposed

`A2AClient.fetch_agent_card` requests `/.well-known/agent-card.json`, but the five Starlette `server.py` files register only `/`, `/a2a`, and `/health`; `get_agent_card` is exposed as an ad hoc JSON-RPC method instead. The repo imports `a2a-sdk` as a dependency but the reviewed servers do not use the standard SDK server/task classes. Verify standards compliance before advertising fully interoperable Google A2A. The `documentation/08_ADDING_NEW_AGENTS.md` four-file blueprint (`card.py`/`executor.py`) diverges from actual current packages.

## High — simulated actions appear as executed

`backend/adapters/mock_action_dispatcher.py` synthesizes successful action results and fake operational details (e.g., pods restarted, stakeholder broadcasts). `backend/application/action_service.py` delegates to this adapter. No proof of infrastructure mutation exists. Surface simulation explicitly in API, UI, logs and reports; do not silently substitute real infrastructure adapters.

## Medium — trace timings do not describe measured MCP calls

`backend/api/runner.py` publishes `protocol_call_*` MCP events with durations derived from agent time (for example `analyst_duration * 0.5`), not independent MCP timing. The UI displays these as if measured spans. Instrument actual tool boundary durations or label synthetic timing as illustrative.

## Medium — knowledge-base search is keyword scoring

`backend/adapters/markdown_knowledge_repository.py::search()` splits query into words with `re.findall`, computes lexical scores from title/tags/content and sorts results. It is not embedding retrieval/vector search; the README's RAG characterization is broader than the present implementation. Keep search semantics accurate until implemented and verified.

## Medium — Docker Ollama environment overrides require verification

`docker-compose.yml` passes `OLLAMA_BASE_URL` and `OLLAMA_MODEL`; `backend/common/config.py::load_config()` only explicitly maps `COCKPIT_HOST` and `COCKPIT_PORT` from environment. `backend/agents/shared/model_factory.py` reads `get_config().ollama.base_url`, not those env variables. Confirm the effective runtime model URL or add validated env handling.

## Low — entrypoint / docs drift

The README suggests `python main.py --mode cli`; `main.py` accepts `chat` instead. Its getting-started examples emphasize Windows `dev.bat`. Use platform-specific commands and update README and test recipes whenever the CLI contract changes.

## Related reliability/security checks (not yet fully audited)

- Check `MarkdownKnowledgeRepository.get_by_id()` for `document_id` path confinement: it joins user-provided text into a filesystem path after only stripping `.md`.
- Inspect `CustomAgent._deterministic_fallback()` and other agent fallbacks for `SUCCESS` results after an exception. Do not mask model failures as completed external work.
- Inspect in-memory `backend/api/execution_bus.py` run lifetime and retention, unbounded queues, concurrency and SSE subscription cleanup before multi-user deployments.
- Check `frontend/src/store/workflowStore.ts` hardcoded initial topology against `/api/topology` for drift.

## Source hierarchy for future reviews

1. Current code and tests (exact commit SHA).
2. Runtime evidence / transport probes / build outputs.
3. Config and deployment files.
4. README and documentation as intended design only.

The above severity ratings reflect the effect of introducing real operational side effects. They do not mean the currently bundled mock test environment has already altered production services.
