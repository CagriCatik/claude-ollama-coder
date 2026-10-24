import pytest

from swarm_coordinator.application.coordinator import SwarmCoordinator


@pytest.mark.asyncio
async def test_happy_path_simulated():
    coordinator = SwarmCoordinator()
    state = await coordinator.run("deploy service", {"risk_level": "low", "requirements_met": True})
    assert state.status.value == "finished"
    assert state.result is not None
    assert state.result.is_simulated is True
    assert state.result.status == "simulated"
    proposal = state.proposals[0]
    assert proposal.is_simulated is True
    assert proposal.status.value == "simulated"


@pytest.mark.asyncio
async def test_event_bus_optional():
    coordinator = SwarmCoordinator(event_bus=None)
    state = await coordinator.run("task", {"risk_level": "low"})
    assert state.status.value == "finished"