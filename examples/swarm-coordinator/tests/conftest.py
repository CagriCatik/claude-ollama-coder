"""Pytest fixtures."""

import pytest

from swarm_coordinator.api.routes import _event_bus, _run_store


@pytest.fixture(autouse=True)
def _reset_state():
    _run_store.clear()
    # recreate event bus queues by clearing history
    _event_bus._queues.clear()
    _event_bus._history.clear()
    yield