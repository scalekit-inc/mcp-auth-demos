## Greeting MCP Server

A secure Model Context Protocol (MCP) server for greeting users with OAuth 2.1 authentication using Scalekit.

### Quick Start

```bash
# 1. Install and build
npm install && npm run build

# 2. Configure environment (see detailed setup below)
cp .env.example .env
# Edit .env with your Scalekit credentials

# 3. Start the server
npm run start

# 4. Test the server
curl http://localhost:3002/.well-known/oauth-protected-resource
```

### Prerequisites

- Node.js (v18+)
- npm
- [Scalekit workspace](https://app.scalekit.com)
- MCP client (refer to your MCP host documentation)

### Setup Guide

### 1. Configure Scalekit

**Enable Full Stack Authentication**

1. Go to [app.scalekit.com](https://app.scalekit.com)
2. Log in to your workspace
3. Enable **Full Stack Authentication**

**Get API Credentials**

1. Navigate to **Settings** → **API Credentials**
2. Copy:
   - Environment URL
   - Client ID
   - Client Secret

### 2. Set Up Environment

Create a `.env` file:

```bash
# Required: ScaleKit Configuration
SCALEKIT_ENVIRONMENT_URL=your_environment_url
SCALEKIT_CLIENT_ID=your_client_id
SCALEKIT_CLIENT_SECRET=your_client_secret
```

💡 **Note**: The remaining configuration (MCP server ID, OAuth metadata, etc.) has sensible defaults in `src/config/config.ts`. You can customize these values directly in the config file if needed.

⚠️ **Important**: Replace `your_*` values with actual credentials from Scalekit.

### 3. Configure Permissions

1. In Scalekit, go to **Authorization** → **Permissions**
2. Create a permission:
   - **Name**: `usr:read`
   - **Description**: `Reading basic information of the users`

### 4. Register MCP Server

1. In Scalekit, go to **MCP Servers**
2. Click **Add MCP Server**
3. Configure:
   - **Name**: `Greeting MCP Server` (or your preferred name)
   - **Server URL**: `http://localhost:3002/` (ensure trailing slash)
   - Enable **Dynamic Client Registration**
   - **Scopes**: Add `usr:read`
4. After creation, copy:
   - **MCP Server ID** (looks like `res_XXX`)
   - **Protected Resource Metadata** (JSON)

**Update the configuration in `src/config/config.ts`:**

The application has sensible defaults, but you should update these values with your actual MCP server details:

```typescript
// In src/config/config.ts, update these values:
mcpServerId: process.env.MCP_SERVER_ID || 'res_XXX', // Replace with your actual MCP Server ID
protectedResourceMetadata: process.env.PROTECTED_RESOURCE_METADATA || '{"authorization_servers":["https://your-env.scalekit.com/resources/res_XXX"],"bearer_methods_supported":["header"],"resource":"http://localhost:3002/","resource_documentation":"https://docs.scalekit.com","scopes_supported":["usr:read"]}',
expectedAudience: process.env.EXPECTED_AUDIENCE || 'http://localhost:3002/',
```

💡 **Tip**: You can either set these as environment variables in your `.env` file or directly modify the default values in `config.ts`.

### 5. Install and Run

```bash
# Install dependencies
npm install

# Build the project
npm run build

# Start the server
npm run start
```

✅ **Check**: Server should start on `http://localhost:3002`

### 6. Connect MCP Client

Your MCP client needs to be configured to authenticate with Scalekit (the authorization server for this MCP server).

**For VS Code Insider with MCP Extension:**
Open your `mcp.json` and add:

```json
{
  "servers": {
    "greeting": {
      "url": "http://localhost:3002/",
      "type": "http"
    }
  },
  "inputs": []
}
```

**For other MCP clients:**
Refer to your MCP host documentation for instructions on how to:

- Configure OAuth authentication servers
- Add Scalekit as an authorization provider
- Connect to OAuth-protected MCP servers

Your MCP client will discover the Scalekit authorization server automatically through the `.well-known/oauth-protected-resource` endpoint.

### 7. Test and Authorize

1. Start your MCP client
2. Follow your MCP client's authentication flow
3. Log in with your email when prompted by Scalekit
4. Authorize the requested permissions
5. Test with a prompt like:
   ```
   Can you please greet John?
   ```

✅ **Success**: The greeting tool should be invoked and return a personalized greeting.

### Verify Setup

### Check Server Health

```bash
curl http://localhost:3002/.well-known/oauth-protected-resource
```

### Test Authentication Flow

1. Start your MCP client
2. Follow the authentication redirects to Scalekit
3. Verify successful authorization in your MCP client

### License

See [LICENSE](./LICENSE).

---

**Need help?** Visit [Scalekit Documentation](https://docs.scalekit.com/mcp/oauth)
