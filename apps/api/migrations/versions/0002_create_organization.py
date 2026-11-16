"""Create the ATR organization chart and seed the initial team."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_organization"
down_revision: Union[str, None] = "0001_system_settings"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    nodes = op.create_table(
        "organization_nodes",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(length=30), nullable=False, unique=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("node_type", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column(
            "parent_id",
            sa.Integer(),
            sa.ForeignKey("organization_nodes.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column("autonomy_level", sa.String(length=20), nullable=False),
        sa.Column("approval_required", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_organization_nodes_code", "organization_nodes", ["code"], unique=True)

    op.bulk_insert(
        nodes,
        [
            {"id": 1, "code": "OWNER", "name": "Owner", "node_type": "owner",
             "title": "Owner / Human decision maker",
             "description": "Sets company direction and approves consequential decisions.",
             "parent_id": None, "autonomy_level": "human", "approval_required": False, "sort_order": 0, "is_active": True},
            {"id": 2, "code": "ATR-CEO", "name": "ATR-CEO", "node_type": "agent",
             "title": "Chief Executive Agent",
             "description": "Receives Owner requests, frames outcomes, delegates work and reports results.",
             "parent_id": 1, "autonomy_level": "hybrid", "approval_required": True, "sort_order": 1, "is_active": True},
            {"id": 3, "code": "ATR-CTO", "name": "ATR-CTO", "node_type": "agent",
             "title": "Chief Technology Agent",
             "description": "Owns technical architecture, engineering standards and specialist coordination.",
             "parent_id": 2, "autonomy_level": "hybrid", "approval_required": True, "sort_order": 2, "is_active": True},
            {"id": 4, "code": "ATR-PMO", "name": "ATR-PMO", "node_type": "agent",
             "title": "Project Management Agent",
             "description": "Plans milestones, tasks, dependencies, schedules and delivery reporting.",
             "parent_id": 2, "autonomy_level": "hybrid", "approval_required": True, "sort_order": 3, "is_active": True},
            {"id": 5, "code": "ATR-RND", "name": "ATR-RND", "node_type": "agent",
             "title": "Research and Development Agent",
             "description": "Researches technologies, datasheets, references and feasibility.",
             "parent_id": 3, "autonomy_level": "bounded", "approval_required": False, "sort_order": 4, "is_active": True},
            {"id": 6, "code": "ATR-HW", "name": "ATR-HW", "node_type": "agent",
             "title": "Hardware Engineering Agent",
             "description": "Designs hardware architecture, components, power systems, PCB and BOM.",
             "parent_id": 3, "autonomy_level": "bounded", "approval_required": True, "sort_order": 5, "is_active": True},
            {"id": 7, "code": "ATR-EMB", "name": "ATR-EMB", "node_type": "agent",
             "title": "Embedded and Firmware Agent",
             "description": "Develops firmware, drivers and embedded communication interfaces.",
             "parent_id": 3, "autonomy_level": "bounded", "approval_required": True, "sort_order": 6, "is_active": True},
            {"id": 8, "code": "ATR-DRONE", "name": "ATR-DRONE", "node_type": "agent",
             "title": "Drone and UAV Agent",
             "description": "Designs UAV systems, propulsion sizing, integration and flight-test plans.",
             "parent_id": 3, "autonomy_level": "bounded", "approval_required": True, "sort_order": 7, "is_active": True},
            {"id": 9, "code": "ATR-IOT", "name": "ATR-IOT", "node_type": "agent",
             "title": "IoT Systems Agent",
             "description": "Designs IoT nodes, gateways, connectivity and device management.",
             "parent_id": 3, "autonomy_level": "bounded", "approval_required": True, "sort_order": 8, "is_active": True},
            {"id": 10, "code": "ATR-SWAI", "name": "ATR-SWAI", "node_type": "agent",
             "title": "Software and AI Agent",
             "description": "Builds application software, backend, frontend, AI integrations and dashboards.",
             "parent_id": 3, "autonomy_level": "bounded", "approval_required": False, "sort_order": 9, "is_active": True},
            {"id": 11, "code": "ATR-QAK", "name": "ATR-QAK", "node_type": "agent",
             "title": "Quality Assurance and Knowledge Agent",
             "description": "Reviews deliverables, verifies tests, maintains knowledge and can return deficient work.",
             "parent_id": 3, "autonomy_level": "independent_review", "approval_required": False, "sort_order": 10, "is_active": True},
        ],
    )
    op.execute(
        "SELECT setval(pg_get_serial_sequence('organization_nodes', 'id'), "
        "(SELECT MAX(id) FROM organization_nodes))"
    )


def downgrade() -> None:
    op.drop_index("ix_organization_nodes_code", table_name="organization_nodes")
    op.drop_table("organization_nodes")
