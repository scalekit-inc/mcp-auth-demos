import { NextFunction, Request, Response } from 'express';
import { config } from '../config/config.js';
import { requestContext, TokenClaims } from './context.js';
import { logger } from './logger.js';
import { scalekit } from './scalekit.js';

const EXPECTED_AUDIENCE = config.expectedAudience;
export const WWWHeader = {
  HeaderKey: 'WWW-Authenticate',
  HeaderValue: `Bearer realm="OAuth", resource_metadata="http://localhost:${config.port}/.well-known/oauth-protected-resource"`,
};

export async function authMiddleware(req: Request, res: Response, next: NextFunction) {
  try {
    if (req.path.startsWith('/.well-known') || req.path.startsWith('/login')) {
      return next();
    }

    const authHeader = req.headers['authorization'];
    const token = authHeader?.startsWith('Bearer ') ? authHeader.split('Bearer ')[1]?.trim() : null;

    if (!token) {
      logger.warn('Missing Bearer token', { path: req.path, method: req.method });
      throw new Error('Missing or invalid Bearer token');
    }

    const claims = await scalekit.validateToken<TokenClaims>(token, { audience: [EXPECTED_AUDIENCE] });

    // Store decoded claims in the request-scoped context so tool handlers can access them.
    const store = requestContext.getStore();
    if (store) store.claims = claims;

    logger.info('Authentication successful');
    next();
  } catch (err) {
    logger.warn('Unauthorized request', { error: err instanceof Error ? err.message : String(err) });
    return res.status(401).set(WWWHeader.HeaderKey, WWWHeader.HeaderValue).end();
  }
}
