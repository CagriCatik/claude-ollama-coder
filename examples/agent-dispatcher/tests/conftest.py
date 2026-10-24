"""Pytest fixtures for Agent Dispatcher tests."""

from uuid import uuid4

import pytest

from agent_dispatcher.models.envelope import TaskEnvelope
from agent_dispatcher.services.dispatcher import DispatcherService


@pytest.fixture
def dispatcher() -> DispatcherService:
    """Fresh dispatcher instance for each test."""
    return DispatcherService()


@pytest.fixture
def registered_dispatcher(dispatcher: DispatcherService) -> DispatcherService:
    """Dispatcher with pre-registered test agents."""
    dispatcher.register_agent("agent-researcher", ["research", "analysis"])
    dispatcher.register_agent("agent-coder", ["coding", "refactoring"])
    return dispatcher


@pytest.fixture
def valid_envelope() -> TaskEnvelope:
    """A valid task envelope for testing."""
    return TaskEnvelope(
        task_id=uuid4(),
        source_agent="orchestrator",
        target_agent="agent-coder",
        payload={"action": "refactor", "file": "src/main.py"},
    )


@pytest.fixture
def valid_envelope_dict(valid_envelope: TaskEnvelope) -> dict:
    """Valid envelope as dict for API testing."""
    return valid_envelope.model_dump(mode="json")


@pytest.fixture(autouse=True)
def _reset_dispatcher_singleton() -> None:
    """Ensure clean state between tests (if using module-level singleton)."""
    # This fixture runs automatically for each test
    yield
    # Cleanup if needed
