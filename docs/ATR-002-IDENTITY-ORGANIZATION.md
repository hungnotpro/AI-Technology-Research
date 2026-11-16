# ATR-002 — Identity & Organization

## Objective

Represent the human Owner and the initial ten ATR agents as a persisted, queryable organization hierarchy.

## Organization

- Owner is the human decision-maker and root of the organization.
- ATR-CEO reports to Owner.
- ATR-CTO and ATR-PMO report to ATR-CEO.
- ATR-RND, ATR-HW, ATR-EMB, ATR-DRONE, ATR-IOT, ATR-SWAI and ATR-QAK report to ATR-CTO.
- ATR-QAK performs independent quality review and may return incomplete work for revision.

## Initial agent directory

| Code | Responsibility |
|---|---|
| ATR-CEO | Request intake, outcome framing, delegation and Owner reporting |
| ATR-CTO | Architecture, engineering standards and technical coordination |
| ATR-PMO | Projects, milestones, tasks, dependencies and delivery tracking |
| ATR-RND | Technology research, datasheets and feasibility |
| ATR-HW | Hardware, components, power, PCB and BOM |
| ATR-EMB | Embedded software, firmware, drivers and interfaces |
| ATR-DRONE | UAV architecture, propulsion, integration and test planning |
| ATR-IOT | IoT nodes, gateways, connectivity and device management |
| ATR-SWAI | Applications, backend, frontend, AI integrations and dashboards |
| ATR-QAK | QA, verification, documentation and knowledge quality |

## Data model

The `organization_nodes` table stores Owner and Agent nodes with:
- Stable code and display name
- Node type and role title
- Description and parent relationship
- Autonomy level
- Whether consequential actions require approval
- Sort order and active status

The parent relationship is a self-referencing foreign key. The initial migration seeds the approved organization chart.

## API

- `GET /api/v1/organization` returns the nested organization hierarchy.
- `GET /api/v1/agents` returns the active agent directory.

These are read-only directory endpoints. They do not execute agents, grant permissions, or authenticate users.

## Governance boundaries

- The autonomy field describes intended operating scope; it is not an authorization mechanism.
- Research, analysis, planning and drafting may proceed within assigned scope.
- Purchases, payments, firmware flashing, hardware actuation, motor tests, drone flights, production deployment and destructive data operations require explicit Owner approval.
- AI must not independently control a physical drone.
- Credentials and personal account identities are not seeded in this milestone.

## Acceptance checklist

- [x] Migration `0002_organization` applies successfully on the local Docker database (Owner verified).
- [x] `GET /api/v1/organization` returns Owner as root with the approved reporting structure (Owner verified).
- [x] `GET /api/v1/agents` returns exactly ten active agents (Owner verified).
- [x] API tests and frontend build pass in GitHub Actions.
- [x] Owner verifies the endpoints from the local Windows environment.

## Out of scope

- Login, user accounts, authentication and authorization
- Agent runtime, LLM calls and autonomous task execution
- Dynamic editing of organization nodes
- Project and task management (ATR-003)
