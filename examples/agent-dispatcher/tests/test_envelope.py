"""Tests for TaskEnvelope model validation."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from agent_dispatcher.models.envelope import TaskEnvelope


class TestTaskEnvelopeValidation:
    """Test TaskEnvelope creation and validation."""

    def test_valid_envelope_all_fields(self) -> None:
        """Valid envelope with all fields provided."""
        task_id = uuid4()
        envelope = TaskEnvelope(
            task_id=task_id,
            source_agent="orchestrator",
            target_agent="worker-1",
            payload={"key": "value"},
            status="running",
        )

        assert envelope.task_id == task_id
        assert envelope.source_agent == "orchestrator"
        assert envelope.target_agent == "worker-1"
        assert envelope.payload == {"key": "value"}
        assert envelope.status == "running"
        assert envelope.created_at is not None

    def test_valid_envelope_with_defaults(self) -> None:
        """Valid envelope uses defaults for status and created_at."""
        envelope = TaskEnvelope(
            task_id=uuid4(),
            source_agent="source",
            target_agent="target",
        )

        assert envelope.status == "pending"
        assert envelope.payload == {}
        assert envelope.created_at is not None
        # created_at should be recent (within last minute)
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        diff = (now - envelope.created_at).total_seconds()
        assert diff < 60

    def test_envelope_immutable(self) -> None:
        """Envelope is frozen - cannot modify after creation."""
        envelope = TaskEnvelope(
            task_id=uuid4(),
            source_agent="source",
            target_agent="target",
        )

        with pytest.raises(ValidationError):
            envelope.status = "running"  # type: ignore[misc]

    def test_with_status_returns_new_envelope(self) -> None:
        """with_status returns new envelope with updated status."""
        envelope = TaskEnvelope(
            task_id=uuid4(),
            source_agent="source",
            target_agent="target",
            status="pending",
        )

        updated = envelope.with_status("running")

        assert updated.status == "running"
        assert envelope.status == "pending"  # Original unchanged
        assert updated.task_id == envelope.task_id

    @pytest.mark.parametrize("missing_field", ["task_id", "source_agent", "target_agent"])
    def test_missing_required_field_raises(self, missing_field: str) -> None:
        """Missing required fields raise ValidationError."""
        data = {
            "task_id": uuid4(),
            "source_agent": "source",
            "target_agent": "target",
        }
        del data[missing_field]

        with pytest.raises(ValidationError) as exc_info:
            TaskEnvelope(**data)

        errors = exc_info.value.errors()
        assert any(e["loc"] == (missing_field,) for e in errors)

    @pytest.mark.parametrize("empty_field", ["source_agent", "target_agent"])
    def test_empty_string_agent_raises(self, empty_field: str) -> None:
        """Empty agent strings are rejected (min_length=1)."""
        data = {
            "task_id": uuid4(),
            "source_agent": "source",
            "target_agent": "target",
        }
        data[empty_field] = ""

        with pytest.raises(ValidationError) as exc_info:
            TaskEnvelope(**data)

        errors = exc_info.value.errors()
        assert any(e["loc"] == (empty_field,) for e in errors)

    @pytest.mark.parametrize("invalid_status", ["invalid", "unknown", "done", ""])
    def test_invalid_status_raises(self, invalid_status: str) -> None:
        """Invalid status values are rejected by pattern."""
        with pytest.raises(ValidationError) as exc_info:
            TaskEnvelope(
                task_id=uuid4(),
                source_agent="source",
                target_agent="target",
                status=invalid_status,
            )

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("status",) for e in errors)

    @pytest.mark.parametrize("valid_status", ["pending", "running", "completed", "failed"])
    def test_valid_status_accepted(self, valid_status: str) -> None:
        """All valid status values are accepted."""
        envelope = TaskEnvelope(
            task_id=uuid4(),
            source_agent="source",
            target_agent="target",
            status=valid_status,
        )
        assert envelope.status == valid_status

    def test_extra_fields_forbidden(self) -> None:
        """Extra fields are rejected (extra='forbid')."""
        with pytest.raises(ValidationError) as exc_info:
            TaskEnvelope(
                task_id=uuid4(),
                source_agent="source",
                target_agent="target",
                extra_field="not allowed",
            )

        errors = exc_info.value.errors()
        assert any(e["type"] == "extra_forbidden" for e in errors)
