# ATR-003 — Projects & Tasks

## Objective

Provide persistent project, milestone and task records so ATR-CEO and ATR-PMO can organize delivery work and assign tasks to the ten registered agents.

## Data model

- Project: unique code, name, description, status, priority, Owner/Agent node and target date.
- Milestone: belongs to a project; has a project-scoped code, name, status, ordering and target date.
- Task: belongs to a project; optionally belongs to a milestone and another parent task; has a unique code, title, status, priority, optional assigned agent, creator and due date.

## Status vocabulary

Project: planned, active, on_hold, completed, cancelled.

Task: backlog, ready, in_progress, blocked, in_review, needs_revision, done, cancelled.

Priority: low, medium, high, critical.

## API

- POST /api/v1/projects
- GET /api/v1/projects
- GET /api/v1/projects/{project_id}
- POST /api/v1/projects/{project_id}/milestones
- POST /api/v1/projects/{project_id}/tasks
- PATCH /api/v1/tasks/{task_id}/status

The API validates project owner, task creator, assigned active agent, duplicate codes and milestone/project consistency.

## Governance and limits

These endpoints persist planning records only. They do not invoke LLMs, start agents, make purchases, operate hardware, deploy software or authorize restricted actions. Authentication and role-based access control are not yet implemented; keep this service on a trusted local development network and do not expose it publicly.

## Acceptance checklist

- [ ] Migration 0003_projects_tasks applies after 0002_organization.
- [ ] Create/list/get project endpoints work.
- [ ] Milestone creation enforces project ownership.
- [ ] Task creation validates assigned agent and milestone.
- [ ] Task status can be updated using the documented state vocabulary.
- [ ] API tests and CI pass.
- [ ] Owner verifies endpoints on local Windows Docker environment.
