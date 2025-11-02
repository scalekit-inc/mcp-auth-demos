import winston from 'winston';
import { config } from '../config/config.js';

export const logger = winston.createLogger({
  level: config.logLevel,
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.printf(({ level, message, timestamp, ...metadata }) => {
      const meta = Object.keys(metadata).length ? ` ${JSON.stringify(metadata)}` : '';
      return `[${timestamp}] ${level.toUpperCase()}: ${message}${meta}`;
    })
  ),
  transports: [
    new winston.transports.Console(),
  ],
});
