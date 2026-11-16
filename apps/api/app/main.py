from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import check_database_connection
from app.organization import router as organization_router

app = FastAPI(
    title="AI Technology Research API",
    version="0.1.0",
    description="Foundation API for the ATR engineering workspace.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"service": "atr-api", "status": "running"}


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "atr-api"}


@app.get("/health/ready", tags=["system"])
def readiness() -> dict[str, str]:
    try:
        check_database_connection()
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"status": "not_ready", "database": "unavailable"},
        ) from exc
    return {"status": "ready", "database": "connected"}


app.include_router(organization_router)
