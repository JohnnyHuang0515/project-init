---
name: security-review
description: Auto-invoked workflow for reviewing security-sensitive changes. Use when modifying authentication, authorization, input validation, cryptographic operations, session handling, file uploads, or any code that processes untrusted input. Also use when touching database queries (SQL injection), rendering user content (XSS), or external HTTP calls (SSRF).
---

# Security Review

A checklist-driven workflow for security-sensitive changes in {{PROJECT_NAME}}.

## When to invoke

This skill should trigger automatically when a diff touches:
- Authentication / login / session code
- Authorization / permission checks
- Anything that parses or executes user-supplied content
- SQL, NoSQL, or other query construction
- File uploads or file-system operations on user-controlled paths
- HTTP clients that take user-controlled URLs
- Cryptographic operations (hashing, signing, encrypting)
- Anywhere secrets or credentials are handled

## The review workflow

### 1. Identify the threat surface

For each changed file, ask:
- What untrusted input does this code see?
- What privileged action can this code take?
- What's the worst thing an attacker could achieve if they controlled the input?

### 2. Run the checklist

For each relevant category below, go through the checks. Flag anything that fails or is unclear.

**Input validation**
- [ ] All user input is validated against an allow-list (not just a deny-list) where possible.
- [ ] Length limits are enforced before any processing.
- [ ] Structured data (JSON, XML) is parsed with a safe parser, not regex.

**Injection**
- [ ] SQL uses parameterized queries or a safe ORM — no string concatenation.
- [ ] Shell commands use argument arrays, not string concatenation.
- [ ] Template rendering escapes by default; raw output is deliberate and reviewed.

**AuthN / AuthZ**
- [ ] Every privileged endpoint checks authentication.
- [ ] Authorization is checked *after* authentication and *before* action.
- [ ] Object-level permissions are verified (not just "is logged in").
- [ ] Passwords are hashed with a modern algorithm (argon2, bcrypt) — never MD5/SHA1.

**Secrets**
- [ ] No hard-coded credentials, API keys, or tokens.
- [ ] `.env` files are in `.gitignore`.
- [ ] Secrets are loaded from a secrets manager or env vars, not bundled.

**Output**
- [ ] HTML output escapes by default.
- [ ] JSON responses don't leak internal data (stack traces, DB schema).
- [ ] Errors shown to users don't reveal system details.

**File handling**
- [ ] User-supplied paths are normalized and checked against an allow-listed root.
- [ ] File uploads validate content type *and* content (not just extension).
- [ ] Downloaded files have a size limit.

**Network**
- [ ] Outbound HTTP from user-controlled URLs blocks internal IPs (SSRF protection).
- [ ] TLS is required for all external calls.
- [ ] Redirects are validated before following.

### 3. Report findings

Structure the report as:

```
## Security review of <change description>

### Findings

- 🔴 CRITICAL: <issue> in <file:line> — <why it matters> — <suggested fix>
- 🟡 WARNING: ...
- 🟢 NOTE: ...

### Verified safe

- Authentication check on line X uses the standard middleware — good.
- SQL query on line Y is parameterized — good.
```

If no issues found, say so explicitly. Don't pad the report.

### 4. What not to do

- Don't run potentially destructive security scans (penetration tests, fuzzers) without the user's explicit go-ahead.
- Don't auto-fix security issues silently — surface them, let the human decide.
- Don't assume context you don't have. If you're not sure whether a check is security-relevant, ask.
