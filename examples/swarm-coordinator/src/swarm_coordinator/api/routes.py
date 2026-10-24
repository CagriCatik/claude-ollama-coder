"""FastAPI transport, runs, health, agent card and A2A JSON-RPC."""

from __future__ import annotations

from uuid import UUID

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

from swarm_coordinator.api.sse import EventBus, format_sse
from swarm_coordinator.application.coordinator import SwarmCoordinator
from swarm_coordinator.domain.models import RunState
from swarm_coordinator.protocol.a2a_models import (
    JsonRpcRequest,
    JsonRpcResponse,
)
from swarm_coordinator.protocol.agent_card import AgentCard

app = FastAPI(title="Swarm Coordinator", version="0.1.0")

_event_bus = EventBus()
_coordinator = SwarmCoordinator(event_bus=_event_bus)
_run_store: dict[UUID, RunState] = {}


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "swarm-coordinator"}


@app.get("/.well-known/agent-card.json")
async def agent_card() -> dict:
    return AgentCard().model_dump(by_alias=True)


@app.post("/api/runs")
async def create_run(request: Request) -> dict:
    body = await request.json()
    description = body.get("input") or body.get("description") or body.get("task") or ""
    telemetry = body.get("telemetry", {})
    state = await _coordinator.run(description, telemetry)
    _run_store[state.run_id] = state
    return state.model_dump(mode="json")


@app.get("/api/runs/{run_id}")
async def get_run(run_id: UUID) -> dict:
    state = _run_store.get(run_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return state.model_dump(mode="json")


@app.get("/api/runs/{run_id}/events")
async def run_events(run_id: UUID) -> StreamingResponse:
    if run_id not in _run_store:
        # allow streaming for not-yet-stored? still 404
        raise HTTPException(status_code=404, detail="Run not found")

    async def generator():
        async for event in _event_bus.subscribe(run_id):
            yield await format_sse(event)
            if event.event.value == "run_finished":
                break

    return StreamingResponse(generator(), media_type="text/event-stream")


def _extract_text(params: dict) -> str:
    # Supports params: {"message": {"parts": [{"text": "..."}]}}
    message = None
    if isinstance(params, dict):
        message = params.get("message")
    if message is None and isinstance(params, dict):
        message = params
    if isinstance(message, dict):
        parts = message.get("parts", [])
        texts = [p.get("text", "") for p in parts if isinstance(p, dict)]
        return " ".join(t for t in texts if t)
    if isinstance(params, dict) and "text" in params:
        return str(params["text"])
    return str(params)


async def _handle_jsonrpc(request: Request) -> JSONResponse:
    raw = await request.json()
    try:
        req = JsonRpcRequest.model_validate(raw)
    except Exception as exc:  # noqa: BLE001
        return JSONResponse(
            JsonRpcResponse(jsonrpc="2.0", id=raw.get("id") if isinstance(raw, dict) else None, error={"code": -32600, "message": str(exc)}).model_dump(mode="json")
        )
    if req.method != "SendMessage":
        return JSONResponse(
            JsonRpcResponse(id=req.id, error={"code": -32601, "message": "Method not found"}).model_dump(mode="json")
        )
    text = _extract_text(req.params)
    state = await _coordinator.run(text, {})
    _run_store[state.run_id] = state
    result = {
        "run_id": str(state.run_id),
        "status": state.status.value if hasattr(state.status, "value") else str(state.status),
        "result": state.result.model_dump(mode="json") if state.result else None,
    }
    return JSONResponse(JsonRpcResponse(id=req.id, result=result).model_dump(mode="json"))


# A2A endpoints (symmetric)
@app.post("/")
async def a2a_root(request: Request) -> JSONResponse:
    return await _handle_jsonrpc(request)


@app.post("/a2a")
async def a2a_path(request: Request) -> JSONResponse:
    return await _handle_jsonrpc(request)