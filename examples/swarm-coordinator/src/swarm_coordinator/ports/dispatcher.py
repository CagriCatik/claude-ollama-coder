"""Abstract port for action dispatch."""

from __future__ import annotations

from typing import Protocol

from swarm_coordinator.domain.models import ActionProposal, ActionResult


class ActionDispatcherPort(Protocol):
    async def dispatch(self, proposal: ActionProposal) -> ActionResult:
        """Dispatch a proposal. Implementations declare simulation provenance."""
        ...