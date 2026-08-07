import { Scalekit } from '@scalekit-sdk/node';
import { NextFunction, Request, Response } from 'express';
import { config } from '../config/config.js';

const scalekit = new Scalekit(config.skEnvUrl, config.skClientId, config.skClientSecret);

const RESOURCE_ID = config.expectedAudience;
const METADATA_URL = `${config.expectedAudience.replace(/\/$/, '')}/.well-known/oauth-protected-resource`;

export const WWWHeader = {
    key: 'WWW-Authenticate',
    value: `Bearer realm="OAuth", resource_metadata="${METADATA_URL}"`,
};

export async function authMiddleware(req: Request, res: Response, next: NextFunction) {
    try {
        // Allow metadata discovery to stay public
        if (req.path.includes('.well-known')) return next();

        const token = req.headers.authorization?.replace('Bearer ', '').trim();
        if (!token) throw new Error('Missing Bearer token');

        await scalekit.validateToken(token);
        return next();
    } catch {
        return res.status(401).set(WWWHeader.key, WWWHeader.value).end();
    }
}