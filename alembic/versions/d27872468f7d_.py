"""empty message

Revision ID: d27872468f7d
Revises: d644912e9cc9
Create Date: 2024-10-29 22:04:38.922897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd27872468f7d'
down_revision: Union[str, None] = 'd644912e9cc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
