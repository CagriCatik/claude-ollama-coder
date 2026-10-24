import json

import pytest
from httpx import ASGITransport, AsyncClient

from swarm_coordinator.api.routes import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_create_and_get_run(client):
    response = await client.post("/api/runs", json={"input": "task", "telemetry": {"risk_level": "low", "requirements_met": True}})
    assert response.status_code == 200
    data = response.json()
    run_id = data["run_id"]
    get_resp = await client.get(f"/api/runs/{run_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["run_id"] == run_id


@pytest.mark.asyncio
async def test_sse_stream_events(client):
    response = await client.post("/api/runs", json={"input": "task", "telemetry": {"risk_level": "low", "requirements_met": True}})
    run_id = response.json()["run_id"]
    events = []
    async with client.stream("GET", f"/api/runs/{run_id}/events") as resp:
        assert resp.status_code == 200
        async for line in resp.aiter_lines():
            if line.startswith("data:"):
                events.append(json.loads(line[5:].strip()))
            if line.startswith("event: run_finished"):
                # continue reading until stream ends
                pass
    event_names = [e.get("event") for e in events]
    assert "component_started" in event_names
    assert "review_completed" in event_names
    assert "execution_completed" in event_names
    assert "run_finished" in event_names
    # timestamps and run ids
    for e in events:
        assert "timestamp" in e
        assert e["run_id"] == run_id


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"