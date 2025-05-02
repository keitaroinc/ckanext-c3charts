"""Init tables

Revision ID: 0549ed52dee2
Revises:
Create Date: 2025-05-02 11:39:50.403181

"""
from alembic import op
import sqlalchemy as sa
from ckan.model.types import make_uuid

# revision identifiers, used by Alembic.
revision = "0549ed52dee2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "ckanext_c3charts_featured_charts",
        sa.Column("id", sa.UnicodeText, primary_key=True, default=make_uuid),
        sa.Column("resource_view_id", sa.UnicodeText),
        sa.Column("resource_id", sa.UnicodeText),
        sa.Column("package_id", sa.UnicodeText),
    )


def downgrade():
    op.drop_table("ckanext_c3charts_featured_charts")
