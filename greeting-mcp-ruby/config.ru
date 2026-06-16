require_relative 'config/environment'
require 'mcp'
require 'rack/cors'
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

router = ->(env) {
  env['PATH_INFO'].start_with?('/.well-known', '/health') ?
    Rails.application.call(env) :
    mcp_with_auth.call(env)
}

# CORS wraps the entire app so both public endpoints and MCP requests get headers
run Rack::Builder.new {
  use Rack::Cors do
    allow do
      origins '*'
      resource '*',
        headers: :any,
        methods: %i[get post options],
        expose:  ['WWW-Authenticate']
    end
  end
  run router
}
