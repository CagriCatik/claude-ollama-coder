"""A2A JSON-RPC 2.0 models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class JsonRpcRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    jsonrpc: str = "2.0"
    id: Any = None
    method: str
    params: dict[str, Any] = Field(default_factory=dict)


class JsonRpcResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    jsonrpc: str = "2.0"
    id: Any = None
    result: Any = None
    error: Any = None


class MessagePart(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str = ""


class A2AMessage(BaseModel):
    model_config = ConfigDict(frozen=True)

    parts: list[MessagePart] = Field(default_factory=list)


class SendMessageParams(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    message: A2AMessage | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)