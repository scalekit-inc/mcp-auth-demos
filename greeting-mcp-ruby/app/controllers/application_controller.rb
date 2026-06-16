class ApplicationController < ActionController::API
  before_action :authenticate_request!

  private

  def authenticate_request!
    token = extract_bearer_token
    return render_unauthorized('Bearer token required') unless token

    @current_claims = validator.validate!(token)
  rescue ScalekitTokenValidator::AuthenticationError => e
    render_unauthorized(e.message)
  end

  def require_scopes!(*scopes)
    validator.validate!(extract_bearer_token, required_scopes: scopes)
  rescue ScalekitTokenValidator::InsufficientScopeError => e
    render json: { error: 'insufficient_scope', message: e.message }, status: :forbidden
    false
  end

  def extract_bearer_token
    header = request.headers['Authorization']
    header&.start_with?('Bearer ') ? header.sub('Bearer ', '').strip : nil
  end

  def render_unauthorized(message)
    response.headers['WWW-Authenticate'] =
      "Bearer resource_metadata=\"#{ENV.fetch('MCP_SERVER_ID', '')}/.well-known/oauth-protected-resource\""
    render json: { error: 'unauthorized', message: message }, status: :unauthorized
  end

  def validator
    @validator ||= ScalekitTokenValidator.new
  end
end
