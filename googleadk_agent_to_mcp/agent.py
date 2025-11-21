import logging
import httpx
from typing import Dict, Optional

# ---------------------------------------------------------
# CONFIGURATION (ALL PARAMS AT TOP OF FILE)
# ---------------------------------------------------------

MCP_SERVER_URL = "http://localhost:3002/" # register a greet mcp server in scalekit dashboard with server url as this
TOKEN_URL = "<env-url>/oauth/token"

CLIENT_ID = "m2m_xxx"
CLIENT_SECRET = "<your-secret>"

SCOPES_LIST = ["usr:read"]
SCOPES_STRING = "usr:read" # make sure this scope is checked in mcp server and the client too

# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent")

# ---------------------------------------------------------
# ADK IMPORTS
# ---------------------------------------------------------

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

from google.adk.auth import AuthCredential, AuthCredentialTypes, OAuth2Auth
from fastapi.openapi.models import OAuth2, OAuthFlows, OAuthFlowClientCredentials

# ---------------------------------------------------------
# GLOBAL TOKEN (must be sync)
# ---------------------------------------------------------

ACCESS_TOKEN: Optional[str] = None

# ---------------------------------------------------------
# ADK OAuth2 AUTH SCHEME  (OpenAPI metadata only)
# ---------------------------------------------------------

auth_scheme = OAuth2(
    flows=OAuthFlows(
        clientCredentials=OAuthFlowClientCredentials(
            tokenUrl=TOKEN_URL,
            scopes={scope: "scope description" for scope in SCOPES_LIST},
        )
    )
)

# ---------------------------------------------------------
# ADK AuthCredential metadata (not used for real HTTP)
# ---------------------------------------------------------

auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.OAUTH2,
    oauth2=OAuth2Auth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=SCOPES_LIST,
    ),
)

# ---------------------------------------------------------
# 1️⃣ FETCH TOKEN — SYNC-ONLY SAFE FUNCTION
# ---------------------------------------------------------

def fetch_access_token() -> str:
    global ACCESS_TOKEN

    if ACCESS_TOKEN:
        return ACCESS_TOKEN

    logger.info("🔐 Fetching OAuth2 access token…")

    resp = httpx.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": SCOPES_STRING,
        },
    )
    resp.raise_for_status()

    ACCESS_TOKEN = resp.json()["access_token"]

    logger.info(f"🔑 ACCESS TOKEN: {ACCESS_TOKEN[:25]}…")
    return ACCESS_TOKEN


# Fetch token before ADK event-loop starts
fetch_access_token()

# ---------------------------------------------------------
# 2️⃣ HEADER PROVIDER (SYNC) — ALWAYS SEND TOKEN
# ---------------------------------------------------------

def header_provider(ctx) -> Dict[str, str]:
    return {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# ---------------------------------------------------------
# 3️⃣ MCP TOOLSET
# ---------------------------------------------------------

todo_mcp_server = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=MCP_SERVER_URL
    ),
    auth_scheme=auth_scheme,
    auth_credential=auth_credential,
    header_provider=header_provider,   # <-- critical: FORCES token headers
)

# ---------------------------------------------------------
# 4️⃣ GOOGLE ADK AGENT
# ---------------------------------------------------------

root_agent = Agent(
    model="gemini-2.5-flash",
    name="greet_agent",
    description="Agent authenticated with forced OAuth2 token for MCP server",
    instruction="Use the MCP tools.",
    tools=[todo_mcp_server],
)

