# Python MCP Server with ScaleKit Authentication

A production-ready Python-based Model Context Protocol (MCP) server with ScaleKit OAuth 2.1 authentication integration.

## Features

- **ScaleKit OAuth 2.1**: Secure authentication with scope-based authorization
- **Modular Architecture**: Clean separation of concerns (config, auth, tools, transport)
- **FastAPI Backend**: Modern async Python web framework
- **Comprehensive Logging**: Structured logging for debugging and monitoring
- **CORS Support**: Cross-origin resource sharing for web client compatibility

## Quick Start

### Automated Setup
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

1. **Create Virtual Environment** (Python 3.11+ required):
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   ```bash
   cp env.example .env
   # Edit .env with your ScaleKit credentials and server settings
   ```

   - `PORT`: (optional) The port the server will listen on. Defaults to 3003.
   - `SK_ENV_URL`: Your ScaleKit environment URL (required).
   - `SK_CLIENT_ID`: Your ScaleKit client ID (required).
   - `SK_CLIENT_SECRET`: Your ScaleKit client secret (required).
   - `MCP_SERVER_ID`: Unique MCP server identifier (required).
   - `PROTECTED_RESOURCE_METADATA`: Minified JSON string for OAuth protected resource metadata (required; copy from Scalekit dashboard and remove all whitespace).
   - `EXPECTED_AUDIENCE`: The MCP server URL as registered in the Scalekit dashboard (required; e.g., `http://localhost:3003/`).

   > **Note:** After editing `.env`, restart the server for changes to take effect.

4. **Run the Server**:
   ```bash
   python main.py
   ```

   The server will start on `http://localhost:3003` (or the port you set in `.env`).

## Available Tools

### greet_user
- **Description**: Greets a user with a personalized message
- **Required Scope**: `usr:read`
- **Parameters**: `name` (string) - The name of the user to greet

## Authentication

The server implements ScaleKit OAuth 2.1 authentication:

- **Bearer Token Validation**: All MCP requests require valid Bearer tokens
- **Scope-Based Access**: Each tool requires specific OAuth scopes
- **Public Endpoints**: OAuth discovery and health check endpoints are publicly accessible
- **OAuth 2.1 Compliance**: Returns proper error responses

## API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/.well-known/oauth-protected-resource` | GET | OAuth 2.1 metadata discovery | No |
| `/` | POST | MCP protocol communication | Yes |
| `/health` | GET | Server health check | No |
| `/docs` | GET | FastAPI API documentation | No |

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SK_ENV_URL` | ScaleKit environment URL | - | Yes |
| `SK_CLIENT_ID` | ScaleKit client ID | - | Yes |
| `SK_CLIENT_SECRET` | ScaleKit client secret | - | Yes |
| `MCP_SERVER_ID` | Unique MCP server identifier | - | Yes |
| `PORT` | Server port | `3003` | No |
| `LOG_LEVEL` | Logging level | `info` | No |
| `PROTECTED_RESOURCE_METADATA` | Minified OAuth protected resource metadata JSON (from Scalekit dashboard) | - | Yes |
| `EXPECTED_AUDIENCE` | The MCP server URL as registered in the Scalekit dashboard (e.g., `http://localhost:3003/`) | - | Yes |

## Development

### Adding New Tools

1. **Define the tool** in `src/tools/index.py`:
   ```python
   tools_list = {
       "your_tool": {
           "name": "your_tool",
           "description": "Your tool description",
           "required_scopes": ["your:scope"],
       },
   }
   ```

2. **Implement the tool** in `src/tools/your_tool.py`:
   ```python
   def register_your_tool(server: Server):
       @server.call_tool()
       async def your_tool_function(param: str) -> dict:
           return {"content": [{"type": "text", "text": "result"}]}
       
       TOOLS["your_tool"]["registered_tool"] = your_tool_function
   ```

3. **Register the tool** in `src/tools/index.py`:
   ```python
   def register_tools(server):
       from .greeting import register_greeting_tools
       from .your_tool import register_your_tool
       
       register_greeting_tools(server)
       register_your_tool(server)
   ```

## License

This project is licensed under the MIT License.
