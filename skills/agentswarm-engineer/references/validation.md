# AgentSwarm verification and acceptance matrix

A successful test is evidence only for the exercised path. Record installed dependency versions, test environment, skipped tests, and external resources before claiming production readiness.

## Default testing ladder

Execute from the repository root. Use the repo's `.venv` if present; never install into the global Python environment without permission.

```bash
python -m pytest tests/backend/unit/test_architecture_rules.py -q
python -m pytest tests/backend/unit -q
python -m pytest tests/backend/contract -q
python -m pytest tests/backend/integration -q
python -m pytest tests/backend/e2e -q
npm --prefix frontend run build
git diff --check
```

On a clean checkout with dependencies missing, install backend with `python -m pip install -e '.[dev]'` in a virtual environment and frontend with `npm --prefix frontend ci`. Some integration/e2e tests may invoke Ollama; report `SKIPPED` or `BLOCKED` if the model is unavailable rather than quietly replacing it with a mock. For deterministic CI, explicitly inject fake models and transports.

## Change-to-tests mapping

| Edited concern | Minimum evidence |
| --- | --- |
| Domain / business rule | `tests/backend/unit/test_domain.py`, `test_application_services.py` and negative cases |
| Port / adapter / storage | `test_adapters.py`; missing/malformed filesystem inputs and path traversal |
| Configuration / model | `test_config_logging.py`, `test_ollama_models.py` where model is reachable; effective env values |
| MCP tool/resource | `tests/backend/contract/test_mcp_contracts.py`; discovery, request schema, error mapping, typed result |
| A2A services | `tests/backend/contract/test_a2a_contracts.py` + **real HTTP** requests matching the coordinator's actual `SendMessage` payload |
| Coordinator | `test_failure_injection.py`, `test_specialist_agents.py`, full pathway with fake transports and fallback failures |
| REST / SSE | `tests/backend/contract/test_api_contracts.py`; run status, replay, event ordering and cleanup |
| Full workflow | `tests/backend/e2e/*.py`; both in-process and separate server modes where relevant |
| React graph / UI | `npm --prefix frontend run build`; browser-level checks of `RunPanel`, `LiveTraceTimeline`, `NodeInspector`, `PayloadViewer` and graph |
| Deployment | `docker compose config`, build, effective env, accessible health/API, model availability, container boundaries |

## Standalone A2A smoke protocol

Start only after confirming the app is safe to run; agent models or fallback modes may be involved.

```bash
python main.py --mode analyst-server        # terminal A, port 8101
python main.py --mode knowledge-server      # terminal B, port 8102
```

Probe `POST /` with `{"jsonrpc":"2.0","method":"SendMessage","params":{"message":{"message_id":"m1","role":"ROLE_USER","parts":[{"text":"read-only diagnostic"}]}},"id":"1"}` and assert correct result *and* error semantics. Probe `/health` and the discovery URL `/.well-known/agent-card.json` if claiming standard A2A compatibility. In the pinned snapshot, only Knowledge handles `SendMessage` and none of the five servers registers the well-known discovery route; a passing custom `execute` method is insufficient.

## SSE replay and telemetry

1. Create a run with `POST /api/runs` (payload `message` and optional `model`). Capture returned `run_id`/`trace_id`.
2. Subscribe to `GET /api/runs/{run_id}/events` using a real SSE client; validate `event` names, JSON shapes, monotonically increasing sequence and terminal `run_finished`.
3. Reconnect/replay and assert no event silently lost or duplicated by the client. Verify events from concurrent runs do not cross-contaminate.
4. Compare reported per-stage/mcp durations with real source timers. Reject invented spans unless explicitly labeled illustrative.

## Security and production gating

Treat this repository as a reference implementation until these controls are verified:

- **Authorization:** identity and permissions verified server-side with fail-closed defaults; never accept `authorized=True` merely because a field was omitted.
- **Approval:** pre-action review, explicit operator sign-off for destructive changes, target allowlists, idempotency and bounded blast radius.
- **Execution:** distinguish mock adapter from production adapter; test actual side effects, failures, retries and rollback safely in staging.
- **Inputs:** request validation, size limits, document ID path confinement, prompt-injection boundaries, telemetry access controls.
- **Operational:** timeout/cancellation, logging without secrets/PII, durable audit, rate limits, multi-run state lifecycle, model failure reporting.
- **Protocols:** validated MCP version and actual A2A spec/SDK interoperability, not a label or a superficial JSON-RPC envelope.

## Reporting standard

Report `PASS`, `FAIL`, `SKIP`, `BLOCKED`, or `NOT RUN` for every relevant check, with exact command and key error. Separate unit/contract, mock/in-process integration, live service and manual UI checks. Do not claim a comprehensive test result from source inspection or from static linting alone.
