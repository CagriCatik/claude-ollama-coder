---
name: software-engineering
description: Software engineering practices. Use when designing APIs or interfaces, deciding on module/package structure, planning error handling strategies, choosing between design patterns, writing production-quality code across multiple files, defining contracts between components, or when code organization decisions affect more than one file.
license: MIT
compatibility: Universal (Multi-file Codebases)
metadata:
  author: claude-ollama-coder
  version: "1.0.0"
---

# Software Engineering Practices

Practical engineering guidelines that sit above language syntax and below architectural patterns. These apply when your decisions affect the shape of code that other code (or people) will depend on.

---

## When to Use This Skill

- **Trigger Scenarios:**
  - When designing internal function or class interfaces spanning multiple files.
  - When structuring new packages, directory layouts, or module boundaries.
  - When deciding between object-oriented and functional design patterns (Strategy, Factory, Adapter, Repository).
  - When designing domain-specific error hierarchies and exception propagation.
  - When establishing test strategies across unit, integration, and end-to-end tiers.
  - When instrumenting structured logging, observability, and correlation IDs.

- **When NOT to Use:**
  - Do not use for system-wide macro architectural tradeoffs across independent services (use `software-architecture`).
  - Do not use for low-level language-specific syntax quirks (use language skills like `python-modern-practices`).

---

## API and Interface Design

**The interface is a contract.** Design it as if you can never change it — because in shared codebases, you often can't without coordination.

- **Minimal surface area**: expose only what callers need. Every public method is a commitment.
- **Stable inputs, stable outputs**: prefer value types and plain data structures over rich objects at boundaries — they're easier to test, serialize, and version.
- **Command-Query Separation**: a function either returns data (query) or causes a side effect (command). Mixing both surprises callers.
- **Fail at the boundary**: validate inputs at the entry point. Internal functions can trust their callers.
- **Avoid boolean trap**: `send(message, true)` — true what? Use named parameters, enums, or separate methods.

```python
# Unclear
def process(data, validate=True, async_mode=False): ...

# Clear
def process(data: Data) -> Result: ...
def process_async(data: Data) -> Awaitable[Result]: ...
def validate(data: Data) -> ValidationResult: ...
```

---

## Error Handling Philosophy

Errors are part of the design, not an afterthought.

- **Distinguish error categories**:
  - *Programming errors* (wrong input type, null where non-null expected): raise/assert immediately — these are bugs, not recoverable conditions.
  - *Expected domain errors* (file not found, timeout, validation failure): return typed results or raise domain-specific exceptions — callers should handle these.
  - *Infrastructure errors* (network down, disk full): propagate with context, let the outer layer decide recovery.

- **Carry context up the stack**: wrap exceptions with what you were trying to do, not just what failed.

```python
# Lose context
except IOError as e:
    raise RuntimeError("failed") from e

# Carry context
except IOError as e:
    raise ConfigLoadError(f"Could not load config from {path}") from e
```

- **Don't recover from errors you don't understand.** A broad `except Exception: pass` hides bugs. Catch what you know how to handle.
- **Error types are documentation.** A function that raises `UserNotFound`, `PermissionDenied`, and `DatabaseError` tells the caller exactly what to plan for.

---

## Module and Package Organization

Organize by domain, not by layer. `robot/` with its controller, driver, and tests is easier to navigate than `controllers/`, `drivers/`, `tests/` spread across the project.

```text
src/
├── robot/
│   ├── __init__.py
│   ├── controller.py    # domain logic
│   ├── driver.py        # hardware interface
│   └── test_controller.py
├── planning/
│   ├── __init__.py
│   ├── planner.py
│   └── test_planner.py
└── common/
    ├── types.py         # shared value types only
    └── logging.py
```

Rules:
- **No circular imports.** If A imports B and B imports A, one of them is doing too much.
- `common/` is for genuinely shared utilities — not a dumping ground. If only one module uses it, keep it there.
- Keep `__init__.py` thin — it's a public API declaration, not a place for logic.

---

## Design Patterns: When to Reach for Them

Patterns solve specific recurring problems. Name them when you use them — it communicates intent.

| Pattern | Reach for it when |
|---|---|
| Strategy | You have multiple interchangeable algorithms and want to swap them at runtime or per-config |
| Observer / Event | One thing happens and multiple independent parties need to react, without the producer knowing who |
| Factory | Construction logic is complex or the concrete type varies; callers shouldn't know the details |
| Adapter | You need to make an external interface fit your internal contracts |
| Decorator | You want to add behavior (logging, caching, retry) without modifying the original class |
| Repository | You want to decouple domain logic from data access — testable without a real database |

Don't apply patterns preemptively. Three similar cases before abstracting. One instance → just write it.

---

## Testing Strategy

Tests exist to let you change code confidently, not to achieve a coverage number.

- **Unit tests**: test a function's logic in isolation. Mock only I/O boundaries (network, disk, time) — not internal collaborators.
- **Integration tests**: test the wiring between components against real dependencies (real DB, real queue). These catch what mocks miss.
- **End-to-end tests**: test the system as a user would. Keep them few — they're slow and flaky. Cover the critical happy path only.

Structure tests by behavior, not by implementation:

```python
# Describes behavior (survives refactoring)
def test_planner_avoids_obstacles():

# Describes implementation (breaks on rename)
def test_planner_calls_get_path_with_correct_args():
```

- **Test the contract, not the internals.** If your test breaks when you rename a private method, it's testing the wrong thing.
- **Arrange-Act-Assert** in that order, one assertion per concept (multiple assertions on the same object are fine).
- A test that never fails teaches you nothing. Write the test before the code at least once to confirm it can fail.

---

## Observability

Code in production is a black box. Build the window in from the start.

- **Structured logging**: log events as key-value data, not formatted strings. Makes log aggregation and alerting possible.
- **Log at the right level**: DEBUG for traces (disabled in prod), INFO for state transitions, WARN for unexpected-but-handled, ERROR for failures requiring attention.
- **Correlation IDs**: thread a request ID through all log entries for a single operation — makes distributed tracing possible.
- **Metrics over logs for frequency**: if something happens 1000× per second, emit a metric counter — don't log every instance.

```python
# Unstructured — hard to query
logger.info(f"Processed request from {user} in {elapsed}ms")

# Structured — queryable
logger.info("request_processed", user_id=user.id, elapsed_ms=elapsed, status="ok")
```

---

## Dependency Management

- **Depend on abstractions, not concretions** — especially for I/O (file system, network, time). This makes testing and swapping implementations straightforward.
- **Inject dependencies, don't create them inside functions.** A function that calls `open()` or `requests.get()` directly is hard to test and inflexible. Pass the dependency in.
- **Keep dependency graphs shallow.** Deep chains (A → B → C → D) mean a change at D can ripple unpredictably to A.
- Pin dependency versions in production. `>=1.0` is fine for a library; it's risky for a deployed service.

---

## Self-Verification Checklist

Before concluding changes across packages and modules:
- [ ] Interface surfaces are minimal with command-query separation preserved.
- [ ] Exceptions preserve context using `raise DomainError(...) from original_error`.
- [ ] No circular imports across modules.
- [ ] Tests verify behavioral contracts rather than private implementation details.
- [ ] Dependencies are injected rather than hardcoded in function bodies.
- [ ] Structured logging emits queryable key-value pairs with correlation IDs where appropriate.
