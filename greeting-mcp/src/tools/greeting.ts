import { McpServer, RegisteredTool } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { logger } from '../lib/logger.js';
import { TOOLS } from './index.js';

export function registerGreetingTools(server: McpServer){
    TOOLS.greet_user.registeredTool = greetUserTool(server)
}

function greetUserTool(server: McpServer): RegisteredTool {
  return server.tool(
    TOOLS.greet_user.name,
    TOOLS.greet_user.description,
    {
      name: z.string().min(1, 'Name is required'),
    },
    async ({ name }) => {
      logger.info(`Invoked greet_user tool for name: ${name}`);
      return {content: [{type: 'text',text: `Hi ${name}`}],};
    });
}
