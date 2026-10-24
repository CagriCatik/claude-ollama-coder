# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Overview
`logsum` — a Python CLI that turns application log files into Markdown/JSON/HTML summaries. Used by test engineers to triage nightly test-bench logs.

## Commands
- Install (dev): `pip install -e ".[dev]"`
- Run: `logsum path/to/file.log [--json|--html] [--since 2026-01-01T00:00:00Z]`
- Tests: `pytest -q`
- Lint/format: `ruff check . && ruff format .`

## Architecture
- `src/logsum/parser.py` — line → `LogRecord` (pure, no I/O)
- `src/logsum/aggregate.py` — records → `Summary` dataclass
- `src/logsum/render/` — one module per output format
- `src/logsum/cli.py` — argument parsing only; no business logic
- Data flow: `cli → parser → aggregate → render`

## Conventions
- Python 3.11, type hints on all public functions
- Timestamps: ISO 8601, always UTC
- Errors: raise `LogsumError` subclasses; CLI converts them to exit code 2
- Commits: Conventional Commits (use `/commit-message`)

## Rules
- Standard library only for parsing; **ask before adding any dependency**
- Every new feature needs a pytest test in `tests/`
- Never edit files in `tests/fixtures/` — they are golden files
- Never read or print `.env`

## Gotchas
- Some bench logs are Latin-1 encoded: open with `errors="replace"`
- `tests/test_perf.py` is slow; skip locally with `-m "not slow"`
