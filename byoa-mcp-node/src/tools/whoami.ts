import { McpServer, RegisteredTool } from '@modelcontextprotocol/sdk/server/mcp.js';
import { requestContext } from '../lib/context.js';
import { logger } from '../lib/logger.js';

export function registerWhoamiTools(server: McpServer) {
  whoamiTool(server);
}

function whoamiTool(server: McpServer): RegisteredTool {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return (server as any).tool(
    'whoami',
    'Returns the identity and custom claims of the authenticated caller from the access token.',
    {},
    async () => {
      const claims = requestContext.getStore()?.claims ?? {};
      logger.info('whoami invoked', { sub: claims.sub });

      const identity = {
        sub: claims.sub,
        email: claims.email,
        org_id: (claims.custom_claims as Record<string, unknown>)?.org_id,
        org_name: (claims.custom_claims as Record<string, unknown>)?.org_name,
        token_issued_at: claims.iat ? new Date(claims.iat * 1000).toISOString() : undefined,
        token_expires_at: claims.exp ? new Date(claims.exp * 1000).toISOString() : undefined,
      };

      return {
        content: [{ type: 'text', text: JSON.stringify(identity, null, 2) }],
      };
    }
  ) as RegisteredTool;
}
