"""
MCP Tools Registry

This module defines and registers all available MCP tools with their required
OAuth scopes. It follows the same pattern as the TypeScript greeting-mcp example.
"""

from typing import Dict, Any

# Tool definitions with OAuth scope requirements
tools_list = {
    "greet_user": {
        "name": "greet_user",
        "description": "Greets the user with a personalized message. This tool can be used to provide a friendly greeting based on the name of the user.",
        "required_scopes": ["usr:read"],  # Requires user read scope
    },
} 

# Type definitions for tool registry
ToolKey = str
ToolDefinition = Dict[str, Any]

# Create TOOLS dictionary with proper structure
TOOLS: Dict[ToolKey, ToolDefinition] = {
    key: {
        **val,
        "name": key,
        "required_scopes": val["required_scopes"].copy()
    }
    for key, val in tools_list.items()
}

def register_tools(server):
    """
    Register all available tools with the MCP server.
    
    This function initializes and registers all tools defined in the tools_list.
    Currently includes the greet_user tool with usr:read scope requirement.
    """
    from .greeting import register_greeting_tools
    
    # Register greeting tools
    register_greeting_tools(server)
