"""Agent card discovery model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AgentCard(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = "swarm-coordinator"
    description: str = "Micro-swarm coordinator with pre-execution audit gate"
    url: str = "http://localhost:8000"
    version: str = "0.1.0"
    protocolVersion: str = "0.3.0"
    capabilities: dict = Field(default_factory=lambda: {"streaming": True, "pushNotifications": False})
    defaultInputModes: list[str] = Field(default_factory=lambda: ["text"])
    defaultOutputModes: list[str] = Field(default_factory=lambda: ["text", "application/json"])
    skills: list[dict] = Field(default_factory=lambda: [{"name": "coordinate", "description": "Coordinate a run"}])