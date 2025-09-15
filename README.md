# MCP Demo: Node.js & Python Servers

This repository demonstrates secure, production-ready Model Context Protocol (MCP) servers implemented in both Node.js and Python, with full integration to the Scalekit platform for authentication, authorization, and dynamic client registration.

## Repository Structure

- `greeting-mcp-node/`  
  Node.js (TypeScript) implementation of an MCP server with Scalekit authentication and permissioned tool access.
- `greeting-mcp-python/`  
  Python (FastAPI + FastMCP) implementation of an MCP server with Scalekit authentication and permissioned tool access.

Each subdirectory contains its own README with detailed setup and usage instructions.

## Features

- **Scalekit OAuth 2.1 Authentication**: Secure, standards-based authentication and authorization for all MCP requests.
- **Dynamic Client Registration**: Register MCP servers with Scalekit for secure, permissioned access.
- **Tool-Based Architecture**: Easily extend with new tools and permissions.
- **Production-Ready**: Includes logging, CORS, and environment-based configuration.

## Quick Start

See the README in each subproject for setup instructions:

- [Node.js MCP Server](./greeting-mcp-node/README.md)
- [Python MCP Server](./greeting-mcp-python/README.md)

## License

This repository is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

## Learn More

- [Scalekit Documentation](https://docs.scalekit.com/guides/mcp/overview/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.org/)
