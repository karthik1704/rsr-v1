"""more models

Revision ID: 7b5eb9badd6f
Revises: b2d8c389109c
Create Date: 2024-09-18 18:36:59.569254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b5eb9badd6f'
down_revision: Union[str, None] = 'b2d8c389109c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resumes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('resume_title', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('nationality', sa.String(), nullable=False),
    sa.Column('address_line_1', sa.String(), nullable=False),
    sa.Column('address_line_2', sa.String(), nullable=True),
    sa.Column('postal_code', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('email_address', sa.String(), nullable=False),
    sa.Column('contact_number', sa.String(), nullable=False),
    sa.Column('responsibilities', sa.String(), nullable=False),
    sa.Column('referred_by', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resumes_id'), 'resumes', ['id'], unique=False)
    op.create_table('stripe_payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('currency', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('stripe_payment_intent_id', sa.String(), nullable=False),
    sa.Column('failure_code', sa.String(), nullable=True),
    sa.Column('failure_message', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stripe_payments_id'), 'stripe_payments', ['id'], unique=False)
    op.create_index(op.f('ix_stripe_payments_stripe_payment_intent_id'), 'stripe_payments', ['stripe_payment_intent_id'], unique=True)
    op.create_index(op.f('ix_stripe_payments_user_id'), 'stripe_payments', ['user_id'], unique=False)
    op.create_table('driving_licenses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.Integer(), nullable=False),
    sa.Column('license_type', sa.String(), nullable=False),
    sa.Column('license_issued_date', sa.Date(), nullable=False),
    sa.Column('license_expiry_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_driving_licenses_id'), 'driving_licenses', ['id'], unique=False)
    op.create_table('educations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.Integer(), nullable=False),
    sa.Column('title_of_qualification', sa.String(), nullable=False),
    sa.Column('organization_name', sa.String(), nullable=False),
    sa.Column('from_date', sa.Date(), nullable=False),
    sa.Column('to_date', sa.Date(), nullable=True),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_educations_id'), 'educations', ['id'], unique=False)
    op.create_table('experiences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.Integer(), nullable=False),
    sa.Column('employer', sa.String(), nullable=False),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('occupation', sa.String(), nullable=False),
    sa.Column('from_date', sa.Date(), nullable=False),
    sa.Column('to_date', sa.Date(), nullable=True),
    sa.Column('currently_working', sa.Boolean(), nullable=False),
    sa.Column('about_company', sa.String(), nullable=True),
    sa.Column('responsibilities', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_experiences_employer'), 'experiences', ['employer'], unique=False)
    op.create_index(op.f('ix_experiences_id'), 'experiences', ['id'], unique=False)
    op.create_table('language_skills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.Integer(), nullable=False),
    sa.Column('language', sa.String(), nullable=False),
    sa.Column('is_mother_tongue', sa.Boolean(), nullable=False),
    sa.Column('proficiency_level', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_language_skills_id'), 'language_skills', ['id'], unique=False)
    op.create_table('others',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.Integer(), nullable=False),
    sa.Column('sectiontitle', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_others_id'), 'others', ['id'], unique=False)
    op.create_table('training_awards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('awarding_institute', sa.String(), nullable=False),
    sa.Column('from_date', sa.Date(), nullable=False),
    sa.Column('to_date', sa.Date(), nullable=True),
    sa.Column('location', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_awards_id'), 'training_awards', ['id'], unique=False)
    op.add_column('users', sa.Column('expiry_date', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'expiry_date')
    op.drop_index(op.f('ix_training_awards_id'), table_name='training_awards')
    op.drop_table('training_awards')
    op.drop_index(op.f('ix_others_id'), table_name='others')
    op.drop_table('others')
    op.drop_index(op.f('ix_language_skills_id'), table_name='language_skills')
    op.drop_table('language_skills')
    op.drop_index(op.f('ix_experiences_id'), table_name='experiences')
    op.drop_index(op.f('ix_experiences_employer'), table_name='experiences')
    op.drop_table('experiences')
    op.drop_index(op.f('ix_educations_id'), table_name='educations')
    op.drop_table('educations')
    op.drop_index(op.f('ix_driving_licenses_id'), table_name='driving_licenses')
    op.drop_table('driving_licenses')
    op.drop_index(op.f('ix_stripe_payments_user_id'), table_name='stripe_payments')
    op.drop_index(op.f('ix_stripe_payments_stripe_payment_intent_id'), table_name='stripe_payments')
    op.drop_index(op.f('ix_stripe_payments_id'), table_name='stripe_payments')
    op.drop_table('stripe_payments')
    op.drop_index(op.f('ix_resumes_id'), table_name='resumes')
    op.drop_table('resumes')
    # ### end Alembic commands ###
