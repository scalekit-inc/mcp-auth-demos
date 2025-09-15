"""
Configuration management for the Python MCP Server.

This module handles all environment variables and server configuration,
including ScaleKit authentication settings and MCP server parameters.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Server configuration class with environment variable defaults."""
    
    # Server identification
    SERVER_NAME = "Python MCP Server"
    SERVER_VERSION = "1.0.0"
    
    # Server settings
    PORT = int(os.getenv("PORT", 3002))  # Default port for MCP server
    LOG_LEVEL = os.getenv("LOG_LEVEL", "info")  # Logging level (debug, info, warning, error)
    
    # ScaleKit OAuth 2.1 configuration
    SK_ENV_URL = os.getenv("SK_ENV_URL", "")  # ScaleKit environment URL
    SK_CLIENT_ID = os.getenv("SK_CLIENT_ID", "")  # ScaleKit client ID
    SK_CLIENT_SECRET = os.getenv("SK_CLIENT_SECRET", "")  # ScaleKit client secret
    
    # MCP server configuration
    MCP_SERVER_ID = os.getenv("MCP_SERVER_ID", "")  # Unique MCP server identifier
    
    # OAuth 2.1 protected resource metadata (optional - will use defaults if not provided)
    PROTECTED_RESOURCE_METADATA = os.getenv("PROTECTED_RESOURCE_METADATA", "")

    EXPECTED_AUDIENCE = os.getenv("EXPECTED_AUDIENCE", "")  # Expected audience for token validation

# Global configuration instance
config = Config()
