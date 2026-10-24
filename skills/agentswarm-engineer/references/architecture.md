# AgentSwarm source-level architecture map

Snapshot: `main` at `a06afa1e73c2ed39c8bcd4470b69adab08cfa47a`, 2026-10-01. Check local HEAD before applying this map.

## Entry points

| Boundary | Main source | Contract / notes |
| --- | --- | --- |
| Process launcher | `main.py` | Modes `cockpit`, `flow`, `chat`, `mcp-server`, `<specialist>-server`; `--query` takes batch path |
| Configuration | `backend/common/config.py`, `config/config.yaml` | Pydantic models and YAML; config file auto reload by mtime; `COCKPIT_HOST` / `COCKPIT_PORT` env overrides |
| Domain | `backend/domain/{task,knowledge,telemetry,action,audit}.py` | Pydantic entities/enums; no orchestration, FastAPI or MCP imports |
| Ports | `backend/ports/*.py` | Abstract repositories and action dispatcher |
| Adapters | `backend/adapters/*.py` | JSON telemetry/tasks, Markdown knowledge, **mock** action dispatch |
| Application | `backend/application/*.py` | Telemetry, Knowledge, Action, Audit services |
| MCP facade | `backend/mcp_server/server.py`, `tools/*.py`, `dependencies.py` | FastMCP tool registration and service dependencies |
| Smolagents bridge | `backend/agents/shared/mcp_factory.py` | Wraps FastMCP calls as smolagents tools, in-process; async bridge `_run_async` |
| Model | `backend/agents/shared/model_factory.py` | `OpenAIServerModel` pointed at Ollama `/v1`; model listing via `/api/tags` |
| Specialists | `backend/agents/{analyst,knowledge,executor,reviewer,custom}/` | `agent.py` ToolCallingAgent; `server.py` Starlette JSON-RPC endpoints |
| A2A coordinator | `backend/agents/coordinator/{orchestrator,a2a_client,registry}.py` | Registry, HTTP JSON-RPC client, delegated results, final LLM synthesis |
| Local CLI | `backend/cli/chat.py` | Rich interaction, creates **in-process** specialist TestClients and replaces A2A send transport |
| Cockpit API | `backend/api/{app,schemas,runner,execution_bus}.py` | REST, run state, SSE lifecycle |
| Cockpit client | `frontend/src/store/{runStore,workflowStore}.ts` | Zustand run/SSE and graph state; `features/` XYFlow UI |

## Current control/data paths

### Remote-style orchestration

```
user query -> CoordinatorOrchestrator
   -> A2AClient.send_message -> specialist Starlette HTTP -> smolagents ToolCallingAgent
   -> MCP tool wrapper -> FastMCP.call_tool -> thin handler -> application service
   -> port -> concrete adapter -> JSON/Markdown/mock
   -> Pydantic result -> Coordinator -> grounded synthesis/fallback
```

Note: This is the **intended** path; standalone A2A `SendMessage` support is incomplete in the pinned snapshot. Do not draw a working end-to-end arrow without testing it.

### Cockpit run path

`POST /api/runs` -> `RunRecord` -> `execute_run()` -> `create_cli_coordinator()` (in-process TestClients) -> events in `RunRecord` -> `GET /api/runs/{id}/events` SSE -> `runStore` -> `workflowStore.applyExecutionEvent()` -> XYFlow inspector/timeline. Final result also from `GET /api/runs/{id}`. REST topology from `GET /api/topology`; some frontend initial nodes are hardcoded independently.

### Protocol and port ownership

- MCP tool names: `get_system_metrics`, `analyze_system_telemetry`, `search_knowledge_base`, `get_knowledge_document`, `execute_swarm_action`, `audit_compliance`, `get_swarm_health`. Resource: `swarm://knowledge/{document_id}`. The MCP server default port is `8000`.
- Specialist defaults: Analyst `8101`, Knowledge `8102`, Executor `8103`, Reviewer `8104`, Custom `8105`.
- Cockpit FastAPI `8006` and Vite dev frontend `5173`.
- Model service default `http://localhost:11434` (Ollama). `config/config.yaml` currently selects `gpt-oss:120b-cloud`; do not assume a model is installed, accessible or free.
- `frontend/src/store/runStore.ts` posts `/api/runs` and opens the named SSE event stream. When running standalone Vite, verify proxy configuration in `frontend/vite.config.ts` rather than assuming `/api` resolves.

## Layers and dependencies to preserve

1. Domain owns invariants and typed data, imports no external framework.
2. Ports define interfaces; application logic depends on those abstractions.
3. Adapters implement filesystem and action I/O; MCP transport does not own business logic.
4. Specialist agents depend on domain-specific tools, not other specialists.
5. Coordinator delegates to specialists using a protocol client; it must not reach into their implementations or raw files.
6. API/CLI/UI orchestrate presentations, not authorization or domain rules.

Start with `tests/backend/unit/test_architecture_rules.py`. It checks AST imports in selected directories, not every possible runtime dependency; perform a manual design review as well.

## Documentation reliability

The `README.md` and `documentation/` directory provide design **intent**, not a definitive specification. For example, they describe official Google A2A SDK-style `card.py`/`executor.py` modules while the actual specialist packages use handcrafted `server.py` Starlette routes. The README labels Markdown keyword scoring as vector RAG. Verify actual code before extending either interface.
