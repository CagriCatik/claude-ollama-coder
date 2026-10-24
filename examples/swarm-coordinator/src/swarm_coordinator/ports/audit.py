"""Abstract port for audit repository."""

from __future__ import annotations

from typing import Protocol

from swarm_coordinator.domain.models import AuditRecord


class AuditRepositoryPort(Protocol):
    def save(self, record: AuditRecord) -> None: ...
    def get(self, run_id) -> list[AuditRecord]: ...
    def latest(self, run_id) -> AuditRecord | None: ...