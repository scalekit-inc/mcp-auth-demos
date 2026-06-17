import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { registerGreetingTools } from './greeting.js';
import { registerWhoamiTools } from './whoami.js';

const toolsList = {
  greet_user: {
    name: 'greet_user',
    description: 'Greets the user with a personalized message.',
    requiredScopes: [],
  },
  whoami: {
    name: 'whoami',
    description: 'Returns the identity and custom claims of the authenticated caller from the access token.',
    requiredScopes: [],
  },
} as const;

export type ToolKey = keyof typeof toolsList;

export type ToolDefinition = {
  name: ToolKey;
  description: string;
  requiredScopes: string[];
};

export const TOOLS: { [K in ToolKey]: ToolDefinition & { name: K } } = Object.fromEntries(
  Object.entries(toolsList).map(([key, val]) => [
    key,
    { ...val, name: key, requiredScopes: [...val.requiredScopes] } as ToolDefinition & { name: typeof key },
  ])
) as any;

export function registerTools(server: McpServer) {
  registerGreetingTools(server);
  registerWhoamiTools(server);
}
