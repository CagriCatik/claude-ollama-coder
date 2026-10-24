"""Message Envelope model for Agent-to-Agent communication."""

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TaskEnvelope(BaseModel):
    """
    Structured message envelope for A2A task dispatch.

    Follows the agent-to-agent skill's envelope specification with
    task_id, source_agent, target_agent, payload, status, and created_at.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    task_id: Annotated[UUID, Field(description="Unique task identifier")]
    source_agent: Annotated[str, Field(min_length=1, description="Source agent identifier")]
    target_agent: Annotated[str, Field(min_length=1, description="Target agent identifier")]
    payload: Annotated[dict, Field(default_factory=dict, description="Task payload data")]
    status: Annotated[
        str,
        Field(
            default="pending",
            pattern="^(pending|running|completed|failed)$",
            description="Task execution status",
        ),
    ]
    created_at: Annotated[
        datetime,
        Field(
            default_factory=lambda: datetime.now(timezone.utc),
            description="Task creation timestamp (UTC)",
        ),
    ]

    def with_status(self, new_status: str) -> "TaskEnvelope":
        """Return a new envelope with updated status (immutable pattern)."""
        return self.model_copy(update={"status": new_status})
