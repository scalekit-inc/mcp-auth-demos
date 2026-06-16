require 'json'

class ScalekitBearerAuth
  def initialize(app)
    @app       = app
    @validator = ScalekitTokenValidator.new
  end

  def call(env)
    token = extract_token(env['HTTP_AUTHORIZATION'])
    return unauthorized('Bearer token required') unless token

    claims = @validator.validate!(token)
    Thread.current.thread_variable_set(:scalekit_claims, claims)
    env['scalekit.claims'] = claims
    @app.call(env)
  rescue ScalekitTokenValidator::AuthenticationError => e
    unauthorized(e.message)
  ensure
    Thread.current.thread_variable_set(:scalekit_claims, nil)
  end

  private

  def extract_token(header)
    header&.start_with?('Bearer ') ? header.sub('Bearer ', '').strip : nil
  end

  def unauthorized(message)
    resource_url = ENV.fetch('MCP_SERVER_ID', '')
    [401,
     { 'Content-Type' => 'application/json',
       'WWW-Authenticate' => "Bearer resource_metadata=\"#{resource_url}/.well-known/oauth-protected-resource\"" },
     [JSON.generate({ error: 'unauthorized', message: message })]]
  end
end
