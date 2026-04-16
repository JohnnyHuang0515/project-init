# API conventions

Conventions for APIs exposed by this project — HTTP, RPC, CLI, or library. Claude should read this before designing or modifying public interfaces.

## HTTP / REST APIs

### URL structure

- Use **kebab-case** in paths: `/user-profiles/123`, not `/userProfiles/123` or `/user_profiles/123`.
- Resources are **plural nouns**: `/orders`, not `/order`.
- Nest at most one level deep: `/orders/{id}/items` is fine; `/users/{uid}/orders/{oid}/items/{iid}` is too much.
- Use query parameters for filtering, pagination, and sorting — not new endpoints.

### Methods

| Method | Use for |
|---|---|
| GET | Read. Must be safe and idempotent. |
| POST | Create, or any action that isn't a plain read/update/delete. |
| PUT | Full replacement. |
| PATCH | Partial update. |
| DELETE | Remove. Idempotent. |

### Status codes

- `200` — OK, response has a body.
- `201` — Created. Include a `Location` header.
- `204` — No content (for successful DELETE, etc.).
- `400` — Client error — malformed request, validation failure.
- `401` — Not authenticated.
- `403` — Authenticated but not authorized.
- `404` — Resource not found.
- `409` — Conflict (e.g., duplicate, or optimistic-lock failure).
- `422` — Semantic validation error (distinct from `400`'s syntactic error).
- `500` — Server error. Never lie; if it's our fault, admit it.

### Request/response bodies

- JSON by default. `Content-Type: application/json`.
- Use **camelCase** in JSON field names (matches most client languages).
- Wrap collections: `{ "items": [...], "nextCursor": "..." }` — don't return bare arrays.
- Include a stable `id` on every resource.
- Timestamps as ISO 8601 strings in UTC: `"2025-01-15T14:30:00Z"`.

### Errors

Error responses have a consistent shape:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Email is required",
    "field": "email",
    "requestId": "req_abc123"
  }
}
```

- `code` is a stable machine-readable constant — clients can switch on it.
- `message` is human-readable and safe to show end users.
- `requestId` lets support trace the failure in logs.

### Versioning

<!-- TODO: Decide on a strategy and document it. Options:
- URL versioning: `/v1/orders`
- Header versioning: `API-Version: 2024-10-01`
- No versioning, use additive changes only.
-->

## Backward compatibility

- **Never remove or rename a field in a response** without a migration path. Adding fields is safe; removing isn't.
- **New fields in requests must be optional** with sensible defaults.
- If you must break compatibility, ship a new version rather than modifying the old one.

## Authentication

<!-- TODO: Describe how auth works in this project. Examples:
- "Bearer tokens in the Authorization header"
- "Session cookies, SameSite=Lax"
- "mTLS for service-to-service"
-->

## Rate limiting

<!-- TODO: Describe rate-limit policy, or note that there isn't one. -->

## What not to do

- Don't put verbs in URLs (`/getUser`) — use nouns and HTTP methods.
- Don't return different shapes for the same endpoint based on query params.
- Don't leak internal errors (stack traces, SQL errors) to clients.
- Don't break backward compatibility without a versioning plan.
