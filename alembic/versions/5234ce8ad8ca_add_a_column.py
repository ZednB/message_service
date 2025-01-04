"""Add a column

Revision ID: 5234ce8ad8ca
Revises: f4c7df0275a2
Create Date: 2024-10-29 00:07:35.874764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5234ce8ad8ca'
down_revision: Union[str, None] = 'f4c7df0275a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
