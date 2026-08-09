import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';

import cors from 'cors';
import express from 'express';
import { config } from './config/config.js';
import { oauthProtectedResourceHandler } from './lib/auth.js';
import { logger } from './lib/logger.js';
import { authMiddleware } from './lib/middleware.js';
import { setupTransportRoutes } from './lib/transport.js';
import { registerTools } from './tools/index.js';

// Add global error handling
process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
    logger.error('Unhandled Rejection', { reason, promise });
});

process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
    logger.error('Uncaught Exception', { error: error.message, stack: error.stack });
    process.exit(1);
});

const PORT = config.port;
const server = new McpServer({ name: config.serverName, version: config.serverVersion });

const app = express();

const allowAll = cors({
  origin: (origin, cb) => cb(null, true),
  credentials: false,
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Mcp-Protocol-Version', 'Content-Type', 'Authorization'],
  exposedHeaders: ['WWW-Authenticate'],
  maxAge: 86400,
});

app.options(/.*/, allowAll);
app.use(allowAll);

app.use(express.json());

// Add a simple logging middleware to debug
app.use((req, res, next) => {
    console.log('=== REQUEST RECEIVED ===', {
        method: req.method,
        path: req.path,
        url: req.url,
        headers: req.headers,
        body: req.body
    });
    next();
});

app.use(authMiddleware);

app.get('/.well-known/oauth-protected-resource', oauthProtectedResourceHandler);

try {
    setupTransportRoutes(app, server);
    logger.info('Transport routes set up successfully');

    registerTools(server);
    logger.info('Registered tools successfully');

    const serverInstance = app.listen(PORT, () => {
        logger.info(`MCP server running on http://localhost:${PORT}`);
        console.log(`🚀 MCP Server is running and should stay alive. Port: ${PORT}`);
    });

    // Keep the process alive
    serverInstance.on('error', (error) => {
        console.error('Server error:', error);
        logger.error('Server error', { error: error.message });
    });

    // Prevent process from exiting
    process.on('SIGINT', () => {
        console.log('\n🛑 Received SIGINT, shutting down gracefully...');
        serverInstance.close(() => {
            logger.info('Server closed');
            process.exit(0);
        });
    });

    process.on('SIGTERM', () => {
        console.log('\n🛑 Received SIGTERM, shutting down gracefully...');
        serverInstance.close(() => {
            logger.info('Server closed');
            process.exit(0);
        });
    });

    // Add keep-alive interval
    setInterval(() => {
        // This interval keeps the Node.js event loop alive
        logger.debug('Server keep-alive ping');
    }, 30000); // Every 30 seconds
} catch (error) {
    console.error('Error during server startup:', error);
    logger.error('Server startup failed', { error: error instanceof Error ? error.message : String(error) });
    process.exit(1);
}