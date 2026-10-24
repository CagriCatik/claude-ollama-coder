"""In-memory, thread-safe audit store."""

from __future__ import annotations

import threading
from collections import defaultdict

from swarm_coordinator.domain.models import AuditRecord


class InMemoryAuditRepository:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._records: defaultdict = defaultdict(list)

    def save(self, record: AuditRecord) -> None:
        with self._lock:
            self._records[record.run_id].append(record)

    def get(self, run_id) -> list[AuditRecord]:
        with self._lock:
            return list(self._records[run_id])

    def latest(self, run_id) -> AuditRecord | None:
        with self._lock:
            records = self._records[run_id]
            return records[-1] if records else None