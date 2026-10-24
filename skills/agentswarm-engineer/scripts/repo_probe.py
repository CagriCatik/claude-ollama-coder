#!/usr/bin/env python3
"""Read-only AgentSwarm source inventory; no third-party imports or network calls.

Usage: python scripts/repo_probe.py --root /path/to/AgentSwarm [--json] [--strict]

The probe identifies code patterns, not runtime correctness. Review findings manually.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any


REQUIRED = (
    "pyproject.toml",
    "main.py",
    "backend/agents/coordinator/a2a_client.py",
    "backend/agents/coordinator/orchestrator.py",
    "backend/api/runner.py",
    "backend/common/config.py",
    "backend/mcp_server/server.py",
    "backend/adapters/mock_action_dispatcher.py",
    "frontend/src/store/workflowStore.ts",
)
AGENTS = ("analyst", "knowledge", "executor", "reviewer", "custom")


def read(root: Path, path: str) -> str:
    file = root / path
    try:
        return file.read_text(encoding="utf-8") if file.is_file() else ""
    except OSError:
        return ""


def inspect(root: Path) -> dict[str, Any]:
    root = root.expanduser().resolve()
    missing = [p for p in REQUIRED if not (root / p).is_file()]
    client = read(root, "backend/agents/coordinator/a2a_client.py")
    orchestrator = read(root, "backend/agents/coordinator/orchestrator.py")
    api_runner = read(root, "backend/api/runner.py")
    config = read(root, "backend/common/config.py")
    dispatcher = read(root, "backend/adapters/mock_action_dispatcher.py")
    audit = read(root, "backend/application/audit_service.py")
    knowledge = read(root, "backend/adapters/markdown_knowledge_repository.py")
    frontend = read(root, "frontend/src/store/workflowStore.ts")

    protocols: dict[str, Any] = {}
    for name in AGENTS:
        path = f"backend/agents/{name}/server.py"
        server = read(root, path)
        protocols[name] = {
            "path": path,
            "present": bool(server),
            "send_message_handler": bool(re.search(r'\bmethod\s*==\s*[\'\"]SendMessage[\'\"]', server)),
            "well_known_discovery_route": bool(re.search(r'Route\(\s*[\'\"]/\.well-known/agent-card\.json', server)),
        }

    has_coordinator_send_message = bool(re.search(r'[\'\"]method[\'\"]\s*:\s*[\'\"]SendMessage[\'\"]', client))
    execution_before_review = False
    for source in (orchestrator, api_runner):
        # Infer relevant order from call sites, not method definitions.
        exec_match = re.search(r'\b(?:self\.)?(?:orchestrator\.)?request_execution\s*\(', source)
        review_match = re.search(r'\b(?:self\.)?(?:orchestrator\.)?request_review\s*\(', source)
        if source == orchestrator:
            # Skip method definitions by considering the run() body only.
            source = source[source.find("    def run("):] if "    def run(" in source else source
            exec_match = re.search(r'\bself\.request_execution\s*\(', source)
            review_match = re.search(r'\bself\.request_review\s*\(', source)
        if exec_match and review_match and exec_match.start() < review_match.start():
            execution_before_review = True

    findings: list[dict[str, str]] = []

    def record(level: str, code: str, message: str) -> None:
        findings.append({"severity": level, "code": code, "message": message})

    if missing:
        record("BLOCKER", "missing-files", "Required files absent: " + ", ".join(missing))
    if has_coordinator_send_message:
        incompatible = [n for n, v in protocols.items() if not v["send_message_handler"]]
        if incompatible:
            record("HIGH", "sendmessage-mismatch", "Coordinator sends SendMessage but no matching handler detected: " + ", ".join(incompatible))
        no_cards = [n for n, v in protocols.items() if not v["well_known_discovery_route"]]
        if no_cards:
            record("HIGH", "discovery-mismatch", "Well-known Agent Card route not detected: " + ", ".join(no_cards))
    if execution_before_review:
        record("CRITICAL", "post-execution-review", "At least one orchestration path invokes execution before review")
    if "authorized\", True" in audit or 'authorized", True' in audit:
        record("HIGH", "permissive-auth-default", "Audit defaults authorization to True when absent")
    if 'signoff_approved", True' in audit:
        record("HIGH", "permissive-signoff-default", "Audit defaults sign-off to True when absent")
    if "MockActionDispatcher" in dispatcher:
        record("INFO", "mock-actions", "MockActionDispatcher present: simulated outcomes are not verified infrastructure mutations")
    if "duration * 0.5" in api_runner or "_duration * 0.5" in api_runner:
        record("MEDIUM", "synthetic-mcp-timing", "Runner derives MCP event duration from a fraction of agent timing")
    if "query_terms" in knowledge and "re.findall" in knowledge:
        record("INFO", "keyword-search", "Markdown knowledge search appears to score query terms, not embeddings")
    if 'OLLAMA_BASE_URL' not in config and 'OLLAMA_MODEL' not in config:
        record("MEDIUM", "ollama-env-not-mapped", "Configuration reader does not reference Docker Ollama env override names")
    if "INITIAL_NODES" in frontend:
        record("INFO", "static-ui-topology", "Frontend defines initial graph nodes independently of API topology")

    return {
        "repository_root": str(root),
        "required_files_present": len(REQUIRED) - len(missing),
        "required_files_total": len(REQUIRED),
        "a2a_protocol_handlers": protocols,
        "observations": findings,
        "disclaimer": "Static pattern scan only. Recheck relevant source and run tests; an absence of warnings is not proof of correctness.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="AgentSwarm repository root")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    parser.add_argument("--strict", action="store_true", help="Exit 2 for BLOCKER/CRITICAL/HIGH source findings")
    args = parser.parse_args()
    report = inspect(args.root)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"AgentSwarm static probe: {report['repository_root']}")
        print(f"Required files: {report['required_files_present']}/{report['required_files_total']}")
        for agent, details in report["a2a_protocol_handlers"].items():
            print(f"  {agent:9s} SendMessage={details['send_message_handler']} discovery={details['well_known_discovery_route']}")
        for item in report["observations"]:
            print(f"[{item['severity']}] {item['code']}: {item['message']}")
        print(report["disclaimer"])
    if args.strict and any(x["severity"] in ("BLOCKER", "CRITICAL", "HIGH") for x in report["observations"]):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
