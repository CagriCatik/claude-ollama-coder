"""FastAPI routes for Agent Dispatcher."""

from uuid import UUID

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError as PydanticValidationError

from agent_dispatcher.models.envelope import TaskEnvelope
from agent_dispatcher.services.dispatcher import DispatchError, DispatcherService


class ProblemDetailException(Exception):
    """RFC 7807 Problem Details exception."""

    def __init__(
        self,
        *,
        type_: str,
        title: str,
        status: int,
        detail: str,
        instance: str | None = None,
    ) -> None:
        self.type = type_
        self.title = title
        self.status = status
        self.detail = detail
        self.instance = instance
        super().__init__(detail)


def create_problem_response(exc: ProblemDetailException) -> JSONResponse:
    """Create RFC 7807 Problem Details JSON response."""
    content = {
        "type": exc.type,
        "title": exc.title,
        "status": exc.status,
        "detail": exc.detail,
    }
    if exc.instance:
        content["instance"] = exc.instance
    return JSONResponse(content=content, status_code=exc.status)


app = FastAPI(
    title="Agent Dispatcher API",
    description="Agent-to-Agent Task Dispatcher Microservice",
    version="0.1.0",
)

# In-memory dispatcher service (single instance for the app)
dispatcher = DispatcherService()


# Pre-register some demo agents for testing
dispatcher.register_agent("agent-researcher", ["research", "analysis"])
dispatcher.register_agent("agent-coder", ["coding", "refactoring"])
dispatcher.register_agent("agent-reviewer", ["review", "testing"])


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle FastAPI request validation errors with RFC 7807 format."""
    errors = exc.errors()
    detail = "; ".join(f"{e['loc']}: {e['msg']}" for e in errors)
    return create_problem_response(
        ProblemDetailException(
            type_="https://api.example.com/errors/validation-error",
            title="Request Validation Failed",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            instance=str(request.url),
        )
    )


@app.exception_handler(PydanticValidationError)
async def pydantic_validation_exception_handler(
    request: Request, exc: PydanticValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors with RFC 7807 format."""
    errors = exc.errors()
    detail = "; ".join(f"{e['loc']}: {e['msg']}" for e in errors)
    return create_problem_response(
        ProblemDetailException(
            type_="https://api.example.com/errors/validation-error",
            title="Request Validation Failed",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            instance=str(request.url),
        )
    )


@app.exception_handler(DispatchError)
async def dispatch_exception_handler(request: Request, exc: DispatchError) -> JSONResponse:
    """Handle dispatch errors with RFC 7807 format."""
    return create_problem_response(
        ProblemDetailException(
            type_="https://api.example.com/errors/agent-not-found",
            title="Target Agent Not Found",
            status=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
            instance=str(request.url),
        )
    )


@app.exception_handler(ProblemDetailException)
async def problem_detail_exception_handler(
    request: Request, exc: ProblemDetailException
) -> JSONResponse:
    """Handle ProblemDetailException with RFC 7807 format."""
    return create_problem_response(exc)


@app.post(
    "/v1/tasks",
    response_model=TaskEnvelope,
    status_code=status.HTTP_201_CREATED,
    summary="Dispatch a task to a target agent",
    responses={
        201: {"description": "Task dispatched successfully"},
        404: {"description": "Target agent not registered"},
        422: {"description": "Invalid request payload"},
    },
)
async def dispatch_task(envelope: TaskEnvelope) -> TaskEnvelope:
    """
    Dispatch a task envelope to a registered worker agent.

    - Validates the envelope schema
    - Routes to the target agent if registered
    - Returns the envelope with updated status

    Returns 201 Created with the envelope on success.
    Returns RFC 7807 Problem Details on error.
    """
    result = dispatcher.dispatch(envelope)
    return result


@app.get("/v1/agents", summary="List registered agents")
async def list_agents() -> list[dict]:
    """List all registered worker agents."""
    agents = dispatcher.list_agents()
    return [
        {
            "agent_id": a.agent_id,
            "capabilities": a.capabilities,
            "registered_at": a.registered_at,
        }
        for a in agents
    ]


@app.get("/v1/tasks/{task_id}", summary="Get task status")
async def get_task(task_id: UUID) -> TaskEnvelope:
    """Get task envelope by ID."""
    task = dispatcher.get_task(task_id)
    if task is None:
        raise ProblemDetailException(
            type_="https://api.example.com/errors/task-not-found",
            title="Task Not Found",
            status=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
            instance=f"/v1/tasks/{task_id}",
        )
    return task


@app.get("/health", summary="Health check")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "service": "agent-dispatcher"}
