import { Pool, PoolClient, QueryResultRow } from "pg";
import { env } from '../config/env.js';

export const pool = new Pool({
  connectionString: env.DATABASE_URL,
  max: 10
});

export async function query<T extends QueryResultRow = QueryResultRow>(
  text: string,
  values: unknown[] = []
) {
  return pool.query<T>(text, values);
}

export async function withTransaction<T>(
  fn: (client: PoolClient) => Promise<T>
) {
  const c = await pool.connect();

  try {
    await c.query('BEGIN');
    const out = await fn(c);
    await c.query('COMMIT');
    return out;
  } catch (e) {
    await c.query('ROLLBACK');
    throw e;
  } finally {
    c.release();
  }
}

export async function healthDb() {
  const r = await pool.query<{ now: string }>('SELECT NOW() AS now');
  return { ok: true, now: r.rows[0].now };
}
