"""Add integrations table

Revision ID: add_integrations_table
Revises: unified_migration
Create Date: 2024-06-24 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = 'add_integrations_table'
down_revision = 'unified_migration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create integrations table
    op.create_table(
        'integrations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('api_key', sa.String(), nullable=False),
        sa.Column('api_secret', sa.String(), nullable=False),
        sa.Column('integration_type', sa.String(), nullable=False),
        sa.Column('configuration', sa.JSON(), nullable=True),
        sa.Column('callback_url', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_integrations_id'), 'integrations', ['id'], unique=False)
    op.create_index(op.f('ix_integrations_api_key'), 'integrations', ['api_key'], unique=True)


def downgrade() -> None:
    # Drop integrations table
    op.drop_index(op.f('ix_integrations_api_key'), table_name='integrations')
    op.drop_index(op.f('ix_integrations_id'), table_name='integrations')
    op.drop_table('integrations') 