"""Domain events and status enums for the swarm coordinator."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SwarmStatus(str, Enum):
    """Lifecycle status for runs, proposals, and audit decisions."""

    PROPOSED = "proposed"
    ANALYZING = "analyzing"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"
    SIMULATED = "simulated"
    EXECUTED = "executed"
    FAILED = "failed"
    FINISHED = "finished"


class EventType(str, Enum):
    """Typed lifecycle events emitted on the SSE bus."""

    COMPONENT_STARTED = "component_started"
    REVIEW_COMPLETED = "review_completed"
    EXECUTION_COMPLETED = "execution_completed"
    RUN_FINISHED = "run_finished"


class SwarmEvent(BaseModel):
    """A single typed lifecycle event with timestamp and run id."""

    model_config = ConfigDict(frozen=True)

    event: EventType
    run_id: UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data: dict[str, Any] = Field(default_factory=dict)