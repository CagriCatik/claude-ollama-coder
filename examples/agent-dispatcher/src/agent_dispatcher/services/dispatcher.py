"""Dispatcher service for routing tasks to registered worker agents."""

from dataclasses import dataclass, field
from uuid import UUID

from agent_dispatcher.models.envelope import TaskEnvelope


class DispatchError(Exception):
    """Raised when task dispatch fails."""

    def __init__(self, message: str, envelope: TaskEnvelope | None = None) -> None:
        super().__init__(message)
        self.envelope = envelope


@dataclass(slots=True)
class AgentInfo:
    """Information about a registered worker agent."""

    agent_id: str
    capabilities: list[str] = field(default_factory=list)
    registered_at: str = ""


class DispatcherService:
    """
    In-memory dispatcher for routing tasks to registered agents.

    Maintains an agent registry and task store for status tracking.
    """

    def __init__(self) -> None:
        self._agents: dict[str, AgentInfo] = {}
        self._tasks: dict[UUID, TaskEnvelope] = {}

    def register_agent(self, agent_id: str, capabilities: list[str] | None = None) -> None:
        """
        Register a worker agent with the dispatcher.

        Args:
            agent_id: Unique identifier for the agent.
            capabilities: Optional list of capability strings.
        """
        from datetime import datetime, timezone

        if agent_id in self._agents:
            return  # Idempotent registration

        self._agents[agent_id] = AgentInfo(
            agent_id=agent_id,
            capabilities=capabilities or [],
            registered_at=datetime.now(timezone.utc).isoformat(),
        )

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent. Returns True if agent was registered."""
        return self._agents.pop(agent_id, None) is not None

    def get_agent(self, agent_id: str) -> AgentInfo | None:
        """Get agent info by ID."""
        return self._agents.get(agent_id)

    def list_agents(self) -> list[AgentInfo]:
        """List all registered agents."""
        return list(self._agents.values())

    def dispatch(self, envelope: TaskEnvelope) -> TaskEnvelope:
        """
        Dispatch a task envelope to the target agent.

        Updates task status to 'running' and stores for tracking.
        Returns updated envelope.

        Raises:
            DispatchError: If target agent is not registered.
        """
        if envelope.target_agent not in self._agents:
            failed_envelope = envelope.with_status("failed")
            self._tasks[envelope.task_id] = failed_envelope
            raise DispatchError(
                f"Target agent '{envelope.target_agent}' not registered",
                envelope=failed_envelope,
            )

        # Update status to running and store
        running_envelope = envelope.with_status("running")
        self._tasks[envelope.task_id] = running_envelope

        return running_envelope

    def complete_task(self, task_id: UUID, success: bool = True) -> TaskEnvelope | None:
        """
        Mark a task as completed or failed.

        Args:
            task_id: The task to update.
            success: True for completed, False for failed.

        Returns:
            Updated envelope if found, None otherwise.
        """
        envelope = self._tasks.get(task_id)
        if envelope is None:
            return None

        new_status = "completed" if success else "failed"
        updated = envelope.with_status(new_status)
        self._tasks[task_id] = updated
        return updated

    def get_task(self, task_id: UUID) -> TaskEnvelope | None:
        """Get task envelope by ID."""
        return self._tasks.get(task_id)

    def list_tasks(self) -> list[TaskEnvelope]:
        """List all tracked tasks."""
        return list(self._tasks.values())
