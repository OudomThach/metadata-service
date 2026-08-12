"""romdoul data sharing entities

Revision ID: 0004
Revises: 0001
Create Date: 2026-08-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(128), unique=True, index=True),
        sa.Column("org_type", sa.String(32), server_default="other"),
        sa.Column("contact", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("categories.id", ondelete="CASCADE"), nullable=True, index=True),
        sa.Column("name", sa.String(128), index=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort", sa.Integer(), server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "collections",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(128), unique=True, index=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "datasets",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("record_id", sa.String(36), sa.ForeignKey("records.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("name", sa.String(256), index=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("categories.id", ondelete="SET NULL"), nullable=True),
        sa.Column("collection_id", sa.Integer(), sa.ForeignKey("collections.id", ondelete="SET NULL"), nullable=True),
        sa.Column("coverage_start", sa.Date(), nullable=True),
        sa.Column("coverage_end", sa.Date(), nullable=True),
        sa.Column("frequency", sa.String(32), nullable=True),
        sa.Column("url", sa.String(512), nullable=True),
        sa.Column("status", sa.String(16), server_default="draft", index=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("file_name", sa.String(256), nullable=True),
        sa.Column("file_size", sa.Integer(), nullable=True),
        sa.Column("file_type", sa.String(128), nullable=True),
        sa.Column("file_base64", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        "audit_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("actor", sa.String(128), server_default="system:unknown", index=True),
        sa.Column("action", sa.String(32), index=True),
        sa.Column("entity_type", sa.String(32), index=True),
        sa.Column("entity_id", sa.String(64), nullable=True, index=True),
        sa.Column("detail", JSONB(), nullable=True),
        sa.Column("at", sa.DateTime(timezone=True), server_default=sa.func.now(), index=True),
    )
    op.create_table(
        "settings",
        sa.Column("key", sa.String(64), primary_key=True),
        sa.Column("value", JSONB(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.add_column("users", sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "organization_id")
    op.drop_table("settings")
    op.drop_table("audit_events")
    op.drop_table("datasets")
    op.drop_table("collections")
    op.drop_table("categories")
    op.drop_table("organizations")
