import 'dotenv/config';
import { z } from 'zod';
export const env=z.object({NODE_ENV:z.string().default('development'),PORT:z.coerce.number().default(4000),DATABASE_URL:z.string(),JWT_SECRET:z.string().min(16),AI_SERVICE_URL:z.string().url(),CORS_ORIGIN:z.string()}).parse(process.env);
