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
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response

from src.config.config import config
from src.lib.auth import oauth_protected_resource_handler
from src.lib.logger import logger
from src.lib.middleware import AuthMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            # Log request
            body = await request.body()
            logger.info(
                f"Request: {request.method} {request.url}\n"
                f"Headers: {dict(request.headers)}\n"
                f"Body: {body.decode('utf-8', errors='replace')}"
            )
            response: Response = await call_next(request)
            resp_body = b""
            async for chunk in response.body_iterator:
                resp_body += chunk
            # Reconstruct response for downstream
            new_response = Response(
                content=resp_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
            logger.info(
                f"Response: {response.status_code}\n"
                f"Headers: {dict(response.headers)}\n"
                f"Body: {resp_body.decode('utf-8', errors='replace')}"
            )
            return new_response

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

# ------------------------------------------------------------------------------
# FastAPI app (uses MCP lifespan)
# ------------------------------------------------------------------------------
app = FastAPI(lifespan=mcp_app.lifespan)

protected_app = FastAPI(middleware=[Middleware(AuthMiddleware)], lifespan=mcp_app.lifespan)
protected_app.mount("", mcp_app)

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
# app.add_middleware(AuthMiddleware)
# app.add_middleware(LoggingMiddleware)


# ------------------------------------------------------------------------------
# Public routes (declare BEFORE mounting MCP)
# ------------------------------------------------------------------------------
@app.get("/.well-known/oauth-protected-resource/mcp")
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
app.mount("/mcp", protected_app)


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
