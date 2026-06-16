require 'scalekit_token_validator'

# Eagerly validate required env vars at boot so missing config fails fast.
%w[SK_ENV_URL MCP_SERVER_ID PROTECTED_RESOURCE_METADATA].each do |var|
  raise "Missing required env var: #{var}" if ENV[var].blank?
end
