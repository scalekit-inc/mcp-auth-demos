# MCP Auth Demos: Node.js, Python & Ruby Servers

This repository demonstrates secure, production-ready Model Context Protocol (MCP) servers in Node.js, Python, and Ruby on Rails, with full integration to the Scalekit platform for OAuth 2.1 authentication and dynamic client registration.

## Repository Structure

- `greeting-mcp-node/`
  Node.js (TypeScript) implementation of an MCP server with Scalekit authentication and permissioned tool access.
- `greeting-mcp-python/`
  Python (FastAPI + FastMCP) implementation of an MCP server with Scalekit authentication and permissioned tool access.
- `greeting-mcp-ruby/`
  Ruby on Rails implementation of an MCP server with Scalekit OAuth 2.1 authentication. Uses the official MCP Ruby SDK with JWKS-based token validation — no client secret required.

Each subdirectory contains its own README with detailed setup and usage instructions.

## Features

- **Scalekit OAuth 2.1 Authentication**: Secure, standards-based authentication and authorization for all MCP requests.
- **Dynamic Client Registration**: Register MCP servers with Scalekit for secure, permissioned access.
- **JWKS Token Validation**: RS256 signature verification via auto-discovered JWKS — no client secrets stored.
- **Tool-Based Architecture**: Easily extend with new tools and permissions.
- **Production-Ready**: Includes logging, CORS, and environment-based configuration.

## Quick Start

See the README in each subproject for setup instructions:

- [Node.js MCP Server](./greeting-mcp-node/README.md)
- [Python MCP Server](./greeting-mcp-python/README.md)
- [Ruby on Rails MCP Server](./greeting-mcp-ruby/README.md)

## License

This repository is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

## Learn More

- [Scalekit Documentation](https://docs.scalekit.com/guides/mcp/overview/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.org/)
