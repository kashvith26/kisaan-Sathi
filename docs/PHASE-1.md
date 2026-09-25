# KISSAN SATHI — Phase 1 Architecture

## 1. Architecture overview

React/React Native clients call the Node + Express + TypeScript application layer. Node owns authentication, users, portal workflows, notifications, deal/payment/grievance orchestration and communication. Node calls a separate Python + FastAPI service for ML inference. PostgreSQL is the system of record for structured transactional entities; MongoDB is reserved for variable AI/feature payloads and simulation snapshots; Redis is optional for hot reads/cache and low-connectivity resilience.

```text
Farmer Web / Buyer Web / Future React Native
                  |
            Node + Express
      auth | business APIs | deals | payments | alerts
                  |
          -------------------
          |                 |
      PostgreSQL        FastAPI AI service
    transactional            |
                    LSTM | HMM | XGBoost | decision | bandit
          |
     MongoDB (AI docs/features) + Redis (optional cache)
```

## 2. Technology decisions

React + TypeScript + Vite + Tailwind/shadcn are the client direction; this Phase 1 skeleton uses a small CSS layer so the shell remains dependency-light while the component system can be added in Phase 2. Node + Express + TypeScript is the application/orchestration layer. FastAPI is the Python ML boundary so AI workloads can scale independently. PostgreSQL handles ACID relationships; MongoDB is appropriate only for flexible/semi-structured records, while Redis remains optional.

## 3. Database ER-style relationships

```text
users
 ├── 1:1 farmer_profiles
 ├── 1:1 buyer_profiles
 ├── 1:N farmer_lots ── N:1 crops
 ├── 1:N buyer_requirements ── N:1 crops
 ├── 1:N offers
 ├── 1:N deals
 ├── 1:N payments (through deals)
 ├── 1:N grievances
 └── 1:N notifications

markets 1:N market_prices N:1 crops
markets 1:N market_arrivals N:1 crops
farmer_lots 1:N buyer_matches N:1 buyer_requirements
farmer_lots 1:N deals N:1 users(buyer)
deals 1:N deal_negotiations
deals 1:N payments
transport_requests 1:N transport_bids N:1 transporters
transport_requests 1:N transport_trips N:1 transporters
warehouses 1:N storage_bookings N:1 farmer_lots
collective_pools aggregates multiple farmer lots in later phases
recommendations / simulations / risk_assessments reference farmer lots and users
```

## 4. Frontend structure

```text
client/src/
  components/ layouts/ pages/ features/ services/ hooks/ store/ types/ utils/
```

Routes are already wired for `/login`, `/farmer/*`, and `/buyer/*`; the portal shells expose the Phase 1 route map so later phases can add feature pages without changing the navigation contract.

## 5. Backend structure

```text
server/src/
  controllers/ routes/ services/ models/ middleware/ utils/ config/
```

Health, authentication, role enforcement and farmer/buyer portal stubs are implemented.

## 6. AI-service structure

```text
ai-service/app/
  models/       # LSTM, HMM, XGBoost, decision engine, bandit stubs
  services/     # reserved for feature/inference orchestration
  routes/       # health/model discovery now; inference routes in later phases
  schemas/      # Pydantic contracts
```

All five model boundaries exist as stubs and explicitly identify the phase that activates them.

## 7. API architecture

Phase 1 implements:

- `GET /api`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/farmer/dashboard` (authenticated farmer)
- `GET /api/buyer/dashboard` (authenticated buyer)
- `GET /health` (server + DB + AI connectivity)

The remaining endpoints from the master prompt are reserved with the same `/api/...` conventions for later phases.

## 8. Authentication architecture

JWT bearer tokens are issued by the server's Phase 1 stub login/register endpoints. Passwords are not persisted by the stub. Production implementation should hash credentials with bcrypt/Argon2, enforce rate limiting, use environment-managed secrets, validate payloads, and use role-based authorization. Never store real financial credentials.

## 9. Farmer portal architecture

The farmer shell is designed around: dashboard → crop lot → markets → forecast → shortage/opportunities → transport economics → buyers → what-if → storage → deals → payments → grievances → profile. The demo shell currently surfaces the Phase 1 soybean profile and marks intelligence modules as future phases.

## 10. Buyer portal architecture

Buyer shell: dashboard → requirements → farmers/lots → offers → deals → orders → transport → payments → grievances → profile. The navigation is separate from the farmer portal as required.

## 11. Core decision-engine architecture

```text
Agmarknet / e-NAM / Weather / Buyer demand / Farmer lot
                    |
          normalization + units
                    |
        validation + trust / anomaly flags
                    |
       +------------+-------------+
       |            |             |
     LSTM          HMM        demand/shortage
       |            |             |
       +------------+-------------+
                    |
        XGBoost destination/buyer rank
                    |
        transport cost + route risk
                    |
      storage + wastage + commission
                    |
       RL / decision-tree baseline
                    |
       net realization + confidence
                    |
 SELL LOCAL / MARKET X / WAIT / STORE / TRANSPORT / BUYER X / POOL
```

The exact net-realization contract is preserved from the master prompt: gross sale value less transport, loading, unloading, toll, commission, storage, packaging, handling, expected wastage/loss and other transaction costs. Explanations must expose the component deltas.

## 12. Data-flow diagram

```text
RAW DATA
  -> CLEANING
  -> NORMALIZATION
  -> VALIDATION / TRUST
  -> PRICE FORECAST (LSTM)
  -> MARKET REGIME (HMM)
  -> SHORTAGE / DEMAND DETECTION
  -> DESTINATION / BUYER RANKING (XGBoost) + BANDIT EXPLORATION
  -> LOGISTICS COST + TRANSPORT RISK
  -> SELL / WAIT / STORE / TRANSPORT DECISION
  -> NET REALIZATION
  -> EXPLAINABLE FINAL ACTION
```

## 13. Development commands

See `README.md`. Client uses Vite; server uses tsx/TypeScript; AI service uses Uvicorn/FastAPI; PostgreSQL is provisioned by Docker Compose.

## 14. Environment variables

### Client
`VITE_API_BASE_URL`

### Server
`NODE_ENV`, `PORT`, `DATABASE_URL`, `JWT_SECRET`, `AI_SERVICE_URL`, `CORS_ORIGIN`

### AI service
`AI_SERVICE_PORT`, `MODEL_MODE`

## 15. Phase 1 status / verification

- Client shell: implemented; buildable with npm dependencies installed.
- Server shell: implemented; TypeScript build/test configuration included.
- AI service: implemented; health/model-discovery endpoints plus five model stubs.
- Database: PostgreSQL schema + Docker Compose + runtime adapter implemented.
- Local DB verification harness: `pg-mem` test validates a PostgreSQL-compatible schema operation without Docker.

**Important environment limitation:** Docker/PostgreSQL is not installed in the current execution environment, so a live external PostgreSQL daemon cannot be started here. The repository is configured for a real PostgreSQL database and includes a one-command Docker Compose setup for that runtime dependency.
