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

# OAuth 2.1 configuration
RESOURCE_ID = f"http://localhost:{config.PORT}/"
WWW_HEADER = {
    "WWW-Authenticate": f'Bearer realm="OAuth", resource_metadata="http://localhost:{config.PORT}/.well-known/oauth-protected-resource"'
}

# Initialize ScaleKit client for token validation
try:
    from scalekit import ScalekitClient
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

async def auth_middleware(request: Request, call_next):
    """
    Authentication middleware for MCP requests following ScaleKit OAuth 2.1 specification.
    
    This middleware:
    1. Allows public access to well-known endpoints and health checks
    2. Extracts Bearer tokens from Authorization headers
    3. Validates tokens using ScaleKit SDK
    4. Returns proper OAuth 2.1 error responses on failure
    """
    try:
        # Allow public access to OAuth discovery, health, and MCP root endpoints
        if ".well-known" in request.url.path or request.url.path == "/health":
            return await call_next(request)
        
        # Extract Bearer token
        auth_header = request.headers.get("authorization")
        logger.info(f"Auth request for {request.method} {request.url.path}")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning(f"Missing Bearer token for {request.method} {request.url.path}")
            return Response(
                content='{"error": "Missing Bearer token"}',
                media_type="application/json",
                status_code=401,
                headers=WWW_HEADER
            )
        
        token = auth_header.split("Bearer ")[1].strip()
        logger.info(f"Token extracted, length: {len(token)}")
        
        if not SCALEKIT_AVAILABLE:
            logger.error("ScaleKit SDK not available for token validation")
            return Response(
                content='{"error": "Authentication service unavailable"}',
                media_type="application/json",
                status_code=401,
                headers=WWW_HEADER
            )
        
        try:
            # Token validation with ScaleKit
            logger.info("Validating token with ScaleKit...")
            is_valid = scalekit_client.validate_access_token(token)
            logger.info(f"Token validation result: {is_valid}")
            
            if not is_valid:
                logger.warning(f"Token validation failed for {request.method} {request.url.path}")
                return Response(
                    content='{"error": "Invalid token"}',
                    media_type="application/json",
                    status_code=401,
                    headers=WWW_HEADER
                )
            
            logger.info(f"Authentication successful for {request.method} {request.url.path}")
            return await call_next(request)
            
        except Exception as e:
            logger.error(f"Token validation exception: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            return Response(
                content='{"error": "Token validation failed"}',
                media_type="application/json",
                status_code=401,
                headers=WWW_HEADER
            )
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return Response(
            content='{"error": "Authentication failed"}',
            media_type="application/json",
            status_code=401,
            headers=WWW_HEADER
        )
