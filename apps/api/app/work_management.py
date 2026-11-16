from datetime import datetime
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Milestone, OrganizationNode, Project, Task

router = APIRouter(prefix="/api/v1", tags=["work-management"])

ProjectStatus = Literal["planned", "active", "on_hold", "completed", "cancelled"]
Priority = Literal["low", "medium", "high", "critical"]
TaskStatus = Literal["backlog", "ready", "in_progress", "blocked", "in_review", "needs_revision", "done", "cancelled"]


class ProjectCreate(BaseModel):
    code: str = Field(min_length=2, max_length=40, pattern=r"^[A-Z0-9][A-Z0-9_-]+$")
    name: str = Field(min_length=2, max_length=180)
    description: str | None = None
    owner_node_code: str = "ATR-CEO"
    priority: Priority = "medium"
    target_date: datetime | None = None


class MilestoneCreate(BaseModel):
    code: str = Field(min_length=2, max_length=40)
    name: str = Field(min_length=2, max_length=180)
    description: str | None = None
    sort_order: int = 0
    target_date: datetime | None = None


class TaskCreate(BaseModel):
    code: str = Field(min_length=2, max_length=50, pattern=r"^[A-Z0-9][A-Z0-9_-]+$")
    title: str = Field(min_length=2, max_length=240)
    description: str | None = None
    milestone_id: int | None = None
    assigned_agent_code: str | None = None
    created_by_node_code: str = "ATR-PMO"
    priority: Priority = "medium"
    due_at: datetime | None = None


def _project_dict(p: Project) -> dict:
    return {"id": p.id, "code": p.code, "name": p.name, "description": p.description,
            "status": p.status, "priority": p.priority, "owner_node_id": p.owner_node_id,
            "target_date": p.target_date}


def _task_dict(t: Task) -> dict:
    return {"id": t.id, "project_id": t.project_id, "milestone_id": t.milestone_id,
            "code": t.code, "title": t.title, "description": t.description, "status": t.status,
            "priority": t.priority, "assigned_agent_id": t.assigned_agent_id,
            "created_by_node_id": t.created_by_node_id, "due_at": t.due_at}


@router.post("/projects", status_code=201)
def create_project(payload: ProjectCreate) -> dict:
    with SessionLocal() as session:
        owner = session.scalar(select(OrganizationNode).where(
            OrganizationNode.code == payload.owner_node_code,
            OrganizationNode.is_active.is_(True)))
        if owner is None:
            raise HTTPException(status_code=422, detail="Unknown or inactive project owner")
        if session.scalar(select(Project).where(Project.code == payload.code)):
            raise HTTPException(status_code=409, detail="Project code already exists")
        project = Project(code=payload.code, name=payload.name, description=payload.description,
                          owner_node_id=owner.id, priority=payload.priority, target_date=payload.target_date)
        session.add(project)
        session.commit()
        session.refresh(project)
        return _project_dict(project)


@router.get("/projects")
def list_projects() -> dict:
    with SessionLocal() as session:
        projects = session.scalars(select(Project).order_by(Project.created_at.desc())).all()
        return {"items": [_project_dict(p) for p in projects], "total": len(projects)}


@router.get("/projects/{project_id}")
def get_project(project_id: int) -> dict:
    with SessionLocal() as session:
        project = session.get(Project, project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        milestones = session.scalars(select(Milestone).where(Milestone.project_id == project_id).order_by(Milestone.sort_order)).all()
        tasks = session.scalars(select(Task).where(Task.project_id == project_id).order_by(Task.created_at)).all()
        result = _project_dict(project)
        result["milestones"] = [{"id": m.id, "code": m.code, "name": m.name, "status": m.status, "sort_order": m.sort_order} for m in milestones]
        result["tasks"] = [_task_dict(t) for t in tasks]
        return result


@router.post("/projects/{project_id}/milestones", status_code=201)
def create_milestone(project_id: int, payload: MilestoneCreate) -> dict:
    with SessionLocal() as session:
        if session.get(Project, project_id) is None:
            raise HTTPException(status_code=404, detail="Project not found")
        if session.scalar(select(Milestone).where(Milestone.project_id == project_id, Milestone.code == payload.code)):
            raise HTTPException(status_code=409, detail="Milestone code already exists in this project")
        milestone = Milestone(project_id=project_id, code=payload.code, name=payload.name,
                              description=payload.description, sort_order=payload.sort_order,
                              target_date=payload.target_date)
        session.add(milestone)
        session.commit()
        session.refresh(milestone)
        return {"id": milestone.id, "project_id": milestone.project_id, "code": milestone.code,
                "name": milestone.name, "status": milestone.status, "sort_order": milestone.sort_order}


@router.post("/projects/{project_id}/tasks", status_code=201)
def create_task(project_id: int, payload: TaskCreate) -> dict:
    with SessionLocal() as session:
        if session.get(Project, project_id) is None:
            raise HTTPException(status_code=404, detail="Project not found")
        if session.scalar(select(Task).where(Task.code == payload.code)):
            raise HTTPException(status_code=409, detail="Task code already exists")
        if payload.milestone_id is not None:
            milestone = session.get(Milestone, payload.milestone_id)
            if milestone is None or milestone.project_id != project_id:
                raise HTTPException(status_code=422, detail="Milestone must belong to this project")
        agent_id = None
        if payload.assigned_agent_code:
            agent = session.scalar(select(OrganizationNode).where(
                OrganizationNode.code == payload.assigned_agent_code,
                OrganizationNode.node_type == "agent",
                OrganizationNode.is_active.is_(True)))
            if agent is None:
                raise HTTPException(status_code=422, detail="Unknown or inactive assigned agent")
            agent_id = agent.id
        creator = session.scalar(select(OrganizationNode).where(OrganizationNode.code == payload.created_by_node_code))
        if creator is None:
            raise HTTPException(status_code=422, detail="Unknown task creator")
        task = Task(project_id=project_id, milestone_id=payload.milestone_id, code=payload.code,
                    title=payload.title, description=payload.description, assigned_agent_id=agent_id,
                    created_by_node_id=creator.id, priority=payload.priority, due_at=payload.due_at)
        session.add(task)
        session.commit()
        session.refresh(task)
        return _task_dict(task)


@router.patch("/tasks/{task_id}/status")
def update_task_status(task_id: int, status: TaskStatus) -> dict:
    with SessionLocal() as session:
        task = session.get(Task, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        task.status = status
        session.commit()
        session.refresh(task)
        return _task_dict(task)
