---
name: api-design
description: REST and HTTP API design standards. Use when designing API endpoints, choosing HTTP methods and status codes, writing OpenAPI/Swagger schemas, structuring RFC 7807 error responses, planning pagination strategies (cursor vs offset), or implementing idempotency.
license: MIT
compatibility: Universal HTTP/REST Web APIs
metadata:
  author: claude-ollama-coder
  version: "1.0.0"
---

# API Design Standards & Best Practices

Pragmatic rules for designing resilient, developer-friendly REST and HTTP APIs.

---

## When to Use This Skill

- **Trigger Scenarios:**
  - When designing new API endpoints, routes, or resources (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
  - When authoring or revising OpenAPI/Swagger definitions or JSON schema payloads.
  - When standardizing HTTP status codes and error payloads across services.
  - When choosing or implementing pagination mechanisms (cursor-based for infinite feeds vs offset-based for admin tables).
  - When designing mutating endpoints requiring `Idempotency-Key` headers.

- **When NOT to Use:**
  - Do not use for low-level socket programming or non-HTTP protocols (e.g. raw UDP, ROS2 DDS, WebRTC).
  - Do not use when working exclusively on internal system architecture without an exposed API surface (use `software-architecture`).

---

## 1. Resource-Oriented URL Naming

URLs identify resources (nouns), while HTTP verbs define actions.

```text
# GOOD: Nouns in plural, clear hierarchy
GET    /api/v1/sessions
POST   /api/v1/sessions
GET    /api/v1/sessions/{session_id}
DELETE /api/v1/sessions/{session_id}
GET    /api/v1/sessions/{session_id}/messages

# BAD: Verbs in URL, inconsistent plurals
POST   /api/createSession
GET    /api/session/get/{id}
POST   /api/delete_session
```

---

## 2. Standardized Error Handling (RFC 7807 Problem Details)

Never return arbitrary strings or ad-hoc error formats. Use the standardized RFC 7807 `application/problem+json` structure:

```json
{
  "type": "https://api.example.com/errors/model-unavailable",
  "title": "Local Model Unavailable",
  "status": 503,
  "detail": "Model 'qwen2.5-coder:14b' is not responding on Ollama port 11434.",
  "instance": "/api/v1/sessions/sess_9921/infer",
  "invalid_params": []
}
```

### HTTP Status Code Fast Guide
| Code | Meaning | Use Case |
|---|---|---|
| `200 OK` | Success with payload | Successful `GET`, `PUT`, or action `POST` |
| `201 Created` | Resource created | Successful `POST` creating a resource (include `Location` header) |
| `204 No Content` | Success without payload | Successful `DELETE` or state change |
| `400 Bad Request` | Malformed syntax / schema error | Invalid JSON, missing required fields |
| `401 Unauthorized` | Missing / invalid authentication | No token or expired API key |
| `403 Forbidden` | Authenticated but unauthorized | User has no permission for this resource |
| `404 Not Found` | Resource does not exist | Invalid ID or non-existent endpoint |
| `409 Conflict` | State conflict | Duplicate unique key, version mismatch |
| `422 Unprocessable` | Semantic validation failure | Syntactically valid JSON, but business rule failed |
| `429 Too Many Requests` | Rate limit exceeded | Include `Retry-After` header |
| `500 Server Error` | Unhandled internal exception | Mask stack traces in production |

---

## 3. Pagination: Cursor vs Offset

| Type | Best For | Implementation |
|---|---|---|
| **Cursor-based** | High-velocity data, infinite scroll, real-time feeds | `GET /messages?cursor=msg_982&limit=50` (returns `next_cursor`) |
| **Offset-based** | Administrative tables, direct page jump | `GET /users?page=3&per_page=20` (returns `total_count`) |

### Cursor Response Format
```json
{
  "data": [ ... ],
  "pagination": {
    "has_more": true,
    "next_cursor": "eyJpZCI6MTA5M30="
  }
}
```

---

## 4. Idempotency for Modifying Actions

For sensitive operations like executing agent steps or billing, support the `Idempotency-Key` HTTP header:

- Client sends a unique UUID: `Idempotency-Key: 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d`.
- Server caches response for 24 hours.
- If repeated request arrives with identical key, return cached response with `X-Cache: HIT`.

---

## 5. Backward Compatibility & Evolution

- **Additive changes are safe**: Adding optional request fields or new response fields does not break clients.
- **Breaking changes require versioning**: Changing data types, renaming fields, or removing endpoints requires URL version prefixing (e.g. `/api/v2/...`).
- **Tolerant Reader pattern**: Clients must ignore unrecognized JSON fields.

---

## Self-Verification Checklist

Before concluding changes to API endpoints or schemas:
- [ ] URL paths use plural nouns and avoid embedded action verbs (`/items`, not `/getItems`).
- [ ] Errors conform to RFC 7807 (`application/problem+json`) with HTTP status codes matching error semantics.
- [ ] Appropriate HTTP status codes used (`201` for creation with `Location`, `204` for deletions).
- [ ] Pagination strategy is defined (cursor-based for feeds, offset-based for indexed sets).
- [ ] Mutating endpoints (POST, PATCH) support or evaluate `Idempotency-Key` headers where duplicate execution is harmful.
- [ ] Tolerant reader conventions followed and breaking changes versioned with URL prefixes (`/v1/`, `/v2/`).
