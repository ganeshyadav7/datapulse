"""enterprise observability baseline

Revision ID: 0001_enterprise_observability
Revises:
Create Date: 2026-06-29
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_enterprise_observability"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=40), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_is_active", "users", ["is_active"], unique=False)
    op.create_index("ix_users_role", "users", ["role"], unique=False)
    op.add_column("airflow_dag_runs", sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("spark_jobs", sa.Column("partitions", sa.Integer(), nullable=False, server_default="1"))


def downgrade() -> None:
    op.drop_column("spark_jobs", "partitions")
    op.drop_column("airflow_dag_runs", "retry_count")
    op.drop_index("ix_users_role", table_name="users")
    op.drop_index("ix_users_is_active", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
