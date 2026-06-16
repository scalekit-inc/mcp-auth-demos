class InspectTokenTool < MCP::Tool
  description 'Returns the value of a specific JWT claim from the access token. ' \
              'If the claim key is not found, lists all available claim keys.'

  input_schema(
    properties: {
      claim_key: {
        type:        'string',
        description: 'The JWT claim key to extract (e.g. "sub", "email", "org_id")'
      }
    },
    required: ['claim_key']
  )

  def self.call(claim_key:, server_context:)
    claims = Thread.current.thread_variable_get(:scalekit_claims) || {}
    value  = claims[claim_key]

    if value.nil?
      available = claims.keys.join(', ')
      text = "Claim '#{claim_key}' not found in token.\nAvailable claims: #{available}"
    else
      text = "#{claim_key}: #{value}"
    end

    MCP::Tool::Response.new([{ type: 'text', text: text }])
  end
end
