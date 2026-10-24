# Agent Dispatcher — A2A Task Dispatcher Microservice

A clean, modern Python microservice for Agent-to-Agent (A2A) task dispatch following structured envelope patterns.

## Features

- **Structured Message Envelopes**: Pydantic v2 models with validation for task_id, source/target agents, payload, status, timestamps
- **Agent Registry**: In-memory registration and discovery of worker agents with capabilities
- **Task Dispatch**: Route tasks to registered agents with status tracking (pending → running → completed/failed)
- **FastAPI REST API**: `POST /v1/tasks` for dispatch, `GET /v1/tasks/{id}` for status, `GET /v1/agents` for registry
- **RFC 7807 Error Handling**: Standardized problem details for all error responses
- **Comprehensive Tests**: Pytest suite covering envelope validation, dispatcher logic, and API endpoints

## Quick Start

### Installation

```bash
cd examples/agent-dispatcher
pip install -e ".[dev]"
```

### Running the Server

```bash
# From the src directory
uvicorn agent_dispatcher.api.routes:app --reload
```

Server starts at `http://localhost:8000`

### Running Tests

```bash
pytest tests/ -v
```

## API Reference

### Dispatch a Task

```http
POST /v1/tasks
Content-Type: application/json

{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "source_agent": "orchestrator",
  "target_agent": "agent-coder",
  "payload": {"action": "refactor", "file": "src/main.py"},
  "status": "pending"
}
```

**Response (201 Created):**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "source_agent": "orchestrator",
  "target_agent": "agent-coder",
  "payload": {"action": "refactor", "file": "src/main.py"},
  "status": "running",
  "created_at": "2026-01-15T10:30:00Z"
}
```

### List Registered Agents

```http
GET /v1/agents
```

### Get Task Status

```http
GET /v1/tasks/{task_id}
```

### Health Check

```http
GET /health
```

## Error Responses (RFC 7807)

All errors follow RFC 7807 Problem Details format:

```json
{
  "type": "https://api.example.com/errors/agent-not-found",
  "title": "Target Agent Not Found",
  "status": 404,
  "detail": "Target agent 'unknown-agent' not registered",
  "instance": "/v1/tasks"
}
```

## Architecture

```
src/agent_dispatcher/
├── models/envelope.py      # TaskEnvelope Pydantic model
├── services/dispatcher.py  # DispatcherService with agent registry
└── api/routes.py           # FastAPI endpoints
```

## Design Principles

- **Modern Python**: 3.10+ syntax, Pydantic v2, type hints throughout
- **Immutability**: Frozen Pydantic models, functional updates via `with_status()`
- **Standards Compliance**: RFC 7807 errors, RESTful endpoints, OpenAPI-ready
- **Testability**: Pure functions, dependency injection, comprehensive test coverage
- **A2A Alignment**: Envelope follows agent-to-agent skill specification

## Pre-registered Demo Agents

The service starts with three demo agents:
- `agent-researcher` — capabilities: research, analysis
- `agent-coder` — capabilities: coding, refactoring
- `agent-reviewer` — capabilities: review, testing

Register custom agents via `DispatcherService.register_agent()`.