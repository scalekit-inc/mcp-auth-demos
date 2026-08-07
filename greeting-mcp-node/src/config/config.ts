import dotenv from 'dotenv';
import fs from 'fs';

dotenv.config();

const metadataFile = process.env.PROTECTED_RESOURCE_METADATA_FILE;
let metadata = process.env.PROTECTED_RESOURCE_METADATA || '';
if (!metadata && metadataFile && fs.existsSync(metadataFile)) {
  metadata = fs.readFileSync(metadataFile, 'utf8');
}

export const config = {
  serverName: 'Greeting MCP',
  serverVersion: '1.0.0',
  port: process.env.PORT || Number(3002),
  skEnvUrl: process.env.SK_ENV_URL || '',
  skClientId: process.env.SK_CLIENT_ID || '',
  skClientSecret: process.env.SK_CLIENT_SECRET || '',
  logLevel: 'info',
  mcpServerId: process.env.MCP_SERVER_ID || '',
  protectedResourceMetadata: metadata,
  expectedAudience: process.env.EXPECTED_AUDIENCE || '',
};
