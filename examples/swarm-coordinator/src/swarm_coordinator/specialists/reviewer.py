"""Reviewer specialist: safety and policy compliance."""

from __future__ import annotations

from swarm_coordinator.domain.models import ActionProposal, ReviewResult


class SafetyReviewer:
    async def review(self, proposal: ActionProposal, analysis: dict) -> ReviewResult:
        requirements_ok = bool(analysis.get("requirements_ok", False))
        risk_level = analysis.get("risk_level", "high")
        allowed_risk = {"low", "medium"}
        if not requirements_ok:
            return ReviewResult(passed=False, notes="Requirements not met.")
        if risk_level not in allowed_risk:
            return ReviewResult(passed=False, notes=f"Risk level {risk_level} not allowed.")
        if not proposal.action or not proposal.target:
            return ReviewResult(passed=False, notes="Proposal missing action or target.")
        return ReviewResult(passed=True, notes="Safety and policy checks passed.")