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



from types import SimpleNamespace
from unittest.mock import patch


def _node(node_id, code, node_type, parent_id, sort_order=0):
    return SimpleNamespace(
        id=node_id,
        code=code,
        name=code,
        node_type=node_type,
        title=code,
        description=f"{code} description",
        parent_id=parent_id,
        autonomy_level="hybrid",
        approval_required=True,
        sort_order=sort_order,
        is_active=True,
    )


def test_agents_directory_returns_seeded_agents() -> None:
    nodes = [
        _node(1, "OWNER", "owner", None),
        _node(2, "ATR-CEO", "agent", 1),
        _node(3, "ATR-CTO", "agent", 2),
    ]
    with patch("app.organization._load_nodes", return_value=nodes):
        response = client.get("/api/v1/agents")
    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert [item["code"] for item in response.json()["items"]] == ["ATR-CEO", "ATR-CTO"]


def test_organization_endpoint_returns_hierarchy() -> None:
    nodes = [
        _node(1, "OWNER", "owner", None),
        _node(2, "ATR-CEO", "agent", 1),
        _node(3, "ATR-CTO", "agent", 2),
    ]
    with patch("app.organization._load_nodes", return_value=nodes):
        response = client.get("/api/v1/organization")
    assert response.status_code == 200
    owner = response.json()["items"][0]
    assert owner["code"] == "OWNER"
    assert owner["children"][0]["code"] == "ATR-CEO"
    assert owner["children"][0]["children"][0]["code"] == "ATR-CTO"
