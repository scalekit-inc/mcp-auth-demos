import { Scalekit } from '@scalekit-sdk/node';
import { config } from '../config/config.js';

export const scalekit = new Scalekit(config.skEnvUrl, config.skClientId, config.skClientSecret);
