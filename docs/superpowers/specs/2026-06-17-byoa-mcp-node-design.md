# Design: byoa-mcp-node — Bring Your Own Auth MCP Server (Node.js)

**Date:** 2026-06-17  
**Status:** Approved

---

## Overview

A self-contained Node.js demo showing how to implement Scalekit's "Bring Your Own Auth" (BYOA) concept for MCP servers. The demo shows customers how to plug their existing login page into Scalekit's OAuth 2.1 layer without migrating users.

Reference docs: https://docs.scalekit.com/mcp/auth-methods/custom-auth/

---

## What This Demonstrates

In standard Scalekit MCP auth, Scalekit hosts the login UI. In BYOA, Scalekit redirects to **the customer's own login page**, the customer authenticates the user, then hands user details back to Scalekit via a backend SDK call. Scalekit issues the final MCP token.

This demo shows:
1. A working MCP server (same `greet_user` tool as `greeting-mcp-node`)
2. A custom login page (`GET /login`) that Scalekit redirects to
3. A login form submission handler (`POST /login/submit`) that calls `scalekit.auth.updateLoginUserDetails()` and redirects back to Scalekit

---

## Architecture

Single Express app, single port (default 3002). Three concerns:

| Concern | Routes | Auth required |
|---|---|---|
| MCP protocol | `POST /` | Yes — Scalekit token |
| Well-known metadata | `GET /.well-known/oauth-protected-resource` | No |
| Login page | `GET /login`, `POST /login/submit` | No |

Auth middleware skips `/.well-known*` and `/login*`. All other routes require a valid Bearer token validated via `scalekit.validateToken()`.

---

## Folder Structure

```
byoa-mcp-node/
├── src/
│   ├── main.ts                 # Express setup, route wiring
│   ├── config/
│   │   └── config.ts           # env var loading
│   ├── lib/
│   │   ├── auth.ts             # oauthProtectedResourceHandler
│   │   ├── middleware.ts       # Scalekit token validation middleware
│   │   ├── transport.ts        # MCP StreamableHTTP transport
│   │   ├── logger.ts           # winston logger
│   │   └── scalekit.ts         # shared Scalekit client singleton
│   ├── login/
│   │   ├── handler.ts          # GET /login + POST /login/submit
│   │   └── template.ts         # inline HTML string for login form
│   └── tools/
│       ├── index.ts            # tool registry + TOOLS map
│       └── greeting.ts         # greet_user tool registration
├── package.json
├── tsconfig.json
├── env.example
└── README.md
```

---

## Key Design Decisions

### Shared Scalekit client (`lib/scalekit.ts`)

One `Scalekit` instance initialized with `(SK_ENV_URL, SK_CLIENT_ID, SK_CLIENT_SECRET)` is exported and imported by both:
- `lib/middleware.ts` — calls `scalekit.validateToken()`
- `login/handler.ts` — calls `scalekit.auth.updateLoginUserDetails()`

### Login flow detail

```
Scalekit → GET /login?login_request_id=lri_xxx&state=xxx
         ↓
         Renders HTML form
         (login_request_id + state as hidden inputs)
         (SK_CONNECTION_ID embedded server-side — never exposed as editable field)

User submits → POST /login/submit
             { email, password, login_request_id, state }
         ↓
         Demo auth: any non-empty email + password accepted
         (comment in code explains real apps replace this with real auth)
         ↓
         scalekit.auth.updateLoginUserDetails(
           SK_CONNECTION_ID,
           login_request_id,
           { sub: email, email }
         )
         ↓
         On success → redirect to:
           {SK_ENV_URL}/sso/v1/connections/{SK_CONNECTION_ID}/partner:callback?state={state}
         On failure → re-render form with error message
```

### HTML login form (`login/template.ts`)

Inline TypeScript string template — no templating library, no static files. Returns a complete HTML page with:
- Email + password fields
- Hidden `login_request_id` and `state` fields
- Basic inline CSS (enough to look reasonable, not a UI showcase)
- Error message slot

### MCP server side

Identical to `greeting-mcp-node`:
- `greet_user` tool requiring `usr:read` scope
- Scope validation on `tools/call` requests
- WWW-Authenticate header on 401s

---

## Environment Variables

```env
PORT=3002
SK_ENV_URL=https://your-env.scalekit.dev
SK_CLIENT_ID=skc_xxx
SK_CLIENT_SECRET=sks_xxx
SK_CONNECTION_ID=conn_xxx          # Dashboard > MCP Servers > [server] > Advanced Configurations
MCP_SERVER_ID=res_xxx
PROTECTED_RESOURCE_METADATA='{...minified_json...}'
EXPECTED_AUDIENCE=http://localhost:3002/
```

`SK_CONNECTION_ID` is new relative to `greeting-mcp-node`. All others are the same.

---

## Error Handling

| Scenario | Behavior |
|---|---|
| Missing `login_request_id` or `state` in GET /login | 400 response |
| Empty email or password on form submit | Re-render form with validation error |
| `updateLoginUserDetails` SDK call fails | Re-render form with generic error; log full error server-side |
| Missing Bearer token on MCP route | 401 with WWW-Authenticate header |
| Invalid/expired token | 401 with WWW-Authenticate header |

---

## What Is Intentionally Simplified

- **No real password check** — demo auth accepts any non-empty email + password. Comment in `handler.ts` marks where real auth logic goes.
- **No session management** — login is stateless per request (login_request_id ties it together).
- **No CSRF protection** — demo only. Comment notes this for production.

---

## README Outline

1. What this demo shows (BYOA concept, one paragraph)
2. Prerequisites (Node 18+, Scalekit workspace)
3. Setup steps mirroring `greeting-mcp-node` README + new step for `SK_CONNECTION_ID`
4. How to find `SK_CONNECTION_ID` in the dashboard
5. Run + test instructions
6. Link to Scalekit BYOA docs
