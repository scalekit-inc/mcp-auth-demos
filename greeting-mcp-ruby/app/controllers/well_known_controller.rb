class WellKnownController < ActionController::API
  # Public — no auth. MCP clients call this to discover the OAuth server.
  def oauth_protected_resource
    metadata = JSON.parse(ENV.fetch('PROTECTED_RESOURCE_METADATA'))
    render json: metadata
  end

  def health
    render json: { status: 'ok', server: 'scalekit-mcp-rails' }
  end
end
