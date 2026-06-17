import { AsyncLocalStorage } from 'async_hooks';

export type TokenClaims = {
  sub?: string;
  email?: string;
  iss?: string;
  aud?: string | string[];
  exp?: number;
  nbf?: number;
  iat?: number;
  custom_claims?: Record<string, unknown>;
  [key: string]: unknown;
};

export type RequestStore = {
  claims: TokenClaims;
};

export const requestContext = new AsyncLocalStorage<RequestStore>();
