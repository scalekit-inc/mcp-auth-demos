import dotenv from 'dotenv';

dotenv.config();

export const config = {
  serverName: 'Greeting MCP',
  serverVersion: '1.0.0',
  port: process.env.PORT || Number(3002),
  skEnvUrl: process.env.SCALEKIT_ENVIRONMENT_URL || '',
  skClientId: process.env.SCALEKIT_CLIENT_ID || '',
  skClientSecret: process.env.SCALEKIT_CLIENT_SECRET || '',
  logLevel: 'info',
  // MCP Server Configuration - Update these values for your setup
  mcpServerId: process.env.MCP_SERVER_ID || 'greeting-mcp-server',
  // OAuth Protected Resource Metadata - Update with your actual metadata
  // This should be a minified JSON string with your OAuth configuration
  protectedResourceMetadata: process.env.PROTECTED_RESOURCE_METADATA || '{"resource":"greeting-mcp-server","authorization_servers":["https://your-scalekit-env.com"],"scopes_supported":["greeting"],"bearer_methods_supported":["header"],"resource_documentation":"https://docs.example.com/api/greeting"}',
  // Expected Audience - Update with your MCP server URL as registered in Scalekit dashboard
  expectedAudience: process.env.EXPECTED_AUDIENCE || 'http://localhost:3002',
};
