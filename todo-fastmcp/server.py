"""Scalekit-authenticated FastMCP server providing in-memory CRUD tools for todos.

This example mirrors the greeting-fastmcp project structure while exposing
todo management capabilities through FastMCP tools.
"""

import os
import uuid
from dataclasses import dataclass, asdict
from typing import Optional

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.scalekit import ScalekitProvider
from fastmcp.server.dependencies import AccessToken, get_access_token

from scalekit import ScalekitClient
import uuid
import requests

# Load environment variables from .env file when available.
load_dotenv()

skClient = ScalekitClient(os.getenv("SCALEKIT_ENVIRONMENT_URL"), os.getenv("SCALEKIT_CLIENT_ID"), os.getenv("SCALEKIT_CLIENT_SECRET"))

mcp = FastMCP(
    "Todo Server",
    stateless_http=True,
    auth=ScalekitProvider(
        environment_url=os.getenv("SCALEKIT_ENVIRONMENT_URL"),
        resource_id=os.getenv("SCALEKIT_RESOURCE_ID"),
        # FastMCP appends /mcp automatically; keep base URL with trailing slash only.
        base_url=os.getenv("MCP_BASE_URL"),
    ),
)


@dataclass
class TodoItem:
    """Simple representation of a todo item stored in memory."""

    id: str
    title: str
    description: Optional[str]
    completed: bool = False

    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation of the todo item."""
        return asdict(self)


# Module-level storage keeps todos available for the lifetime of the process.
_TODO_STORE: dict[str, TodoItem] = {}


def _require_scope(scope: str) -> Optional[str]:
    """Return an error message if the active token lacks the expected scope, else None."""
    token: AccessToken = get_access_token()
    if scope not in token.scopes:
        return f"Insufficient permissions: `{scope}` scope required."
    return None


# Zluri's system saves this todo task via internal api with Auth0 token
@mcp.tool
def create_internal_todo(title: str, description: Optional[str] = None) -> dict:
    """Create a new todo item."""
    error = _require_scope("todo:write")
    if error:
        return {"error": error}

    todo = TodoItem(id=str(uuid.uuid4()), title=title, description=description)
    _TODO_STORE[todo.id] = todo

    # this is the access token that mcp client sent. open it and get the user_id
    token: AccessToken = get_access_token()
    user_id = token.claims.get("email")

    # Get Auth0 access token from Zluri's internal api connected account
    auth0_connected_account = skClient.actions.get_or_create_connected_account(connection_name="AUTH0", identifier=user_id).connected_account
    tokens = auth0_connected_account.authorization_details["oauth_token"]
    auth0_access_token = tokens["access_token"]
    print("Zluri's Auth0 Access Token:", auth0_access_token)

    # Call Zuluri internal api to create the todo task
    try:
        headers = {
            "Authorization": f"Bearer {auth0_access_token}",
            "Content-Type": "application/json",
        }
        payload = {"name": todo.title}
        resp = requests.post("https://fd05b447-7822-4c2b-bb91-5bed8ff78b07.mock.pstmn.io/todo", json=payload, headers=headers, timeout=10)
        print("Zluri's internal API response:", resp.status_code, resp.text)
    except Exception as e:
        print("Failed to call external API:", e)

    return {"todo": todo.to_dict()}

# Zluri's system saves this todo task via external api with Auth0 token
@mcp.tool
def create_external_todo(title: str, description: Optional[str] = None) -> dict:
    """Create a new todo item."""
    error = _require_scope("todo:write")
    if error:
        return {"error": error}

    todo = TodoItem(id=str(uuid.uuid4()), title=title, description=description)
    _TODO_STORE[todo.id] = todo

    # This is the access token that mcp client sent. open it and get the user_id
    token: AccessToken = get_access_token()
    user_id = token.claims.get("email")

    # Get Zluri API Key connected account
    ext_connected_account = skClient.actions.get_or_create_connected_account(connection_name="zluri", identifier=user_id).connected_account
    tokens = ext_connected_account.authorization_details["oauth_token"]
    ext_access_token = tokens["access_token"]
    print("Zluri's external api-key or token:", ext_access_token)

    # Call Zuluri external api to create the todo task
    try:
        headers = {
            "Authorization": f"{ext_access_token}",
            "Content-Type": "application/json",
        }
        payload = {"name": todo.title}
        resp = requests.post("https://fd05b447-7822-4c2b-bb91-5bed8ff78b07.mock.pstmn.io/todo-ext", json=payload, headers=headers, timeout=10)
        print("Zluri's External API response:", resp.status_code, resp.text)
    except Exception as e:
        print("Failed to call external API:", e)

    return {"todo": todo.to_dict()}

if __name__ == "__main__":
    mcp.run(transport="http", port=int(os.getenv("PORT", "3002")))
