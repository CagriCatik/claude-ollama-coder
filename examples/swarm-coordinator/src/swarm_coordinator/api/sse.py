"""SSE event bus and streaming helpers."""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator

from swarm_coordinator.domain.events import SwarmEvent


class EventBus:
    def __init__(self) -> None:
        self._queues: dict = {}
        self._history: dict = {}
        self._lock = asyncio.Lock()

    async def publish(self, event: SwarmEvent) -> None:
        async with self._lock:
            self._history.setdefault(event.run_id, []).append(event)
            queues = list(self._queues.get(event.run_id, []))
        for q in queues:
            await q.put(event)

    async def subscribe(self, run_id) -> AsyncGenerator[SwarmEvent, None]:
        queue: asyncio.Queue = asyncio.Queue()
        async with self._lock:
            self._queues.setdefault(run_id, []).append(queue)
            history = list(self._history.get(run_id, []))
        for ev in history:
            yield ev
        try:
            while True:
                event = await queue.get()
                yield event
        finally:
            async with self._lock:
                if run_id in self._queues:
                    self._queues[run_id] = [q for q in self._queues[run_id] if q is not queue]


async def format_sse(event: SwarmEvent) -> str:
    payload = event.model_dump(mode="json")
    return f"event: {event.event.value}\ndata: {json.dumps(payload)}\n\n"