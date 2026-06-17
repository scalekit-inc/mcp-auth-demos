# BYOA MCP Server (Node.js)

A Node.js demo showing how to use Scalekit's **Bring Your Own Auth** (BYOA) for MCP servers.

Instead of Scalekit hosting the login UI, Scalekit redirects to your own login page. You authenticate the user, send their details to Scalekit via the SDK, and Scalekit issues the MCP access token. This means your existing users can access your MCP server without any migration.

See: [Scalekit BYOA docs](https://docs.scalekit.com/mcp/auth-methods/custom-auth/)

---

## How the BYOA flow works

```
MCP Client → Scalekit → GET /login?login_request_id=...&state=...
                         (your login page)
                               ↓
                         User submits credentials
                               ↓
                         POST user details to Scalekit SDK
                               ↓
                         Redirect → Scalekit callback
                               ↓
                         Scalekit issues MCP token
                               ↓
                         MCP Client calls tools with token
```

---

## Prerequisites

- Node.js v18+
- npm
- Access to [app.scalekit.com](https://app.scalekit.com) with a workspace

---

## Setup

### 1. Enable Full Stack Authentication

Go to [app.scalekit.com](https://app.scalekit.com) and enable **Full Stack Authentication** for your workspace.

### 2. Obtain API Credentials

Copy your **Environment URL**, **Client ID**, and **Client Secret** from Settings → API Credentials.

### 3. Set Up Permissions

Go to **Authorization** → **Permissions** and create:

- **Name:** `usr:read`
- **Description:** `Reading basic information of the users`

### 4. Register the MCP Server

Go to **MCP Servers** and register a new server:

- **Server Identifier:** `http://localhost:3002/` (trailing slash required)

After creation, copy:
- **MCP Server ID** (`res_xxx`)
- **Protected Resource Metadata** (JSON — minify it for the env var)

### 5. Configure the BYOA Connection

In the MCP server you just registered, open **Advanced Configurations** and find the **Connection ID** (`conn_xxx`).

Set the **User POST URL** to point at your login endpoint:
```
http://localhost:3002/login
```

### 6. Configure Environment Variables

```sh
cp env.example .env
```

Fill in `.env`:

```env
PORT=3002
SK_ENV_URL=https://your-env.scalekit.dev
SK_CLIENT_ID=skc_xxx
SK_CLIENT_SECRET=sks_xxx
SK_CONNECTION_ID=conn_xxx
MCP_SERVER_ID=res_xxx
PROTECTED_RESOURCE_METADATA='{"resource":"http://localhost:3002/",...}'
EXPECTED_AUDIENCE=http://localhost:3002/
```

`SK_CONNECTION_ID` is the connection ID from Advanced Configurations — starts with `conn_`, not `res_`.

### 7. Install and Build

```sh
npm install
npm run build
```

### 8. Run

```sh
npm start
```

Server starts on `http://localhost:3002`.

### 9. Connect with an MCP Client

Add to your `mcp.json`:

```json
{
  "servers": {
    "byoa-greeting": {
      "url": "http://localhost:3002/",
      "type": "http"
    }
  }
}
```

Click **Start**. The MCP client will trigger the OAuth flow, which redirects to `http://localhost:3002/login`.

### 10. Test the Login

When the login page appears, enter any email and password (this demo accepts any non-empty credentials). In a real app, replace the credential check in `src/login/handler.ts` with your actual auth logic.

After login, Scalekit completes the OAuth flow and your MCP client can call tools.

Try prompting:
> Can you please greet Alice?

---

## Project Structure

```
src/
├── main.ts               # Express app, route wiring
├── config/config.ts      # Environment variable loading
├── lib/
│   ├── scalekit.ts       # Shared Scalekit client (used by middleware + login handler)
│   ├── middleware.ts     # Token validation for MCP routes
│   ├── auth.ts           # /.well-known/oauth-protected-resource handler
│   ├── transport.ts      # MCP StreamableHTTP transport
│   └── logger.ts
├── login/
│   ├── handler.ts        # GET /login, POST /login/submit
│   └── template.ts       # Login page HTML
└── tools/
    ├── index.ts           # Tool registry
    └── greeting.ts        # greet_user tool
```

---

## Adapting for Production

| Location | What to change |
|---|---|
| `src/login/handler.ts` | Replace the mock auth check with your real credential validation |
| `src/login/handler.ts` | Pass richer user claims (`roles`, `custom_attributes`) to `updateLoginUserDetails` |
| `src/login/template.ts` | Replace with your actual login UI or redirect to it |

---

## License

See [LICENSE](../LICENSE).
