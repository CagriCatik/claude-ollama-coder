# AgentSwarm implementation recipes

Run these as an engineering checklist, not as blind generation templates. Start each task by inspecting the current commit and relevant tests. Do not add abstractions that do not serve a concrete boundary.

## New specialist

1. Define responsibility, authorization scope, accepted user inputs, output schema, and **tool allowlist**. If possible, add a domain/service or port without coupling it to smolagents.
2. Copy the **current real implementation pattern** from `backend/agents/custom/{agent.py,server.py}`. The documented `card.py`/`executor.py` template is not implemented in the pinned tree. Decide whether to retain the current handcrafted RPC for internal compatibility or deliberately migrate all agents to the official A2A SDK; never mix incompatible contracts without a compatibility layer.
3. Add Pydantic result model in `backend/agents/shared/result_models.py`; require explicit failed/error states and provenance. Avoid converting model failures into `SUCCESS`.
4. Add `agents.<name>` and prompts in both `config/config.yaml` and `backend/common/config.py`; use a nonconflicting port.
5. Register a descriptor in `backend/agents/coordinator/orchestrator.py`; add delegation method, conditional route/decision, and any synthesis contract fields. Register it only if the workflow actually invokes it.
6. Implement transport consistently: `/health`, service card discovery, method names including `SendMessage` if used by the shared coordinator client, and well-defined JSON-RPC success/error envelopes. Verify external A2A clients if standards compliance is claimed.
7. If an MCP tool is needed, follow the next recipe; don't give the new agent every tool by default.
8. Update `main.py` server modes, `backend/cli/chat.py` local bootstrap (if required), `backend/api/app.py` topology, `backend/api/runner.py` execution/events, frontend workflow graph and inspectors, and documentation. Consider shared topology definitions to reduce drift.
9. Test result parsing, prompt fallback, tool restrictions, bad/missing params, HTTP RPC, timeouts, coordinator dispatch, in-process CLI and standalone A2A transport, SSE, and UI rendering.

## New MCP tool/resource

1. Specify named operation, precise input/response schema, trust boundary, side effects, authentication, and failure contract.
2. For business behavior, put rules in `backend/application/`; define `backend/ports/` and `backend/adapters/` when new I/O is needed. Avoid pushing business logic into a FastMCP decorator.
3. Add handler under `backend/mcp_server/tools/`, wire service factory in `backend/mcp_server/dependencies.py`, and register `@server.tool` or `@server.resource` in `backend/mcp_server/server.py`.
4. Add a narrow smolagents wrapper under `backend/agents/shared/mcp_factory.py` **only for the specialist that needs it**. Ensure JSON representation, return value and async bridge are actually compatible with the installed MCP/smolagents versions.
5. Update specialist instructions in `config/config.yaml`, direct tool-call tests in `tests/backend/contract/test_mcp_contracts.py`, service unit tests, agent integration tests, and relevant docs.
6. If tool mutates state, apply permission checks and durable audit **before dispatch**. Keep mock mode explicit and unit-test it separately from live adapters.

## Coordinator and protocol

1. Reproduce the actual request: `A2AClient.send_message` emits method `SendMessage`, with `message.parts[]`. Compare it with every `backend/agents/*/server.py` handler. In the pinned snapshot, only Knowledge accepts `SendMessage`.
2. Decide whether the goal is a private JSON-RPC interface or full A2A interoperability. An endpoint claiming `protocol: Google A2A` is not proof of A2A SDK compatibility; check well-known Agent Card, standard message schema, streaming/cancellation semantics, and integration tests with the official SDK when needed.
3. Fix protocol symmetry end-to-end (client + all servers) with contract tests first. Include unknown method, malformed JSON, missing message parts, timeout, transient refusal, and structured errors.
4. Do not use the CLI TestClient transport as the only proof: `backend/cli/chat.py` bypasses HTTP and can mask network compatibility failures.
5. For action flows, model `propose -> authorize -> review -> approve -> dispatch -> verify -> audit record` with denied/timeout/rollback paths. Current coordinator and `backend/api/runner.py` instead call Executor before Reviewer; migration must preserve UI trace semantics while removing this risk.
6. Refactor duplicate orchestration logic in `CoordinatorOrchestrator.run` and `backend/api/runner.py` carefully; maintain exact public API/SSE contracts and add controlled fake agent tests.

## Cockpit and events

1. Locate API schemas in `backend/api/schemas.py`; follow `app.py` / `runner.py` / `execution_bus.py` to establish event source and sequencing.
2. Track a field from API response to `frontend/src/types/workflow.ts`, `frontend/src/store/runStore.ts`, `frontend/src/store/workflowStore.ts`, and the specific `features/` inspector/view.
3. Keep event names synchronized: `component_started`, `component_completed`, `protocol_call_started`, `protocol_call_completed`, `run_finished`. Protect the SSE replay/reconnect behavior, listener cleanup, terminal states, and duplicate event handling.
4. Avoid fabricating MCP duration values. In pinned `runner.py`, an MCP event uses an arbitrary fraction of agent latency. Record observed transport spans or label illustrative events explicitly as synthetic.
5. Keep topology nodes consistent between server `GET /api/topology` and `frontend/src/store/workflowStore.ts` defaults. Test newly added agents on all UI surfaces and narrow viewport layouts.
6. Run `npm --prefix frontend run build`, API/SSE contract tests, and browser inspection (if browser available). Do not claim visual QA from successful TypeScript compilation alone.

## Model and deployment configuration

- `backend/agents/shared/model_factory.py` uses `get_config().ollama.base_url` to construct `/v1`; confirm a live model separately with Ollama health/tag/chat APIs when the task requires inference.
- Docker Compose passes `OLLAMA_BASE_URL` and `OLLAMA_MODEL`, but the pinned `backend/common/config.py` does not map those env vars. Inspect effective config in the container before assuming overrides work; implement/test the env mapping when changing deployment.
- `main.py --mode chat` is the supported interactive mode. The README's `--mode cli` is stale. `dev.bat` is Windows-oriented; use direct `python`/`npm` commands on Unix.
- Keep `data/` fixtures representative. Do not check in credentials or real private telemetry.

## Change acceptance mini-template

- Goal / user-visible behavior
- Touched boundaries and public contracts
- Threat/side-effect model
- Test examples (happy path, malformed, denied, timeout, fallback)
- Implementation and documentation changes
- Observed test commands and results
- Known limitations and deferred tasks
