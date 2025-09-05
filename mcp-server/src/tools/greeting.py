"""
Greeting Tools Implementation

This module implements the greeting tools for the MCP server using the MCP SDK,
following the same pattern as the TypeScript greeting-mcp example.
"""

from mcp.server import Server
from src.lib.logger import logger
from src.tools.index import TOOLS

def register_greeting_tools(server: Server):
    """
    Register greeting tools with the MCP server using the MCP SDK.

    This function registers the greet_user tool using the server.call_tool method,
    similar to how the TypeScript version uses server.tool().
    """
    TOOLS["greet_user"]["registered_tool"] = greet_user_tool(server)

def greet_user_tool(server: Server):
    """
    Create and return the greet_user tool, similar to TypeScript pattern.
    """
    @server.call_tool()
    async def greet_user(name: str) -> dict:
        """
        Greet a user with a personalized message.

        Args:
            name: The name of the user to greet

        Returns:
            A dictionary containing the greeting message
        """
        logger.info(f"Invoked greet_user tool for name: {name}")
        greeting = f"Hi {name}, welcome to Scalekit!"
        return {
            "content": [
                {
                    "type": "text",
                    "text": greeting
                }
            ]
        }
    
    return greet_user
