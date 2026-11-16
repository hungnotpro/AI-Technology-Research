# AI Technology Research (ATR)

ATR is a small AI-agent engineering workspace focused on research and development in drones and IoT.

## Current milestone

**ATR-001 — Project Foundation**

This milestone establishes a runnable web/API/database development environment. Agent orchestration and LLM integrations are intentionally out of scope until the foundation is verified.

## Architecture

- Web: React + TypeScript + Vite
- API: Python + FastAPI
- Database: PostgreSQL
- Local environment: Docker Compose
- CI: GitHub Actions

## Repository layout

```text
apps/
  api/       FastAPI service
  web/       React dashboard
infra/
  docker/    Container-related configuration
.github/
  workflows/ CI workflows
docs/        Architecture and delivery notes
```

## Quick start

1. Copy `.env.example` to `.env`.
2. Start the stack:

   ```bash
   docker compose up --build
   ```

3. Open:
   - Dashboard: http://localhost:5173
   - API health: http://localhost:8000/health
   - API docs: http://localhost:8000/docs
   - PostgreSQL: localhost:5432

Stop the stack with `docker compose down`. Add `-v` only when you intentionally want to delete the local database volume.

## Development without Docker

API:

```bash
cd apps/api
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Web:

```bash
cd apps/web
npm install
npm run dev
```

## Safety and governance

ATR may research, plan, draft code, and prepare engineering artifacts. Actions with real-world impact require explicit Owner approval. This includes purchases, payments, hardware control, firmware flashing, motor tests, drone flights, production deployment, and destructive data operations.

Never test propellers while attached to motors on a bench. Hardware and flight testing must use appropriate supervision and applicable regulations.

## Delivery status

See [docs/ATR-001-FOUNDATION.md](docs/ATR-001-FOUNDATION.md) for the first milestone acceptance checklist.
