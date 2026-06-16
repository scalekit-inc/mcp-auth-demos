require_relative 'config/environment'
require 'mcp'
require_relative 'lib/scalekit_token_validator'
require_relative 'app/middleware/scalekit_bearer_auth'
require_relative 'app/tools/who_am_i_tool'
require_relative 'app/tools/greet_user_tool'
require_relative 'app/tools/inspect_token_tool'

mcp_server = MCP::Server.new(
  name:    'scalekit-mcp-rails',
  version: '1.0.0',
  tools:   [WhoAmITool, GreetUserTool, InspectTokenTool]
)
mcp_transport = MCP::Server::Transports::StreamableHTTPTransport.new(mcp_server, stateless: true)

mcp_with_auth = Rack::Builder.new do
  use ScalekitBearerAuth
  run mcp_transport
end

# Public paths → Rails (well-known discovery + health)
# Everything else → MCP transport with auth
run ->(env) {
  env['PATH_INFO'].start_with?('/.well-known', '/health') ?
    Rails.application.call(env) :
    mcp_with_auth.call(env)
}
