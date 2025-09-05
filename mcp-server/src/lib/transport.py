"""
MCP Transport Layer

This module handles the HTTP transport for MCP (Model Context Protocol) communication.
It uses the MCP SDK's built-in transport capabilities, similar to the TypeScript version.
"""

import json
from fastapi import FastAPI, Request, Response
from mcp.server import Server
from src.lib.logger import logger


def setup_transport_routes(app: FastAPI, server: Server):
    """
    Setup MCP transport routes for HTTP communication.

    This function creates the main MCP endpoint that handles all MCP protocol
    communication using the MCP SDK's built-in transport, similar to TypeScript.
    """

    @app.post("/")
    async def handle_mcp_request(request: Request) -> Response:
        """
        Handle MCP requests via HTTP transport using MCP SDK.

        This endpoint processes MCP protocol requests using the SDK's transport layer.
        """
        try:
            # Parse incoming request body
            body = await request.json()
            logger.info(f"MCP Request: {body.get('method', 'unknown')} (ID: {body.get('id', 1)})")
            
            # Use MCP SDK's built-in request handling
            
            method = body.get('method', 'unknown')
            request_id = body.get('id', 1)
            params = body.get('params', {})
            
            # Handle MCP initialization
            if method == "initialize":
                logger.info("Handling MCP initialization")
                result = {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {
                        "logging": {},
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "Python MCP Server",
                        "version": "1.0.0"
                    }
                }
                response_data = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
                return Response(
                    content=json.dumps(response_data),
                    media_type="application/json"
                )
            
            # Handle tools/list
            elif method == "tools/list":
                logger.info("Handling tools/list request")
                from src.tools.index import TOOLS
                tools = []
                for tool_name, tool_def in TOOLS.items():
                    tools.append({
                        "name": tool_name,
                        "description": tool_def.get("description", ""),
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "The name of the user to greet"
                                }
                            },
                            "required": ["name"]
                        }
                    })
                
                response_data = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tools}
                }
                return Response(
                    content=json.dumps(response_data),
                    media_type="application/json"
                )
            
            # Handle tools/call
            elif method == "tools/call":
                tool_name = params.get("name", "")
                tool_args = params.get("arguments", {})
                logger.info(f"Handling tools/call request for tool: {tool_name}")
                
                if tool_name == "greet_user":
                    from src.tools.index import TOOLS
                    tool_function = TOOLS["greet_user"].get("registered_tool")
                    
                    if tool_function:
                        user_name = tool_args.get("name", "Anonymous")
                        logger.info(f"Executing greet_user tool for user: {user_name}")
                        result = await tool_function(user_name)
                        logger.info(f"Tool execution completed successfully")
                        
                        response_data = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": result
                        }
                        return Response(
                            content=json.dumps(response_data),
                            media_type="application/json"
                        )
                    else:
                        response_data = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {
                                "code": -32601,
                                "message": "Tool not registered"
                            }
                        }
                        return Response(
                            content=json.dumps(response_data),
                            media_type="application/json"
                        )
                else:
                    response_data = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": "Tool not found"
                        }
                    }
                    return Response(
                        content=json.dumps(response_data),
                        media_type="application/json"
                    )
            
            # Handle all other MCP methods
            logger.info(f"Acknowledging MCP method: {method}")
            response_data = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {}
            }
            return Response(
                content=json.dumps(response_data),
                media_type="application/json"
            )
            
        except Exception as error:
            logger.error(f"Transport error: {str(error)}")
            error_response = {
                "jsonrpc": "2.0",
                "id": 1,
                "error": {
                    "code": -32603,
                    "message": "Internal error"
                }
            }
            return Response(
                content=json.dumps(error_response),
                media_type="application/json",
                status_code=500
            )