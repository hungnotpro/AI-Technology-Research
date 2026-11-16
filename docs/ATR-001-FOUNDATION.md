# ATR-001 — Project Foundation

## Objective

Create a reproducible local development foundation for the ATR web dashboard, API, and PostgreSQL database.

## In scope

- React + TypeScript + Vite dashboard shell
- FastAPI service with liveness and database-readiness endpoints
- PostgreSQL 16 service in Docker Compose
- SQLAlchemy 2 database engine and declarative model base
- Alembic migration configuration and initial system settings migration
- Environment variable template and ignore rules
- API tests for health and readiness behavior
- GitHub Actions API test and frontend build jobs

## Explicitly out of scope

- Agent runtime and LLM provider integration
- Agent memory, vector database, Redis
- Business workflows and task orchestration
- Hardware interfaces or drone control
- Production deployment

## Acceptance checklist

- [x] Docker Compose builds and starts all three services (Owner verified locally)
- [x] API responds at GET /health with HTTP 200 (dashboard shows API connected)
- [x] Dashboard loads at port 5173 and displays API connection state (Owner verified locally)
- [x] PostgreSQL health check passes (Owner screenshot shows Healthy)
- [x] API container connects to PostgreSQL and executes SELECT 1 (Owner verified)
- [ ] GET /health/ready reports database readiness
- [ ] Alembic initial migration applies successfully
- [ ] API tests pass after database readiness tests are added
- [ ] Frontend TypeScript build passes in GitHub Actions
- [ ] GitHub Actions workflow is green for this change
- [ ] No credentials or real secrets are committed (final repository audit pending)
- [ ] README setup instructions are verified on a clean machine

## Risks / notes

- The local default database password is a development placeholder only. Replace it for any shared environment.
- The Vite development server is used in this first milestone; production serving will be designed separately.
- A successful CI build does not prove Docker runtime behavior. The full Compose acceptance check must be run in a Docker-capable environment.
- Database schema changes must be delivered through Alembic migrations; do not use automatic table creation in application startup.

## Completion rule

ATR-001 is complete only after every acceptance item has evidence. File creation alone does not count as a passed test.
