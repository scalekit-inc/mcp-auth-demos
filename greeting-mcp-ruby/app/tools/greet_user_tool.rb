class GreetUserTool < MCP::Tool
  description 'Greets the user with a personalized message.'

  input_schema(
    properties: { name: { type: 'string', description: 'The name to greet' } },
    required: ['name']
  )

  def self.call(name:, server_context:)
    MCP::Tool::Response.new([{ type: 'text', text: "Hi #{name}, welcome to Scalekit!" }])
  end
end
