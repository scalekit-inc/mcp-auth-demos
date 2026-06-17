import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express from 'express';
import { logger } from './logger.js';
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';

// SDK 1.13+ enforces one transport per McpServer instance, so we create a fresh
// server per request for stateless operation.
export const setupTransportRoutes = (app: express.Express, createServer: () => McpServer) => {
  app.post('/', async (req, res) => {
    const server = createServer();
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined, // stateless
    });
    await server.connect(transport);
    res.on('close', () => {
      transport.close();
      server.close();
    });
    try {
      await transport.handleRequest(req, res, req.body);
    } catch (error) {
      logger.error('Transport error:', error);
    }
  });
};
