"""
ScaleKit Authentication Middleware

This module implements OAuth 2.1 authentication middleware using ScaleKit SDK.
It validates Bearer tokens for all MCP requests and ensures proper authorization
according to the OAuth 2.1 specification.
"""

import json
from fastapi import Request
from fastapi.responses import Response
from src.config.config import config
from src.lib.logger import logger
from scalekit import ScalekitClient
from scalekit.common.scalekit import TokenValidationOptions
from starlette.types import ASGIApp, Receive, Scope, Send

# OAuth 2.1 configuration
WWW_HEADER = {
    "WWW-Authenticate": f'Bearer realm="OAuth", resource_metadata="http://localhost:{config.PORT}/.well-known/oauth-protected-resource/mcp"'
}

# Initialize ScaleKit client for token validation
try:
    scalekit_client = ScalekitClient(
        env_url=config.SK_ENV_URL,
        client_id=config.SK_CLIENT_ID,
        client_secret=config.SK_CLIENT_SECRET
    )
    SCALEKIT_AVAILABLE = True
    logger.info("ScaleKit client initialized successfully")
except Exception as e:
    logger.warning(f"ScaleKit SDK not available: {e}")
    scalekit_client = None
    SCALEKIT_AVAILABLE = False

class AuthMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive=receive)
        path = scope["path"]

        # Allow public routes
        if ".well-known" in path or path == "/health":
            return await self.app(scope, receive, send)

        auth_header = request.headers.get("authorization")
        logger.info(f"Auth request for {request.method} {path}")

        if not auth_header or not auth_header.startswith("Bearer "):
            headers = {
                "WWW-Authenticate": (
                    f'Bearer realm="OAuth", '
                    f'resource_metadata="http://localhost:{config.PORT}/.well-known/oauth-protected-resource/mcp"'
                )
            }
            response = Response('{"error": "Missing Bearer token"}', status_code=401, media_type="application/json", headers=headers)
            await response(scope, receive, send)
            return

        token = auth_header.split("Bearer ")[1].strip()
        logger.info(f"Token extracted, length: {len(token)}")

        try:
            options = TokenValidationOptions(issuer=config.SK_ENV_URL, audience=[config.EXPECTED_AUDIENCE])
            is_valid = scalekit_client.validate_access_token(token, options=options)
            logger.info(f"Token validation result: {is_valid}")
            if not is_valid:
                response = Response('{"error": "Invalid token"}', status_code=401, media_type="application/json")
                await response(scope, receive, send)
                return
        except Exception as e:
            logger.error(f"Token validation failed: {e}")
            response = Response('{"error": "Authentication failed"}', status_code=401, media_type="application/json")
            await response(scope, receive, send)
            return

        # If authenticated, continue to next ASGI app (MCP)
        await self.app(scope, receive, send)
