---
name: secure-coding
description: Security guidelines and vulnerability prevention. Use when handling sensitive data, parsing untrusted user input, running shell or subprocess commands, working with authentication or authorization tokens, reading/writing local files from user parameters, or auditing code for security risks.
license: MIT
compatibility: Universal (Python, Bash, Node.js)
metadata:
  author: claude-ollama-coder
  version: "1.0.0"
---

# Secure Coding Practices & Vulnerability Prevention

Actionable rules to prevent security vulnerabilities during code generation and review.

---

## When to Use This Skill

- **Trigger Scenarios:**
  - When invoking subprocesses, terminal commands, or shell scripts with dynamic arguments.
  - When handling user-supplied filenames, paths, or archive extractions.
  - When managing secrets, API keys, credentials, or session tokens.
  - When parsing or deserializing untrusted payloads (JSON, YAML, pickled objects).
  - When auditing codebases for OWASP Top 10 vulnerabilities (Injection, Broken Access Control, SSRF).

- **When NOT to Use:**
  - Do not use for cosmetic styling or pure algorithmic optimization where security surfaces are absent.

---

## 1. Safe Command Execution (Injection Defense)

Never pass unsanitized input to a shell.

```python
# VULNERABLE: Shell injection risk
import subprocess
subprocess.run(f"grep {pattern} {filename}", shell=True)

# SECURE: Argument array without shell=True
import subprocess
subprocess.run(["grep", "--", pattern, filename], shell=False, check=True)
```

### Command Execution Rules
- Always use list/array argument format: `["tool", "arg1", "arg2"]`.
- Set `shell=False` explicitly.
- Use `--` delimiter before arguments to prevent option injection attacks.
- Validate inputs against strict allowlists (e.g., regex `^[a-zA-Z0-9_-]+$`) before processing.

---

## 2. Path Traversal Defense

Never trust user-supplied filenames or relative path components.

```python
import os
from pathlib import Path

BASE_DIR = Path("/app/storage/uploads").resolve()

# VULNERABLE: Path traversal attack (e.g. filename = "../../etc/passwd")
def get_file_bad(filename: str):
    return open(BASE_DIR / filename, "rb").read()

# SECURE: Canonical resolution and boundary enforcement
def get_file_secure(filename: str) -> bytes:
    # Strip path separators from user input
    safe_name = os.path.basename(filename)
    target_path = (BASE_DIR / safe_name).resolve()

    # Ensure resolved path remains strictly inside BASE_DIR
    if not target_path.is_relative_to(BASE_DIR):
        raise ValueError("Access denied: path traversal attempt detected.")

    return target_path.read_bytes()
```

---

## 3. Secret & Credential Protection

- **Zero hardcoded credentials**: Never embed API keys, database passwords, or JWT secrets in code or git repositories.
- **Environment variables**: Use `.env` or system environment variables with typed loading (`pydantic-settings` or `python-dotenv`).
- **Secret masking in logs**: Ensure logging formatters sanitize authorization headers and token payloads.

```python
# SECURE: Secret masking in error outputs
def mask_secret(secret: str) -> str:
    if len(secret) <= 8:
        return "***"
    return f"{secret[:4]}...{secret[-4:]}"
```

---

## 4. Input Validation & Deserialization

- **Reject invalid data early**: Validate inputs at the system perimeter before invoking business logic.
- **Never use `eval()` or unvalidated `pickle`**: `pickle.loads()` can execute arbitrary code. Use `json` or `msgpack`.
- **Enforce schemas with Pydantic v2**:

```python
from pydantic import BaseModel, Field, EmailStr

class UserRegistration(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    age: int = Field(ge=13, le=120)
```

---

## Self-Verification Checklist

Before concluding your security audit or code edits:
- [ ] Subprocess invocations explicitly set `shell=False` and pass arguments as lists.
- [ ] File paths validated with `Path.resolve().is_relative_to(base_dir)`.
- [ ] No API keys, credentials, or private keys committed in source or print statements.
- [ ] Sensitive tokens masked in logging outputs (`mask_secret()`).
- [ ] Untrusted inputs validated against strict schemas before deserialization.
- [ ] Network requests enforce timeout bounds to mitigate Denial of Service (DoS).
