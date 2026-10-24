"""Safe orchestration: propose -> analyze -> review/audit -> approve -> execute."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from swarm_coordinator.adapters.mock_dispatcher import MockActionDispatcher
from swarm_coordinator.application.audit_service import AuditService
from swarm_coordinator.domain.events import EventType, SwarmEvent, SwarmStatus
from swarm_coordinator.domain.models import (
    ActionProposal,
    RunState,
    Task,
)
from swarm_coordinator.specialists.analyst import AnalystAgent
from swarm_coordinator.specialists.executor import ExecutorAgent
from swarm_coordinator.specialists.reviewer import SafetyReviewer


class SwarmCoordinator:
    def __init__(
        self,
        analyst: AnalystAgent | None = None,
        reviewer: SafetyReviewer | None = None,
        executor: ExecutorAgent | None = None,
        audit_service: AuditService | None = None,
        event_bus: Any = None,
    ) -> None:
        self.analyst = analyst or AnalystAgent()
        self.reviewer = reviewer or SafetyReviewer()
        self.dispatcher = None
        if executor is None:
            self.dispatcher = MockActionDispatcher()
            self.executor = ExecutorAgent(self.dispatcher)
        else:
            self.executor = executor
        self.audit_service = audit_service or AuditService()
        self.event_bus = event_bus

    async def _publish(self, event: SwarmEvent) -> None:
        if self.event_bus is not None:
            await self.event_bus.publish(event)

    async def run(self, description: str, telemetry: dict | None = None) -> RunState:
        run_id = uuid4()
        telemetry = telemetry or {}
        task = Task(description=description, telemetry=telemetry)

        # component_started: coordinator
        await self._publish(
            SwarmEvent(event=EventType.COMPONENT_STARTED, run_id=run_id, data={"component": "coordinator"})
        )

        state = RunState(run_id=run_id, status=SwarmStatus.PROPOSED, task=task)

        proposal = ActionProposal(
            run_id=run_id,
            action="execute_task",
            target=description,
            parameters={"telemetry": telemetry},
            status=SwarmStatus.PROPOSED,
        )
        state = state.model_copy(update={"proposals": (proposal,)})

        # analyze
        state = state.model_copy(update={"status": SwarmStatus.ANALYZING})
        await self._publish(
            SwarmEvent(event=EventType.COMPONENT_STARTED, run_id=run_id, data={"component": "analyst"})
        )
        analysis = await self.analyst.analyze(task)
        state = state.model_copy(update={"analysis": analysis})

        # review
        await self._publish(
            SwarmEvent(event=EventType.COMPONENT_STARTED, run_id=run_id, data={"component": "reviewer"})
        )
        review = await self.reviewer.review(proposal, analysis)
        audit_record = self.audit_service.from_review(run_id, review)
        state = state.model_copy(
            update={
                "audit_records": (audit_record,),
                "status": SwarmStatus.REVIEWED,
            }
        )
        await self._publish(
            SwarmEvent(
                event=EventType.REVIEW_COMPLETED,
                run_id=run_id,
                data={"passed": review.passed, "notes": review.notes},
            )
        )

        # audit gate (fail-closed)
        approved = review.passed and self.audit_service.verify_approval(audit_record)
        if not approved:
            rejected_proposal = proposal.model_copy(update={"status": SwarmStatus.REJECTED})
            state = state.model_copy(
                update={
                    "proposals": (rejected_proposal,),
                    "status": SwarmStatus.REJECTED,
                    "finished_at": datetime.now(timezone.utc),
                }
            )
            await self._publish(
                SwarmEvent(event=EventType.RUN_FINISHED, run_id=run_id, data={"status": SwarmStatus.REJECTED.value})
            )
            return state

        # approved
        approved_proposal = proposal.model_copy(update={"status": SwarmStatus.APPROVED})
        state = state.model_copy(update={"proposals": (approved_proposal,), "status": SwarmStatus.APPROVED})

        # execute
        await self._publish(
            SwarmEvent(event=EventType.COMPONENT_STARTED, run_id=run_id, data={"component": "executor"})
        )
        result = await self.executor.execute(approved_proposal)
        # mark proposal status based on result
        if result.is_simulated:
            final_proposal_status = SwarmStatus.SIMULATED
        else:
            final_proposal_status = SwarmStatus.EXECUTED
        final_proposal = approved_proposal.model_copy(update={"status": final_proposal_status, "is_simulated": result.is_simulated})
        state = state.model_copy(
            update={
                "proposals": (final_proposal,),
                "result": result,
                "status": SwarmStatus(result.status) if result.status in [s.value for s in SwarmStatus] else state.status,
            }
        )
        await self._publish(
            SwarmEvent(
                event=EventType.EXECUTION_COMPLETED,
                run_id=run_id,
                data={"status": result.status, "is_simulated": result.is_simulated},
            )
        )

        state = state.model_copy(update={"status": SwarmStatus.FINISHED, "finished_at": datetime.now(timezone.utc)})
        await self._publish(
            SwarmEvent(event=EventType.RUN_FINISHED, run_id=run_id, data={"status": SwarmStatus.FINISHED.value})
        )
        return state