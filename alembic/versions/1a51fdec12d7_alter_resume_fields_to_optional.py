"""alter resume fields to optional

Revision ID: 1a51fdec12d7
Revises: f3d981b036e2
Create Date: 2024-09-22 20:06:06.178085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a51fdec12d7'
down_revision: Union[str, None] = 'f3d981b036e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('resumes', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('resumes', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('resumes', 'date_of_birth',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('resumes', 'nationality',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('resumes', 'address_line_1',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('resumes', 'postal_code',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('resumes', 'city',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('resumes', 'country',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('resumes', 'email_address',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('resumes', 'contact_number',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('resumes', 'responsibilities',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('resumes', 'responsibilities',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('resumes', 'contact_number',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('resumes', 'email_address',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('resumes', 'country',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('resumes', 'city',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('resumes', 'postal_code',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('resumes', 'address_line_1',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('resumes', 'nationality',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('resumes', 'date_of_birth',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('resumes', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('resumes', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
