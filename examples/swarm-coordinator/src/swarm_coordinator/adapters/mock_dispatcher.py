"""Explicitly simulated action dispatcher. Never claims production mutation."""

from __future__ import annotations

from swarm_coordinator.domain.models import ActionProposal, ActionResult


class MockActionDispatcher:
    """Simulated dispatcher. All results are stamped is_simulated=True."""

    async def dispatch(self, proposal: ActionProposal) -> ActionResult:
        return ActionResult(
            proposal_id=proposal.proposal_id,
            status="simulated",
            is_simulated=True,
            details={
                "adapter": "MockActionDispatcher",
                "note": "No infrastructure mutation performed; result is simulated.",
                "action": proposal.action,
                "target": proposal.target,
            },
        )