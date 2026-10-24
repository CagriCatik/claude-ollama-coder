"""Execution boundary: delegates to a dispatcher port."""

from __future__ import annotations

from swarm_coordinator.domain.models import ActionProposal, ActionResult
from swarm_coordinator.ports.dispatcher import ActionDispatcherPort


class ExecutorAgent:
    def __init__(self, dispatcher: ActionDispatcherPort) -> None:
        self.dispatcher = dispatcher

    async def execute(self, proposal: ActionProposal) -> ActionResult:
        return await self.dispatcher.dispatch(proposal)