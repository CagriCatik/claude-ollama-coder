"""Tests for FastAPI endpoints."""

from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from agent_dispatcher.api.routes import app
from agent_dispatcher.models.envelope import TaskEnvelope


@pytest.fixture
async def async_client() -> AsyncClient:
    """Async test client for FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


class TestDispatchTaskEndpoint:
    """Test POST /v1/tasks endpoint."""

    async def test_valid_dispatch_returns_201(self, async_client: AsyncClient) -> None:
        """Valid envelope returns 201 Created with envelope."""
        envelope = TaskEnvelope(
            task_id=uuid4(),
            source_agent="orchestrator",
            target_agent="agent-coder",
            payload={"action": "test"},
        )

        response = await async_client.post(
            "/v1/tasks",
            json=envelope.model_dump(mode="json"),
        )

        assert response.status_code == 201
        data = response.json()
        assert data["task_id"] == str(envelope.task_id)
        assert data["status"] == "running"
        assert data["target_agent"] == "agent-coder"

    async def test_valid_dispatch_with_all_fields(self, async_client: AsyncClient) -> None:
        """Valid envelope with all fields works."""
        envelope = TaskEnvelope(
            task_id=uuid4(),
            source_agent="orchestrator",
            target_agent="agent-researcher",
            payload={"query": "test query"},
            status="pending",
        )

        response = await async_client.post("/v1/tasks", json=envelope.model_dump(mode="json"))

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "running"  # Updated by dispatcher
        assert data["payload"] == {"query": "test query"}

    async def test_invalid_target_agent_returns_404(self, async_client: AsyncClient) -> None:
        """Unknown target agent returns 404 with RFC 7807 problem details."""
        envelope = TaskEnvelope(
            task_id=uuid4(),
            source_agent="orchestrator",
            target_agent="unknown-agent",
        )

        response = await async_client.post(
            "/v1/tasks",
            json=envelope.model_dump(mode="json"),
        )

        assert response.status_code == 404
        data = response.json()
        assert data["type"] == "https://api.example.com/errors/agent-not-found"
        assert data["title"] == "Target Agent Not Found"
        assert data["status"] == 404
        assert "not registered" in data["detail"]
        assert "instance" in data

    async def test_missing_required_field_returns_422(self, async_client: AsyncClient) -> None:
        """Missing required field returns 422 with validation error."""
        # Missing target_agent
        payload = {
            "task_id": str(uuid4()),
            "source_agent": "orchestrator",
            "payload": {},
        }

        response = await async_client.post("/v1/tasks", json=payload)

        assert response.status_code == 422
        data = response.json()
        assert data["type"] == "https://api.example.com/errors/validation-error"
        assert data["title"] == "Request Validation Failed"
        assert data["status"] == 422
        assert "target_agent" in data["detail"]

    async def test_empty_source_agent_returns_422(self, async_client: AsyncClient) -> None:
        """Empty source_agent returns 422."""
        payload = {
            "task_id": str(uuid4()),
            "source_agent": "",
            "target_agent": "agent-coder",
        }

        response = await async_client.post("/v1/tasks", json=payload)

        assert response.status_code == 422

    async def test_invalid_status_returns_422(self, async_client: AsyncClient) -> None:
        """Invalid status value returns 422."""
        payload = {
            "task_id": str(uuid4()),
            "source_agent": "orchestrator",
            "target_agent": "agent-coder",
            "status": "invalid-status",
        }

        response = await async_client.post("/v1/tasks", json=payload)

        assert response.status_code == 422

    async def test_invalid_json_returns_422(self, async_client: AsyncClient) -> None:
        """Invalid JSON returns 422 (unprocessable content)."""
        response = await async_client.post(
            "/v1/tasks",
            content="not valid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422
        data = response.json()
        assert data["type"] == "https://api.example.com/errors/validation-error"
        assert data["title"] == "Request Validation Failed"


class TestListAgentsEndpoint:
    """Test GET /v1/agents endpoint."""

    async def test_list_agents(self, async_client: AsyncClient) -> None:
        """List registered agents."""
        response = await async_client.get("/v1/agents")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3  # Pre-registered demo agents

        agent_ids = {a["agent_id"] for a in data}
        assert "agent-coder" in agent_ids
        assert "agent-researcher" in agent_ids
        assert "agent-reviewer" in agent_ids


class TestGetTaskEndpoint:
    """Test GET /v1/tasks/{task_id} endpoint."""

    async def test_get_existing_task(self, async_client: AsyncClient) -> None:
        """Get existing task returns envelope."""
        # First dispatch a task
        envelope = TaskEnvelope(
            task_id=uuid4(),
            source_agent="orchestrator",
            target_agent="agent-coder",
        )
        dispatch_response = await async_client.post(
            "/v1/tasks",
            json=envelope.model_dump(mode="json"),
        )
        assert dispatch_response.status_code == 201

        task_id = dispatch_response.json()["task_id"]

        # Now get the task
        response = await async_client.get(f"/v1/tasks/{task_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == task_id
        assert data["status"] == "running"

    async def test_get_nonexistent_task_returns_404(self, async_client: AsyncClient) -> None:
        """Get non-existent task returns 404 with RFC 7807."""
        response = await async_client.get(f"/v1/tasks/{uuid4()}")

        assert response.status_code == 404
        data = response.json()
        assert data["type"] == "https://api.example.com/errors/task-not-found"
        assert data["title"] == "Task Not Found"
        assert data["status"] == 404


class TestHealthEndpoint:
    """Test GET /health endpoint."""

    async def test_health_check(self, async_client: AsyncClient) -> None:
        """Health check returns ok."""
        response = await async_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "agent-dispatcher"
