from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
