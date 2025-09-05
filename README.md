<p align="center">
  <a href="https://scalekit.com" target="_blank" rel="noopener noreferrer">
    <picture>
      <img src="https://cdn.scalekit.cloud/v1/scalekit-logo-dark.svg" height="64">
    </picture>
  </a>
</p>

<h1 align="center">
  Scalekit MCP Auth Demos
</h1>

<p align="center">
  <strong>Auth stack for AI apps ⚡ Secure MCP with OAuth</strong>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@scalekit-sdk/node"><img src="https://img.shields.io/npm/v/@scalekit-sdk/node.svg" alt="npm version"></a>
  <a href="https://github.com/scalekit-inc/mcp-auth-demos/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://docs.scalekit.com/guides/mcp/overview"><img src="https://img.shields.io/badge/docs-MCP%20Guide-blue" alt="MCP Documentation"></a>
</p>

<p align="center">
  Secure Model Context Protocol (MCP) server demonstrating OAuth-protected AI agent interactions
</p>

## 🚀 What This Demo Shows

- **OAuth-Protected MCP**: Secure AI agent access with user authentication
- **Dynamic Client Registration**: Automatic MCP server registration and permissioning
- **Permission Management**: Fine-grained access control for AI tools
- **Enterprise Integration**: Connect AI agents to enterprise authentication systems

## Prerequisites
- Node.js (v18+ recommended)
- npm
- Access to [app.scalekit.com](https://app.scalekit.com) with workspace
- (Optional) VS Code Insider with MCP extension, or any compatible MCP client

## Getting Started

### 1. Enable Full Stack Authentication
- Go to [app.scalekit.com](https://app.scalekit.com) and log in to your workspace.
- Enable **Full Stack Authentication** for your workspace.

### 2. Obtain Credentials
- Copy your **Environment URL**, **Client ID**, and **Client Secret** from the Settings -> API Credentials section on Scalekit dashboard.

### 3. Configure Environment Variables
- Create/Update `.env` file in the root of the `greeting-mcp` directory.
- Add the following variables:
	```env
	SK_ENV_URL=your_environment_url
	SK_CLIENT_ID=your_client_id
	SK_CLIENT_SECRET=your_client_secret
	# Add MCP_SERVER_ID and PROTECTED_RESOURCE_METADATA in later steps
	```

### 4. Set Up Permissions
- In [app.scalekit.com](https://app.scalekit.com), navigate to **Authorization** > **Permissions**.
- Create a permission:
	- **Name:** `usr:read`
	- **Description:** `Reading basic information of the users`

### 5. Register the MCP Server
- Go to **MCP Servers** in [app.scalekit.com](https://app.scalekit.com).
- Register a new MCP server:
	- **Server Identifier:** `http://localhost:3002/` [make sure you have put a trailing slash at the end]
	- **Enable Dynamic Client Registration:** (check the box)
- After creation, copy:
	- **MCP Server ID** (looks like `res_XXX`)
	- **Protected Resource Metadata** (as JSON)
- Add these to your `.env` file. **Minify** the JSON for `PROTECTED_RESOURCE_METADATA` (remove all whitespace):
	```env
	MCP_SERVER_ID=res_XXX
	PROTECTED_RESOURCE_METADATA='{...minified_json...}'
	```

### 6. Install Dependencies
```sh
cd greeting-mcp
npm install
npx tsc
```

### 7. Run the Server
```sh
npm run start
```

The server will start on `http://localhost:3002`.

### 8. Connect with an MCP Client
- Use an MCP client (e.g., VS Code Insider with MCP extension).
- Open your `mcp.json` and paste:
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
- Click **Start**.

### 9. Authorize and Test
- Allow all prompts in the MCP client.
- Log in with your email address and authorize when prompted.
- In your MCP client, enter a prompt like:
	> Can you please greet John?
- You should see the greeting tool being invoked (allow if prompted).

#### Note - For Non-OAuth MCP Clients
If your MCP client does not support OAuth, use the following in your `mcp.json`. This makes use of mcp-remote to handle authentication:
```json
{
	"mcpServers": {
		"greeting": {
			"command": "npx",
			"args": [
				"-y", "mcp-remote", "http://localhost:3002/"
			]
		}
	}
}
```

---

## Project Structure
```
greeting-mcp/
├── package.json
├── tsconfig.json
├── src/
│   ├── main.ts
│   ├── config/
│   │   └── config.ts
│   ├── lib/
│   │   ├── auth.ts
│   │   ├── logger.ts
│   │   ├── middleware.ts
│   │   └── transport.ts
│   └── tools/
│       ├── greeting.ts
│       └── index.ts
```

## License
See [LICENSE](./LICENSE).

## Key Features

- **Secure MCP Authentication**: OAuth 2.0 flow for AI agent authorization
- **Dynamic Registration**: Automatic server setup and permission configuration
- **Fine-Grained Permissions**: Control what AI agents can access
- **Enterprise Ready**: Production-grade security for business environments
- **Client Compatibility**: Works with VS Code, Claude Desktop, Cursor, and Windsurf

## Additional Resources

- 📚 [MCP Authentication Guide](https://docs.scalekit.com/guides/mcp/overview/)
- 🔧 [Scalekit API Reference](https://docs.scalekit.com/apis)
- 💬 [Community Support](https://github.com/scalekit-inc/scalekit-sdk-node-js/discussions)
- 🎯 [Get Started with MCP](https://docs.scalekit.com/quick-start-guide)
- ⚡ [Model Context Protocol Spec](https://modelcontextprotocol.io)

---

<p align="center">
  Made with ❤️ by <a href="https://scalekit.com">Scalekit</a>
</p>