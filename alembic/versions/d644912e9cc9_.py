"""empty message

Revision ID: d644912e9cc9
Revises: eb38377da40c
Create Date: 2024-10-29 21:58:50.564664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd644912e9cc9'
down_revision: Union[str, None] = 'eb38377da40c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
