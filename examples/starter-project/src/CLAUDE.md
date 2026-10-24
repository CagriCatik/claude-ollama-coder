# src/ — additional rules

- Keep modules under ~300 lines; split by responsibility.
- `parser.py` and `aggregate.py` must stay free of I/O so they're easy to test.
- New output formats go in `render/<format>.py` and register in `render/__init__.py`.
