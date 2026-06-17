import { McpServer, RegisteredTool } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { requestContext } from '../lib/context.js';
import { logger } from '../lib/logger.js';
import { TOOLS } from './index.js';

export function registerGreetingTools(server: McpServer) {
  greetUserTool(server);
}

function greetUserTool(server: McpServer): RegisteredTool {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return (server as any).tool(
    TOOLS.greet_user.name,
    TOOLS.greet_user.description,
    { name: z.string().min(1, 'Name is required') },
    async ({ name }: { name: string }) => {
      const claims = requestContext.getStore()?.claims ?? {};
      const orgName = (claims.custom_claims as Record<string, unknown>)?.org_name as string | undefined;
      logger.info(`Invoked greet_user tool for name: ${name}`, { org: orgName });

      const greeting = orgName
        ? `Hi ${name}, welcome from ${orgName}!`
        : `Hi ${name}!`;

      return { content: [{ type: 'text', text: greeting }] };
    }
  ) as RegisteredTool;
}
