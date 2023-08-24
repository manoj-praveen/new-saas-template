"""added user login table

Revision ID: 2dd458174473
Revises:
Create Date: 2023-08-17 20:15:41.077396

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2dd458174473"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_login",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("password_salt", sa.String(), nullable=False),
        sa.Column(
            "t_create",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "t_update",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
            onupdate=sa.text("now()"),
        ),
        sa.Column("t_delete", sa.TIMESTAMP(timezone=True)),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="user_login_email_key"),
    )


def downgrade():
    op.drop_table("user_login", schema=None)
