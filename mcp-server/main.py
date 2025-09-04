"""
Python MCP Server with ScaleKit Authentication

A simple Model Context Protocol (MCP) server that provides authenticated access
to tools via ScaleKit OAuth 2.1. This server follows the same structure as the
TypeScript greeting-mcp example but implemented in Python.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp.server import Server
from src.config.config import config
from src.lib.auth import oauth_protected_resource_handler
from src.lib.logger import logger
from src.lib.middleware import auth_middleware
from src.lib.transport import setup_transport_routes
from src.tools.index import register_tools

# Initialize MCP server
mcp_server = Server(config.SERVER_NAME)

# Create FastAPI application
app = FastAPI(
    title=config.SERVER_NAME,
    version=config.SERVER_VERSION,
    description="Python MCP Server with ScaleKit Authentication"
)

# Configure CORS for MCP client compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Mcp-Protocol-Version", "Content-Type", "Authorization"],
    expose_headers=["WWW-Authenticate"],  # Required for OAuth 2.1
    max_age=86400,
)

# Add ScaleKit authentication middleware
app.middleware("http")(auth_middleware)

# OAuth 2.1 Protected Resource Metadata endpoint
@app.get("/.well-known/oauth-protected-resource")
async def oauth_endpoint():
    """OAuth 2.1 protected resource metadata endpoint"""
    return await oauth_protected_resource_handler()

# Setup MCP transport routes
setup_transport_routes(app, mcp_server)
logger.info("Transport routes set up successfully")

# Register tools
register_tools(mcp_server)
logger.info("Registered tools successfully")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint - accessible without authentication"""
    return {
        "status": "healthy",
        "server": config.SERVER_NAME,
        "version": config.SERVER_VERSION
    }

# Application entry point
if __name__ == "__main__":
    import uvicorn

    logger.info(f"MCP server running on http://localhost:{config.PORT}")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.PORT,
        log_level=config.LOG_LEVEL.lower()
    )
