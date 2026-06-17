import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import cors from 'cors';
import express from 'express';
import { config } from './config/config.js';
import { oauthProtectedResourceHandler } from './lib/auth.js';
import { logger } from './lib/logger.js';
import { authMiddleware } from './lib/middleware.js';
import { setupTransportRoutes } from './lib/transport.js';
import { loginGetHandler, loginSubmitHandler } from './login/handler.js';
import { registerTools } from './tools/index.js';

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
app.use(express.urlencoded({ extended: false }));
app.use(authMiddleware);

app.get('/.well-known/oauth-protected-resource', oauthProtectedResourceHandler);

// BYOA: Scalekit redirects the user here to authenticate with your own login UI.
// After authentication, the handler posts user details back to Scalekit and redirects
// to Scalekit's callback to complete the OAuth flow.
app.get('/login', loginGetHandler);
app.post('/login/submit', loginSubmitHandler);

setupTransportRoutes(app, server);
logger.info('Transport routes set up successfully');

registerTools(server);
logger.info('Registered tools successfully');

app.listen(PORT, () => logger.info(`MCP server running on http://localhost:${PORT}`));
