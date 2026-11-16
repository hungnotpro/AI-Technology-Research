# ATR-001 — Project Foundation

## Objective

Create a reproducible local development foundation for the ATR web dashboard, API, and PostgreSQL database.

## In scope

- React + TypeScript + Vite dashboard shell
- FastAPI service with root and health endpoints
- PostgreSQL 16 service in Docker Compose
- Environment variable template and ignore rules
- API smoke tests
- GitHub Actions API test and frontend build jobs

## Explicitly out of scope

- Agent runtime and LLM provider integration
- Agent memory, vector database, Redis
- Business workflows and task orchestration
- Hardware interfaces or drone control
- Production deployment

## Acceptance checklist

- [ ] Docker Compose builds and starts all three services
- [ ] API responds at `GET /health` with HTTP 200
- [ ] Dashboard loads at port 5173 and displays API connection state
- [ ] PostgreSQL health check passes
- [ ] API tests pass
- [ ] Frontend TypeScript build passes
- [ ] GitHub Actions workflow is green
- [ ] No credentials or real secrets are committed
- [ ] README setup instructions are verified on a clean machine

## Risks / notes

- The local default database password is a development placeholder only. Replace it for any shared environment.
- The Vite development server is used in this first milestone; production serving will be designed separately.
- A successful CI build does not prove Docker runtime behavior. The full Compose acceptance check must be run in a Docker-capable environment.

## Completion rule

ATR-001 is complete only after every acceptance item has evidence. File creation alone does not count as a passed test.
