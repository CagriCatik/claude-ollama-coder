import pytest
from httpx import ASGITransport, AsyncClient

from swarm_coordinator.api.routes import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_send_message_jsonrpc(client):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "SendMessage",
        "params": {"message": {"parts": [{"text": "hello"}]}},
    }
    for path in ["/", "/a2a"]:
        response = await client.post(path, json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 1
        assert "result" in data
        assert data["result"]["status"] in ("finished", "rejected", "simulated")


@pytest.mark.asyncio
async def test_agent_card(client):
    response = await client.get("/.well-known/agent-card.json")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "skills" in data