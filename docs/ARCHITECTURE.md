# Architecture

```text
                    +--------------------------+
                    | React + TypeScript/Vite |
                    | Farmer + Buyer portals  |
                    +------------+-------------+
                                 |
                                 v
                   +-------------+-------------+
                   | Node + Express + TS       |
                   | auth / marketplace /      |
                   | deals / payments / API    |
                   +------+------+--------------+
                          |      |
                SQL/ACID  |      | ML HTTP calls
                          v      v
                  +-------+--+ +--------+---------+
                  |Postgres | | FastAPI AI       |
                  |system of| | forecast/regime/  |
                  |record   | | ranking/decision |
                  +-------+-+ +------------------+
                          |
                       optional
                          v
                      MongoDB
                 AI features/snapshots

                 Redis = optional hot-cache
```

## Decision-engine flow

```text
market prices + arrivals + demand + weather + lot + offers
                        |
                 normalize units/names
                        |
                 validate / trust flags
                        |
          +-------------+-------------+
          |             |             |
       forecast      regime       shortage
          |             |             |
          +-------------+-------------+
                        |
             destination / buyer rank
                        |
           transport + storage + risk
                        |
             net realization engine
                        |
        SELL / WAIT / STORE / TRANSPORT
                        |
              explainable reasons
```

## Data ownership

PostgreSQL is the transactional source for users, profiles, markets, prices, lots, requirements, offers, deals, transport, storage, grievances, notifications, recommendations and risk records. MongoDB is reserved for variable AI feature payloads and simulation snapshots. Redis is optional for low-connectivity hot reads.
