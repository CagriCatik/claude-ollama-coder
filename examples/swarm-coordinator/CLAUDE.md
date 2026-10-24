# CLAUDE.md

## Commands
- Install: `pip install -e ".[dev]"`
- Tests: `pytest tests/ -v`
- Run: `uvicorn swarm_coordinator.api.routes:app --reload`

## Architecture rules
- domain/: pure entities, zero framework imports
- ports/: abstract protocols only
- adapters/: I/O implementations
- application/: orchestration & business logic
- api/: transport only

## Gotchas
- Audit defaults fail-closed.
- Mock dispatcher returns simulated only.
- Do not execute before review approval.
- SSE stream ends on run_finished.