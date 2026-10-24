"""Fail-closed audit authorization service."""

from __future__ import annotations

from swarm_coordinator.adapters.memory_audit import InMemoryAuditRepository
from swarm_coordinator.domain.models import AuditRecord, ReviewResult


class AuditService:
    def __init__(self, repository: InMemoryAuditRepository | None = None) -> None:
        self.repository = repository or InMemoryAuditRepository()

    def create_record(
        self,
        run_id,
        *,
        authorized: bool = False,
        signoff_approved: bool = False,
        reviewer_notes: str = "",
    ) -> AuditRecord:
        # Fail-closed: defaults remain False unless explicitly granted.
        record = AuditRecord(
            run_id=run_id,
            authorized=bool(authorized),
            signoff_approved=bool(signoff_approved),
            reviewer_notes=reviewer_notes,
        )
        self.repository.save(record)
        return record

    def from_review(self, run_id, review: ReviewResult) -> AuditRecord:
        authorized = bool(review.passed)
        # signoff is granted only when review passed (still requires verify_approval)
        signoff_approved = bool(review.passed)
        return self.create_record(
            run_id,
            authorized=authorized,
            signoff_approved=signoff_approved,
            reviewer_notes=review.notes,
        )

    def verify_approval(self, record: AuditRecord) -> bool:
        """Fail-closed: both flags must be True."""
        return bool(record.authorized) and bool(record.signoff_approved)

    def verify_approval_for_run(self, run_id) -> bool:
        record = self.repository.latest(run_id)
        if record is None:
            return False
        return self.verify_approval(record)