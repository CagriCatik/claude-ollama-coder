---
name: python-modern-practices
description: Modern Python 3.10+ engineering standards and idioms. Use when writing Python code, defining type hints and generics, modeling structured data with Pydantic v2, configuring pyproject.toml, writing pytest fixtures and tests, or implementing asynchronous I/O.
license: MIT
compatibility: Python >= 3.10
metadata:
  author: claude-ollama-coder
  version: "1.0.0"
---

# Modern Python Best Practices (3.10+)

Modern idioms, typing patterns, and engineering standards for production Python applications.

---

## When to Use This Skill

- **Trigger Scenarios:**
  - When writing or refactoring Python files (`*.py`).
  - When configuring project packaging with `pyproject.toml` (hatchling, poetry, flit, ruff).
  - When defining type hints, generics, Protocols, or union types (`|`).
  - When modeling structured schemas or settings using Pydantic v2 (`BaseModel`, `Field`, `ConfigDict`).
  - When writing test suites with `pytest` (fixtures, parametrizations, mocks, `tmp_path`).
  - When writing asynchronous HTTP calls or concurrency with `httpx` and `asyncio`.

- **When NOT to Use:**
  - Do not use for legacy Python 2.x or Python <= 3.9 projects requiring legacy `typing` imports.
  - Do not use when writing non-Python languages (Bash, C++, Rust).

---

## 1. Modern Type Annotations (PEP 604 & Built-in Generics)

Do not import `Union`, `Optional`, `List`, or `Dict` from `typing`. Use Python 3.10+ native syntax:

```python
# Outdated
from typing import Optional, List, Dict, Union
def fetch_users(ids: List[int]) -> Optional[Dict[str, Union[str, int]]]: ...

# Modern (Python 3.10+)
def fetch_users(ids: list[int]) -> dict[str, str | int] | None: ...
```

### Advanced Typing: Protocols for Structural Subtyping
Use `Protocol` instead of abstract base classes when you only care about interface contracts (duck typing with static verification):

```python
from typing import Protocol

class ModelRunner(Protocol):
    def generate(self, prompt: str, temperature: float = 0.2) -> str: ...

# Any object with a matching generate() method satisfies this protocol
def execute_task(runner: ModelRunner, prompt: str) -> str:
    return runner.generate(prompt)
```

---

## 2. Structured Data Modeling with Pydantic v2

Pydantic v2 provides Rust-backed validation and serialization.

```python
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone

class SessionConfig(BaseModel):
    # Enforce immutable models when appropriate
    model_config = ConfigDict(frozen=True, extra="forbid")

    session_id: str
    model_name: str = Field(default="gpt-oss:20b-cloud")
    max_tokens: int = Field(default=4096, gt=0, le=131072)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def from_env(cls) -> "SessionConfig":
        import os
        return cls(
            session_id="default-session",
            model_name=os.getenv("CLAUDE_OLLAMA_MODEL", "gpt-oss:20b-cloud"),
        )
```

---

## 3. Asynchronous I/O with `httpx` & `asyncio`

Prefer `httpx` over `requests` for modern sync/async HTTP requests with connection pooling and timeouts:

```python
import httpx

async def query_ollama(prompt: str, model: str = "qwen2.5-coder:14b") -> str:
    # Always specify timeouts to prevent indefinite hanging
    timeout = httpx.Timeout(60.0, connect=10.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
        )
        response.raise_for_status()
        return response.json()["response"]
```

---

## 4. Testing with `pytest` Idioms

- **Use fixtures for setup and teardown**:
- **Parametrize test cases** to avoid code repetition:
- **Use `tmp_path` fixture** for filesystem tests:

```python
import pytest
from pathlib import Path

@pytest.fixture
def sample_modelfile(tmp_path: Path) -> Path:
    file = tmp_path / "Modelfile"
    file.write_text("FROM qwen2.5-coder:14b\nPARAMETER num_ctx 65536")
    return file

@pytest.mark.parametrize("temperature,expected_valid", [
    (0.2, True),
    (0.0, True),
    (1.5, False),
    (-0.1, False),
])
def test_temperature_validation(temperature: float, expected_valid: bool):
    is_valid = 0.0 <= temperature <= 1.0
    assert is_valid == expected_valid
```

---

## 5. Modern Project Standards (`pyproject.toml`)

Avoid `setup.py` or legacy `requirements.txt`-only package definitions for libraries. Use standard `pyproject.toml` with `ruff` for ultra-fast linting and formatting:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "claude-ollama-coder"
version = "1.0.0"
requires-python = ">=3.10"
dependencies = [
    "ollama>=0.4.0",
    "pydantic>=2.10.0",
    "httpx>=0.28.0",
]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
```

---

## Self-Verification Checklist

Before concluding Python coding tasks:
- [ ] Modern built-in type syntax used (`list[...]`, `dict[...]`, `X | None`); no legacy `typing.Optional` or `typing.Union`.
- [ ] Pydantic models leverage v2 conventions (`model_config = ConfigDict(...)`, `Field(...)`).
- [ ] Network requests via `httpx` or sockets include explicit timeout values.
- [ ] Tests authored in `pytest` style with fixtures and `@pytest.mark.parametrize`.
- [ ] No circular imports; imports organized and cleanly formatted (PEP 8 / ruff).
- [ ] Files and resources safely closed using context managers (`with` / `async with`).
