from collections import defaultdict

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import SessionLocal
from app.models import OrganizationNode

router = APIRouter(prefix="/api/v1", tags=["organization"])


def _load_nodes() -> list[OrganizationNode]:
    with SessionLocal() as session:
        return list(
            session.scalars(
                select(OrganizationNode)
                .where(OrganizationNode.is_active.is_(True))
                .order_by(OrganizationNode.sort_order, OrganizationNode.id)
            ).all()
        )


def _serialize(node: OrganizationNode) -> dict:
    return {
        "code": node.code,
        "name": node.name,
        "node_type": node.node_type,
        "title": node.title,
        "description": node.description,
        "autonomy_level": node.autonomy_level,
        "approval_required": node.approval_required,
        "children": [],
    }


@router.get("/organization")
def get_organization() -> dict:
    try:
        nodes = _load_nodes()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Organization data unavailable") from exc

    by_parent: dict[int | None, list[OrganizationNode]] = defaultdict(list)
    for node in nodes:
        by_parent[node.parent_id].append(node)

    def build(node: OrganizationNode) -> dict:
        result = _serialize(node)
        result["children"] = [build(child) for child in by_parent[node.id]]
        return result

    roots = by_parent[None]
    if not roots:
        raise HTTPException(status_code=404, detail="Organization has not been initialized")
    return {"items": [build(root) for root in roots]}


@router.get("/agents")
def list_agents() -> dict:
    try:
        nodes = _load_nodes()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Agent directory unavailable") from exc

    agents = [_serialize(node) for node in nodes if node.node_type == "agent"]
    return {"items": agents, "total": len(agents)}
