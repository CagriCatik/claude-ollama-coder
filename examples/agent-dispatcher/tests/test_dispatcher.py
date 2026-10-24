"""Tests for DispatcherService."""

import contextlib
from uuid import uuid4

import pytest

from agent_dispatcher.models.envelope import TaskEnvelope
from agent_dispatcher.services.dispatcher import DispatchError, DispatcherService


class TestDispatcherService:
    """Test DispatcherService functionality."""

    def test_register_agent(self, dispatcher: DispatcherService) -> None:
        """Register agent adds to registry."""
        dispatcher.register_agent("test-agent", ["cap1", "cap2"])

        agent = dispatcher.get_agent("test-agent")
        assert agent is not None
        assert agent.agent_id == "test-agent"
        assert agent.capabilities == ["cap1", "cap2"]

    def test_register_agent_idempotent(self, dispatcher: DispatcherService) -> None:
        """Registering same agent twice is idempotent."""
        dispatcher.register_agent("test-agent", ["cap1"])
        dispatcher.register_agent("test-agent", ["cap2"])  # Different caps

        agent = dispatcher.get_agent("test-agent")
        assert agent.capabilities == ["cap1"]  # Original preserved

    def test_unregister_agent(self, dispatcher: DispatcherService) -> None:
        """Unregister removes agent from registry."""
        dispatcher.register_agent("test-agent")
        assert dispatcher.unregister_agent("test-agent") is True
        assert dispatcher.get_agent("test-agent") is None
        assert dispatcher.unregister_agent("test-agent") is False  # Not found

    def test_list_agents(self, dispatcher: DispatcherService) -> None:
        """List all registered agents."""
        dispatcher.register_agent("agent-1", ["cap1"])
        dispatcher.register_agent("agent-2", ["cap2"])

        agents = dispatcher.list_agents()
        assert len(agents) == 2
        assert {a.agent_id for a in agents} == {"agent-1", "agent-2"}

    def test_dispatch_to_registered_agent(
        self, registered_dispatcher: DispatcherService, valid_envelope: TaskEnvelope
    ) -> None:
        """Dispatch to registered agent updates status to running."""
        result = registered_dispatcher.dispatch(valid_envelope)

        assert result.status == "running"
        assert result.task_id == valid_envelope.task_id
        assert result.source_agent == valid_envelope.source_agent
        assert result.target_agent == valid_envelope.target_agent

        # Task stored in tracker
        stored = registered_dispatcher.get_task(valid_envelope.task_id)
        assert stored is not None
        assert stored.status == "running"

    def test_dispatch_to_unknown_agent_raises(
        self, dispatcher: DispatcherService, valid_envelope: TaskEnvelope
    ) -> None:
        """Dispatch to unknown agent raises DispatchError."""
        # valid_envelope targets "agent-coder" which is not registered in bare dispatcher
        with pytest.raises(DispatchError) as exc_info:
            dispatcher.dispatch(valid_envelope)

        assert "not registered" in str(exc_info.value)
        assert exc_info.value.envelope is not None
        assert exc_info.value.envelope.status == "failed"

    def test_dispatch_stores_failed_envelope_on_unknown_agent(
        self, dispatcher: DispatcherService, valid_envelope: TaskEnvelope
    ) -> None:
        """Failed dispatch still stores envelope with failed status."""
        with contextlib.suppress(DispatchError):
            dispatcher.dispatch(valid_envelope)

        stored = dispatcher.get_task(valid_envelope.task_id)
        assert stored is not None
        assert stored.status == "failed"

    def test_complete_task_success(self, registered_dispatcher: DispatcherService) -> None:
        """Mark task as completed."""
        envelope = TaskEnvelope(
            task_id=uuid4(),
            source_agent="orchestrator",
            target_agent="agent-coder",
        )
        registered_dispatcher.dispatch(envelope)

        updated = registered_dispatcher.complete_task(envelope.task_id, success=True)

        assert updated is not None
        assert updated.status == "completed"

    def test_complete_task_failure(self, registered_dispatcher: DispatcherService) -> None:
        """Mark task as failed."""
        envelope = TaskEnvelope(
            task_id=uuid4(),
            source_agent="orchestrator",
            target_agent="agent-coder",
        )
        registered_dispatcher.dispatch(envelope)

        updated = registered_dispatcher.complete_task(envelope.task_id, success=False)

        assert updated is not None
        assert updated.status == "failed"

    def test_complete_nonexistent_task_returns_none(self, dispatcher: DispatcherService) -> None:
        """Complete non-existent task returns None."""
        result = dispatcher.complete_task(uuid4())
        assert result is None

    def test_get_task(self, registered_dispatcher: DispatcherService) -> None:
        """Get task by ID."""
        envelope = TaskEnvelope(
            task_id=uuid4(),
            source_agent="orchestrator",
            target_agent="agent-coder",
        )
        registered_dispatcher.dispatch(envelope)

        task = registered_dispatcher.get_task(envelope.task_id)
        assert task is not None
        assert task.task_id == envelope.task_id

    def test_get_nonexistent_task_returns_none(self, dispatcher: DispatcherService) -> None:
        """Get non-existent task returns None."""
        assert dispatcher.get_task(uuid4()) is None

    def test_list_tasks(self, registered_dispatcher: DispatcherService) -> None:
        """List all tracked tasks."""
        for _i in range(3):
            envelope = TaskEnvelope(
                task_id=uuid4(),
                source_agent="orchestrator",
                target_agent="agent-coder",
            )
            registered_dispatcher.dispatch(envelope)

        tasks = registered_dispatcher.list_tasks()
        assert len(tasks) == 3
