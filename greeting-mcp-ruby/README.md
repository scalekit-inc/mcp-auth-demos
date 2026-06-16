# Scalekit MCP Server — Ruby on Rails

A Ruby on Rails sample showing how to protect an [MCP](https://modelcontextprotocol.io) server with [Scalekit](https://scalekit.com) OAuth 2.1.

MCP clients (Claude Desktop, MCPJam, etc.) authenticate via Scalekit before they can call any tool. The server validates the Bearer token on every request using Scalekit's JWKS endpoint — no client secret needed.

## Prerequisites

- Ruby 3.2+
- Bundler
- A [Scalekit](https://scalekit.com) account

## Setup

### 1. Scalekit dashboard

1. Create an **MCP Server** resource in your Scalekit environment
2. Set the **Server URL** to `http://localhost:3001` (or your deployed URL)
3. Enable **Dynamic Client Registration (DCR)**
4. Enable **Client ID Metadata Document (CIMD)**
5. Copy the **Environment URL**, **Client ID**, and the **Protected Resource Metadata** JSON

### 2. Configure environment

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```
PORT=3001
SK_ENV_URL=https://your-env.scalekit.dev
SK_CLIENT_ID=your_scalekit_client_id
MCP_SERVER_ID=http://localhost:3001
PROTECTED_RESOURCE_METADATA={"authorization_servers":["..."],...}
```

`MCP_SERVER_ID` must exactly match the **Server URL** registered in Scalekit — it is validated against the `aud` claim in every access token.

### 3. Install and run

```bash
bundle install
bundle exec puma -p 3001
```

## How it works

```
MCP Client
  │
  ├─ GET /.well-known/oauth-protected-resource   (public — no auth)
  │    └─ returns authorization_servers[] so the client can discover Scalekit
  │
  └─ POST /   (all MCP calls)
       │
       ├─ ScalekitBearerAuth middleware
       │    ├─ extracts Bearer token from Authorization header
       │    ├─ fetches JWKS from Scalekit (RFC 8414 auto-discovery, cached 1h)
       │    ├─ validates signature, issuer, and audience
       │    └─ stores claims in thread-local storage for tools to read
       │
       └─ MCP::Server (official MCP Ruby SDK, stateless HTTP transport)
            └─ dispatches to the requested tool
```

**No client secret** — tokens are validated purely via RS256 + JWKS. The JWKS URI is discovered automatically from the authorization server metadata (RFC 8414), so nothing is hardcoded.

## Project structure

```
config.ru                              # Rack entry point — wires auth + MCP transport
lib/scalekit_token_validator.rb        # JWKS fetch, JWT decode, aud/iss validation
app/middleware/scalekit_bearer_auth.rb # Rack middleware — validates token on every MCP request
app/tools/
  who_am_i_tool.rb                     # Returns the `sub` claim — confirms auth is wired up
  greet_user_tool.rb                   # Greets a user by name
  inspect_token_tool.rb                # Extracts and logs any claim from the access token
app/controllers/
  well_known_controller.rb             # Serves /.well-known/oauth-protected-resource and /health
```

## Adding a tool

Create a new file in `app/tools/`:

```ruby
class MyTool < MCP::Tool
  description 'Does something useful.'

  input_schema(
    properties: { name: { type: 'string', description: 'Input value' } },
    required:   ['name']
  )

  def self.call(name:, server_context:)
    # Access token claims if needed
    claims = Thread.current.thread_variable_get(:scalekit_claims) || {}
    user   = claims['sub']

    MCP::Tool::Response.new([{ type: 'text', text: "Hello #{name} (user: #{user})" }])
  end
end
```

Then register it in `config.ru`:

```ruby
require_relative 'app/tools/my_tool'

mcp_server = MCP::Server.new(
  name:  'scalekit-mcp-rails',
  tools: [WhoAmITool, GreetUserTool, InspectTokenTool, MyTool]
)
```

## Accessing token claims in a tool

Scalekit issues JWT access tokens. Any standard or custom claim is available inside a tool via:

```ruby
claims = Thread.current.thread_variable_get(:scalekit_claims) || {}

claims['sub']    # user ID  (always present)
claims['iss']    # issuer   (always present)
claims['email']  # email    (if configured in Scalekit)
claims['org_id'] # custom claim example
```

The `inspect_token` tool demonstrates this interactively — pass any claim key and it returns the value (or lists all available keys if the claim is not found).

## Included tools

| Tool | Description |
|------|-------------|
| `who_am_i` | Returns the `sub` (user ID) from the token — verifies OAuth is wired up |
| `greet_user` | Takes a `name` parameter and returns a greeting |
| `inspect_token` | Takes a `claim_key` parameter and returns that claim's value from the token |

## Deploying

Set the same environment variables on your host. Update `MCP_SERVER_ID` and the **Server URL** in your Scalekit dashboard to your production URL. No other changes needed.
