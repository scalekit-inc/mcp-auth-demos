class InspectTokenTool < MCP::Tool
  description 'Extracts and logs a specific claim from the access token. ' \
              'Pass a claim key (e.g. "sub", "email", "org_id") to inspect it. ' \
              'Omit the key to see all available claims.'

  input_schema(
    properties: {
      claim_key: {
        type:        'string',
        description: 'The JWT claim key to extract (e.g. "sub", "email", "org_id"). Omit to list all claims.'
      }
    },
    required: ['claim_key']
  )

  def self.call(claim_key:, server_context:)
    claims = Thread.current.thread_variable_get(:scalekit_claims) || {}

    value = claims[claim_key]

    # Log the extracted claim — useful for debugging custom claims in production
    Rails.logger.info "[InspectToken] claim=#{claim_key.inspect} value=#{value.inspect}"

    if value.nil?
      available = claims.keys.join(', ')
      text = "Claim '#{claim_key}' not found in token.\nAvailable claims: #{available}"
    else
      text = "#{claim_key}: #{value}"
    end

    MCP::Tool::Response.new([{ type: 'text', text: text }])
  end
end
