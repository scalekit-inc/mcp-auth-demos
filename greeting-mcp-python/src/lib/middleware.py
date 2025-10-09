"""
ScaleKit OAuth 2.1 Authentication Middleware
--------------------------------------------

This module validates Bearer tokens for all incoming HTTP requests to the MCP server.
It integrates with the ScaleKit SDK for token verification following the OAuth 2.1 specification.

Responsibilities:
1. Allow unauthenticated access to public routes like /.well-known and /health
2. Extract and validate Bearer tokens from the Authorization header
3. Verify the token using ScaleKit SDK (audience + issuer)
4. Return proper OAuth 2.1-compliant WWW-Authenticate responses on failure
"""

from fastapi import Request
from fastapi.responses import Response
from src.config.config import config
from src.lib.logger import logger
from scalekit import ScalekitClient
from scalekit.common.scalekit import TokenValidationOptions

# ---------------------------------------------------------------------------
# Setup ScaleKit Client
# ---------------------------------------------------------------------------
WWW_HEADER = {
    "WWW-Authenticate": (
        f'Bearer realm="OAuth", '
        f'resource_metadata="http://localhost:{config.PORT}/.well-known/oauth-protected-resource/mcp"'
    )
}

try:
    scalekit_client = ScalekitClient(
        env_url=config.SK_ENV_URL,
        client_id=config.SK_CLIENT_ID,
        client_secret=config.SK_CLIENT_SECRET,
    )
    SCALEKIT_AVAILABLE = True
    logger.info("ScaleKit client initialized successfully")
except Exception as e:
    SCALEKIT_AVAILABLE = False
    scalekit_client = None
    logger.warning(f"ScaleKit SDK not available: {e}")

# ---------------------------------------------------------------------------
# Authentication Middleware Function
# ---------------------------------------------------------------------------
async def auth_middleware(request: Request, call_next):
    """
    Middleware for authenticating requests using ScaleKit OAuth 2.1.
    """
    try:
        # Allow public and non-auth routes
        if ".well-known" in request.url.path or request.url.path == "/health":
            return await call_next(request)

        logger.info(f"Auth request for {request.method} {request.url.path}")

        # Extract Bearer token
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Missing Bearer token")
            return Response(
                content='{"error": "Missing Bearer token"}',
                media_type="application/json",
                status_code=401,
                headers=WWW_HEADER,
            )

        token = auth_header.split("Bearer ")[1].strip()
        logger.info(f"Token extracted, length: {len(token)}")

        # Ensure ScaleKit SDK is available
        if not SCALEKIT_AVAILABLE:
            logger.error("ScaleKit SDK not available for token validation")
            return Response(
                content='{"error": "Authentication service unavailable"}',
                media_type="application/json",
                status_code=503,
                headers=WWW_HEADER,
            )

        # Validate token
        logger.info("Validating token with ScaleKit...")
        options = TokenValidationOptions(
            issuer=config.SK_ENV_URL,
            audience=[config.EXPECTED_AUDIENCE],
        )
        is_valid = scalekit_client.validate_access_token(token, options=options)
        logger.info(f"Token validation result: {is_valid}")

        if not is_valid:
            return Response(
                content='{"error": "Invalid token"}',
                media_type="application/json",
                status_code=401,
                headers=WWW_HEADER,
            )

        # Token valid → continue request
        logger.info(f"Authentication successful for {request.method} {request.url.path}")
        return await call_next(request)

    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return Response(
            content='{"error": "Authentication failed"}',
            media_type="application/json",
            status_code=401,
            headers=WWW_HEADER,
        )
