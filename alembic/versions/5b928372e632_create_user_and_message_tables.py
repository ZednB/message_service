"""Create User and Message tables

Revision ID: 5b928372e632
Revises: 21c148c5461a
Create Date: 2025-01-05 14:15:06.489901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b928372e632'
down_revision: Union[str, None] = '21c148c5461a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('password', sa.String(length=1024), nullable=False)
    )

    # Создание таблицы messages
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('sender_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('recipient_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), default=sa.func.current_timestamp())
    )


def downgrade():
    # Удаление таблиц в случае отката
    op.drop_table('messages')
    op.drop_table('users')
