# Greeting MCP Server

A secure Model Context Protocol (MCP) server for greeting users. This project demonstrates secure, permissioned mcp with dynamic client registration using Scalekit's platform.

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
	"servers": {
		"greet": {
			"url": "http://localhost:3002/",
			"type": "http"
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

---

For more information, visit [Scalekit Documentation](https://docs.scalekit.com/guides/mcp/overview/) or contact your workspace admin.