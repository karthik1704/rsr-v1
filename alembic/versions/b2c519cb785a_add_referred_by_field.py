"""add referred by field

Revision ID: b2c519cb785a
Revises: 14564538e26f
Create Date: 2024-12-27 18:21:38.240992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c519cb785a'
down_revision: Union[str, None] = '14564538e26f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('referred_by', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'referred_by')
    # ### end Alembic commands ###
