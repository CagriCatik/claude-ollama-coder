import uuid
from unittest.mock import AsyncMock

import pytest

from swarm_coordinator.application.audit_service import AuditService
from swarm_coordinator.application.coordinator import SwarmCoordinator


@pytest.mark.asyncio
async def test_audit_defaults_block_execution():
    svc = AuditService()
    record = svc.create_record(uuid.uuid4())
    assert svc.verify_approval(record) is False


@pytest.mark.asyncio
async def test_review_fail_blocks_execution():
    coordinator = SwarmCoordinator()
    # force reviewer to fail
    coordinator.reviewer.review = AsyncMock(return_value=__import__("swarm_coordinator.domain.models", fromlist=["ReviewResult"]).ReviewResult(passed=False, notes="no"))
    # spy executor
    original_execute = coordinator.executor.execute
    called = {"n": 0}

    async def spy(proposal):
        called["n"] += 1
        return await original_execute(proposal)

    coordinator.executor.execute = spy

    state = await coordinator.run("danger", {"risk_level": "high", "requirements_met": False})
    assert state.status.value == "rejected"
    assert called["n"] == 0


@pytest.mark.asyncio
async def test_approval_denied_blocks_execution():
    from swarm_coordinator.domain.models import ReviewResult

    coordinator = SwarmCoordinator()
    coordinator.reviewer.review = AsyncMock(return_value=ReviewResult(passed=True, notes="ok"))
    # force audit to deny by overriding verify_approval
    coordinator.audit_service.verify_approval = lambda record: False
    called = {"n": 0}
    original_execute = coordinator.executor.execute

    async def spy(proposal):
        called["n"] += 1
        return await original_execute(proposal)

    coordinator.executor.execute = spy
    state = await coordinator.run("task", {"risk_level": "low", "requirements_met": True})
    assert state.status.value == "rejected"
    assert called["n"] == 0