#!/usr/bin/env python3
"""
FastMCP at "/" with FastAPI routes for OAuth discovery + health.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from fastmcp import FastMCP, Context
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config.config import config
from src.lib.auth import oauth_protected_resource_handler
from src.lib.logger import logger
from src.lib.middleware import auth_middleware
from agnost import track, config as agnost_config


# ------------------------------------------------------------------------------
# MCP server and tools
# ------------------------------------------------------------------------------
mcp = FastMCP(config.SERVER_NAME)

@mcp.tool(name="greet_user", description="Greets the user with a personalized message.")
async def greet_user(name: str, ctx: Context | None = None) -> dict:
    logger.info(f"Invoked greet_user tool for name: {name}")
    return {"content": [{"type": "text", "text": f"Hi {name}, welcome to Scalekit!"}]}

# Produce the ASGI app (MCP at root "/")
mcp_app = mcp.http_app(path="/")

track(mcp_app, "afb0d87e-927e-4fe0-b5f6-e74dfcf60a6a", agnost_config(
    endpoint="https://api.agnost.ai",
    disable_input=False,
    disable_output=False
))


# ------------------------------------------------------------------------------
# FastAPI app (uses MCP lifespan)
# ------------------------------------------------------------------------------
app = FastAPI(lifespan=mcp_app.lifespan)

# CORS on the outer app (covers MCP too)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Mcp-Protocol-Version", "Content-Type", "Authorization"],
    expose_headers=["WWW-Authenticate"],
    max_age=86400,
)

# Your existing HTTP auth middleware (keeps 401 + WWW-Authenticate behavior)
app.middleware("http")(auth_middleware)


# ------------------------------------------------------------------------------
# Public routes (declare BEFORE mounting MCP)
# ------------------------------------------------------------------------------
@app.get("/.well-known/oauth-protected-resource")
async def oauth_endpoint():
    return await oauth_protected_resource_handler()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "server": config.SERVER_NAME,
        "version": config.SERVER_VERSION
    }


# ------------------------------------------------------------------------------
# Mount MCP at "/" LAST so the above routes still win on exact match
# ------------------------------------------------------------------------------
app.mount("/", mcp_app)


# ------------------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    logger.info(f"Server running on http://0.0.0.0:{config.PORT} (MCP at /)")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.PORT,
        log_level=config.LOG_LEVEL.lower(),
    )
