import dotenv from 'dotenv';

dotenv.config();

export const config = {
  serverName: 'Greeting MCP',
  serverVersion: '1.0.0',
  port: process.env.PORT || Number(3002),
  skEnvUrl: process.env.SK_ENV_URL || '',
  skClientId: process.env.SK_CLIENT_ID || '',
  skClientSecret: process.env.SK_CLIENT_SECRET || '',
  logLevel: 'info',
  mcpServerId: process.env.MCP_SERVER_ID || '',
  protectedResourceMetadata: process.env.PROTECTED_RESOURCE_METADATA || '',
};
