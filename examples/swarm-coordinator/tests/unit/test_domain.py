import pytest
from pydantic import ValidationError

from swarm_coordinator.domain.events import EventType, SwarmEvent, SwarmStatus
from swarm_coordinator.domain.models import (
    ActionProposal,
    AuditRecord,
    RunState,
    Task,
)


def test_task_requires_description():
    task = Task(description="hello")
    assert task.description == "hello"


def test_audit_record_defaults_fail_closed():
    import uuid

    record = AuditRecord(run_id=uuid.uuid4())
    assert record.authorized is False
    assert record.signoff_approved is False


def test_action_proposal_immutable():
    import uuid

    proposal = ActionProposal(run_id=uuid.uuid4(), action="a", target="t")
    with pytest.raises(ValidationError):
        proposal.status = SwarmStatus.APPROVED


def test_run_state_tuple_fields():
    import uuid

    task = Task(description="x")
    state = RunState(run_id=uuid.uuid4(), task=task)
    assert state.proposals == ()
    assert state.status == SwarmStatus.PROPOSED


def test_swarm_event_timestamp():
    import uuid

    ev = SwarmEvent(event=EventType.COMPONENT_STARTED, run_id=uuid.uuid4())
    assert ev.timestamp is not None