import { McpServer, RegisteredTool } from '@modelcontextprotocol/sdk/server/mcp.js';
import { registerGreetingTools } from './greeting.js';

const toolsList = {
  greet_user: {
    name: 'greet_user',
    description: 'Greets the user with a personalized message. This tool can be used to provide a friendly greeting based on the name of the user.',
    requiredScopes: ['usr:read'],
  },
} as const;

export type ToolKey = keyof typeof toolsList;

export type ToolDefinition = {
  name: ToolKey;
  description: string;
  registeredTool?: RegisteredTool;
  requiredScopes: string[];
};

export const TOOLS: { [K in ToolKey]: ToolDefinition & { name: K } } = Object.fromEntries(
Object.entries(toolsList).map(([key, val]) => [
    key,
    { ...val, name: key, requiredScopes: [...val.requiredScopes] } as ToolDefinition & { name: typeof key },
  ])
) as any;

export function registerTools(server: McpServer) {
    registerGreetingTools(server)
}