class WhoAmITool < MCP::Tool
  description 'Returns the sub from the authenticated token — verifies OAuth is wired up.'

  def self.call(server_context:)
    claims = Thread.current.thread_variable_get(:scalekit_claims) || {}
    MCP::Tool::Response.new([{ type: 'text', text: "sub: #{claims['sub']}" }])
  end
end
