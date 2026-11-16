from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_service_status() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": "atr-api", "status": "running"}


def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "atr-api"}


def test_readiness_returns_database_connected() -> None:
    with patch("app.main.check_database_connection", return_value=True):
        response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "connected"}


def test_readiness_returns_503_when_database_is_unavailable() -> None:
    with patch("app.main.check_database_connection", side_effect=RuntimeError("offline")):
        response = client.get("/health/ready")
    assert response.status_code == 503
    assert response.json()["detail"]["database"] == "unavailable"
