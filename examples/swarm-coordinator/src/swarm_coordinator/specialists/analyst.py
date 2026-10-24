"""Analyst specialist: evaluates telemetry and requirements."""

from __future__ import annotations

from swarm_coordinator.domain.models import Task


class AnalystAgent:
    async def analyze(self, task: Task) -> dict:
        telemetry = task.telemetry or {}
        requirements_ok = bool(telemetry.get("requirements_met", True))
        risk_level = telemetry.get("risk_level", "low")
        return {
            "task_id": str(task.task_id),
            "requirements_ok": requirements_ok,
            "risk_level": risk_level,
            "summary": f"Analysed task '{task.description}' with risk={risk_level}.",
        }