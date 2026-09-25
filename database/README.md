# Database

PostgreSQL is the Phase 1 system-of-record database. `schema.sql` defines the relational entities in the supplied master prompt. Run with:

```bash
docker compose -f database/docker-compose.yml up -d
```

Then point `server/.env` at `postgres://postgres:postgres@localhost:5432/kissan_sathi`.
