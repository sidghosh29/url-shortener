"""Seed default roles and backfill unassigned users.

Revision ID: d31fa74ec692
Revises: 04c9489e218d
Create Date: 2026-10-10 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import insert

# revision identifiers, used by Alembic.
revision: str = "d31fa74ec692"
down_revision: str | Sequence[str] | None = "04c9489e218d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    roles = sa.table(
        "roles",
        sa.column("id", sa.Integer()),
        sa.column("name", sa.String(length=20)),
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
    )
    users = sa.table("users", sa.column("role_id", sa.Integer()))

    op.execute(
        insert(roles)
        .values(
            [
                {
                    "name": "member",
                    "created_at": sa.func.now(),
                    "updated_at": sa.func.now(),
                },
                {
                    "name": "admin",
                    "created_at": sa.func.now(),
                    "updated_at": sa.func.now(),
                },
            ]
        )
        .on_conflict_do_nothing(index_elements=[roles.c.name])
    )

    op.alter_column("users", "role_id", existing_type=sa.Integer(), nullable=True)
    member_role_id = op.get_bind().execute(
        sa.select(roles.c.id).where(roles.c.name == "member")
    ).scalar_one()
    op.execute(
        users.update()
        .where(users.c.role_id.is_(None))
        .values(role_id=member_role_id)
    )
    op.alter_column("users", "role_id", existing_type=sa.Integer(), nullable=False)


def downgrade() -> None:
    # Keep seeded roles: they may be referenced by users and can predate this revision.
    pass
