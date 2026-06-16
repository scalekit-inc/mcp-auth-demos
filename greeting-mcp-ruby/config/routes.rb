Rails.application.routes.draw do
  get '/.well-known/oauth-protected-resource', to: 'well_known#oauth_protected_resource'
  get '/health', to: 'well_known#health'
end
