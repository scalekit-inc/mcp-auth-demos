#!/usr/bin/env python3
"""
FastMCP Server with OAuth 2.1 Authentication
--------------------------------------------

This file composes three layers:
1. FastMCP server exposing tools (MCP protocol endpoints)
2. Auth middleware (validates Bearer tokens via ScaleKit SDK)
3. Outer FastAPI app for public routes and CORS handling

Final routes:
- /.well-known/oauth-protected-resource/mcp  → OAuth discovery endpoint
- /health                                   → Health check
- /mcp/*                                   → Protected MCP API (tools)
"""

from fastmcp import FastMCP, Context
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.config.config import config
from src.lib.auth import oauth_protected_resource_handler
from src.lib.logger import logger
from src.lib.middleware import auth_middleware

# ------------------------------------------------------------------------------
# Define MCP tools
# ------------------------------------------------------------------------------
mcp = FastMCP(config.SERVER_NAME)

@mcp.tool(name="greet_user", description="Greets the user with a personalized message.")
async def greet_user(name: str, ctx: Context | None = None) -> dict:
    """Example tool that returns a greeting."""
    logger.info(f"Invoked greet_user tool for name: {name}")
    return {"content": [{"type": "text", "text": f"Hi {name}, welcome to Scalekit!"}]}

# Create MCP ASGI app at root (no nested /mcp)
mcp_app = mcp.http_app(path="/")

# ------------------------------------------------------------------------------
# Protected sub-app (adds OAuth middleware)
# ------------------------------------------------------------------------------
protected_app = FastAPI(lifespan=mcp_app.lifespan)
protected_app.middleware("http")(auth_middleware)
protected_app.mount("", mcp_app)

# ------------------------------------------------------------------------------
# Outer app (CORS + public endpoints)
# ------------------------------------------------------------------------------
app = FastAPI(lifespan=mcp_app.lifespan)

# Enable CORS for client compatibility (e.g., MCP Inspector)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Mcp-Protocol-Version", "Content-Type", "Authorization"],
    expose_headers=["WWW-Authenticate"],
    max_age=86400,
)

# Public endpoints
@app.get("/.well-known/oauth-protected-resource/mcp")
async def oauth_endpoint():
    """OAuth 2.1 resource metadata endpoint for ScaleKit."""
    return await oauth_protected_resource_handler()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "server": config.SERVER_NAME, "version": config.SERVER_VERSION}

# Mount protected MCP app at /mcp
app.mount("/mcp", protected_app)

# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    logger.info(f"🚀 Server running on http://0.0.0.0:{config.PORT} (MCP at /mcp)")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.PORT,
        log_level=config.LOG_LEVEL.lower(),
    )
