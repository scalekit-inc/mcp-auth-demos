require 'jwt'
require 'net/http'
require 'json'

class ScalekitTokenValidator
  JWKS_CACHE_TTL = 3600

  AuthenticationError    = Class.new(StandardError)
  InsufficientScopeError = Class.new(StandardError)

  @jwks_cache     = nil
  @jwks_cached_at = nil
  @jwks_uri       = nil
  @cache_mutex    = Mutex.new  # guards jwks_cache
  @uri_mutex      = Mutex.new  # guards jwks_uri discovery

  class << self
    attr_accessor :jwks_cache, :jwks_cached_at, :jwks_uri, :cache_mutex, :uri_mutex
  end

  def validate!(token, required_scopes: [])
    payload = decode_token(token)
    check_scopes!(payload, required_scopes) if required_scopes.any?
    payload
  end

  private

  def decode_token(token)
    payload, _header = JWT.decode(
      token, nil, true,
      algorithms:  ['RS256'],
      jwks:        { keys: fetch_jwks },
      iss:         ENV.fetch('SK_ENV_URL'),
      verify_iss:  true,
      verify_aud:  false  # manual check — token aud is an array
    )

    expected_aud = ENV.fetch('MCP_SERVER_ID')
    token_auds   = Array(payload['aud'])
    unless token_auds.include?(expected_aud)
      raise AuthenticationError, "Audience mismatch: expected #{expected_aud}, got #{token_auds.inspect}"
    end

    payload
  rescue JWT::DecodeError => e
    raise AuthenticationError, e.message
  end

  def fetch_jwks
    c = self.class
    return c.jwks_cache if c.jwks_cache && (Time.now - c.jwks_cached_at) < JWKS_CACHE_TTL

    # Resolve URI before acquiring cache_mutex — jwks_uri uses uri_mutex (different lock)
    uri = resolve_jwks_uri

    c.cache_mutex.synchronize do
      return c.jwks_cache if c.jwks_cache && (Time.now - c.jwks_cached_at) < JWKS_CACHE_TTL

      c.jwks_cache     = get_json(uri)['keys']
      c.jwks_cached_at = Time.now
    end
    c.jwks_cache
  end

  def resolve_jwks_uri
    c = self.class
    return c.jwks_uri if c.jwks_uri

    c.uri_mutex.synchronize do
      return c.jwks_uri if c.jwks_uri

      auth_server = JSON.parse(ENV.fetch('PROTECTED_RESOURCE_METADATA'))['authorization_servers']&.first
      raise AuthenticationError, 'No authorization_servers in PROTECTED_RESOURCE_METADATA' unless auth_server

      metadata    = get_json("#{auth_server}/.well-known/oauth-authorization-server")
      c.jwks_uri  = metadata['jwks_uri']
      raise AuthenticationError, 'jwks_uri missing from authorization server metadata' unless c.jwks_uri

      Rails.logger.info "[ScalekitTokenValidator] discovered jwks_uri=#{c.jwks_uri}"
    end
    c.jwks_uri
  end

  def get_json(url)
    uri  = URI(url)
    resp = Net::HTTP.get_response(uri)
    raise AuthenticationError, "HTTP #{resp.code} fetching #{url}" unless resp.is_a?(Net::HTTPSuccess)
    JSON.parse(resp.body)
  end

  def check_scopes!(payload, required_scopes)
    token_scopes = payload['scope']&.split(' ') || []
    missing      = required_scopes - token_scopes
    raise InsufficientScopeError, "Missing scopes: #{missing.join(', ')}" if missing.any?
  end
end
