"""
Logging Configuration

This module sets up structured logging for the Python MCP Server with
consistent formatting and configurable log levels.
"""

import logging
import sys
from src.config.config import config

def setup_logger():
    """
    Setup logger with consistent formatting and configurable log levels.
    
    Creates a logger with:
    - Configurable log level from environment variables
    - Consistent timestamp and level formatting
    - Console output to stdout
    - Prevention of duplicate handlers
    """
    logger = logging.getLogger("mcp_server")
    logger.setLevel(getattr(logging, config.LOG_LEVEL.upper()))
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler for stdout output
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, config.LOG_LEVEL.upper()))
    
    # Create formatter with timestamp and level
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger

# Global logger instance
logger = setup_logger()
