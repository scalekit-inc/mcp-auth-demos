import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express from 'express';
import { logger } from './logger.js';

export const setupTransportRoutes = (
  app: express.Express,
  server: McpServer
) => {
  // Handle both root and /mcp endpoints for compatibility
  app.post(['/', '/mcp'], async (req, res) => {
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined, // stateless
    });

    try {
      logger.info('Transport: Processing MCP request', {
        method: req.body?.method,
        id: req.body?.id
      });

      await server.connect(transport);
      await transport.handleRequest(req, res, req.body);

      logger.info('Transport: Request handled successfully', {
        method: req.body?.method,
        id: req.body?.id,
        responseHeadersSent: res.headersSent
      });
    } catch (error) {
      logger.error('Transport error:', error);
      if (!res.headersSent) {
        res.status(500).json({
          jsonrpc: '2.0',
          error: {
            code: -32603,
            message: 'Internal server error',
          },
          id: null,
        });
      }
    }
  });
};