"""Pure domain entities. No framework imports beyond Pydantic."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from swarm_coordinator.domain.events import SwarmStatus


class Task(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: UUID = Field(default_factory=uuid4)
    description: str
    telemetry: dict[str, Any] = Field(default_factory=dict)


class ActionProposal(BaseModel):
    model_config = ConfigDict(frozen=True)

    proposal_id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    action: str
    target: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    status: SwarmStatus = SwarmStatus.PROPOSED
    is_simulated: bool = False


class AuditRecord(BaseModel):
    """Fail-closed audit record: authorization defaults to denied."""

    model_config = ConfigDict(frozen=True)

    record_id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    authorized: bool = False
    signoff_approved: bool = False
    reviewer_notes: str = ""
    reviewed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReviewResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    passed: bool = False
    notes: str = ""


class ActionResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    action_id: UUID = Field(default_factory=uuid4)
    proposal_id: UUID
    status: str = "simulated"
    is_simulated: bool = True
    details: dict[str, Any] = Field(default_factory=dict)


class RunState(BaseModel):
    model_config = ConfigDict(frozen=True)

    run_id: UUID = Field(default_factory=uuid4)
    status: SwarmStatus = SwarmStatus.PROPOSED
    task: Task
    proposals: tuple[ActionProposal, ...] = Field(default_factory=tuple)
    audit_records: tuple[AuditRecord, ...] = Field(default_factory=tuple)
    result: ActionResult | None = None
    analysis: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime | None = None