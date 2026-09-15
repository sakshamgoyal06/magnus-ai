"""chat_records table for Telegram conversation persistence

Revision ID: 20250915_0002
Revises: 20250914_0001
Create Date: 2026-09-15

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20250915_0002"
down_revision: str | Sequence[str] | None = "20250914_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "chat_records",
        sa.Column("id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("conversation_id", sa.Uuid(), nullable=False),
        sa.Column("telegram_user_id", sa.BigInteger(), nullable=False),
        sa.Column("telegram_chat_id", sa.BigInteger(), nullable=False),
        sa.Column("telegram_message_id", sa.BigInteger(), nullable=True),
        sa.Column("role", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "role IN ('user', 'assistant', 'system')",
            name="chat_records_role_check",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram_message_id", name="chat_records_telegram_message_id_key"),
    )
    op.create_index(
        "chat_records_conversation_id_created_at_idx",
        "chat_records",
        ["conversation_id", "created_at"],
    )
    op.create_index(
        "chat_records_telegram_user_id_created_at_idx",
        "chat_records",
        ["telegram_user_id", "created_at"],
    )
    op.execute("ALTER TABLE chat_records ENABLE ROW LEVEL SECURITY")


def downgrade() -> None:
    op.drop_index("chat_records_telegram_user_id_created_at_idx", table_name="chat_records")
    op.drop_index("chat_records_conversation_id_created_at_idx", table_name="chat_records")
    op.drop_table("chat_records")
