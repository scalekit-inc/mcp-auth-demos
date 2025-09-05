"""
OAuth 2.1 Protected Resource Metadata Handler

This module implements the OAuth 2.1 protected resource metadata endpoint
(/.well-known/oauth-protected-resource) that provides OAuth client discovery
information for ScaleKit authentication.
"""

import json
from fastapi import Response
from src.config.config import config
from src.lib.logger import logger

async def oauth_protected_resource_handler() -> Response:
    """
    Handle OAuth 2.1 protected resource metadata endpoint.
    
    This endpoint provides OAuth client discovery information including:
    - Authorization server URLs
    - Supported bearer token methods
    - Resource identifier
    - Supported scopes
    
    Returns either custom metadata from environment variables or default
    metadata structure following ScaleKit OAuth 2.1 specification.
    """
    try:
        logger.info("OAuth protected resource metadata requested")
        
        # Use custom metadata if provided in environment variables
        if config.PROTECTED_RESOURCE_METADATA:
            logger.info("Using custom OAuth metadata from environment")
            metadata = json.loads(config.PROTECTED_RESOURCE_METADATA)
        else:
            # If PROTECTED_RESOURCE_METADATA is not set, return an error
            logger.error("PROTECTED_RESOURCE_METADATA config missing for OAuth metadata endpoint")
            return Response(
                content=json.dumps({"error": "PROTECTED_RESOURCE_METADATA config missing"}),
                media_type="application/json",
                status_code=500
            )

        logger.info(f"OAuth metadata response: {json.dumps(metadata, indent=2)}")
        logger.info(f"Authorization server: {metadata['authorization_servers'][0]}")
        logger.info(f"Supported scopes: {metadata['scopes_supported']}")
        
        return Response(
            content=json.dumps(metadata, indent=2),
            media_type="application/json",
            status_code=200
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid OAuth metadata JSON: {e}")
        return Response(
            content=json.dumps({"error": "Invalid metadata configuration"}),
            media_type="application/json",
            status_code=500
        )
