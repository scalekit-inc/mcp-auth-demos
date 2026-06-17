import { Request, Response } from 'express';
import { config } from '../config/config.js';
import { logger } from '../lib/logger.js';
import { scalekit } from '../lib/scalekit.js';
import { loginPage } from './template.js';

export function loginGetHandler(req: Request, res: Response) {
  const { login_request_id, state } = req.query as Record<string, string>;

  if (!login_request_id || !state) {
    res.status(400).send('Missing login_request_id or state');
    return;
  }

  res.setHeader('Content-Type', 'text/html');
  res.send(loginPage({ loginRequestId: login_request_id, state }));
}

export async function loginSubmitHandler(req: Request, res: Response) {
  const { email, password, login_request_id, state } = req.body as Record<string, string>;

  if (!login_request_id || !state) {
    res.status(400).send('Missing login_request_id or state');
    return;
  }

  if (!email || !password) {
    res.setHeader('Content-Type', 'text/html');
    res.send(loginPage({ loginRequestId: login_request_id, state, error: 'Email and password are required.' }));
    return;
  }

  // In a real app, validate the user's credentials against your auth system here.
  // This demo accepts any non-empty email and password to focus on the BYOA handshake.

  // After authenticating the user, look up whatever attributes you want to pass along —
  // org membership, roles, subscription tier, feature flags, anything your auth system knows.
  // Scalekit embeds these as custom claims in the issued access token so your MCP server
  // can read them on every request without an extra database call.
  const userAttributes = {
    org_id: 'org_acme_01',
    org_name: 'Acme Corp',
  };

  try {
    await scalekit.auth.updateLoginUserDetails(
      config.skConnectionId,
      login_request_id,
      {
        sub: email,
        email,
        customAttributes: userAttributes,
      }
    );

    const callbackUrl = `${config.skEnvUrl}/sso/v1/connections/${config.skConnectionId}/partner:callback?state=${encodeURIComponent(state)}`;
    logger.info(`Login successful for ${email}, redirecting to Scalekit callback`);
    res.redirect(callbackUrl);
  } catch (err) {
    logger.error('updateLoginUserDetails failed', { error: err instanceof Error ? err.message : String(err) });
    res.setHeader('Content-Type', 'text/html');
    res.send(loginPage({ loginRequestId: login_request_id, state, error: 'Login failed. Please try again.' }));
  }
}
