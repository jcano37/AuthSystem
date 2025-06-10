"""Add roles and permissions system

Revision ID: roles_permissions_migration
Revises: initial_migration
Create Date: 2024-05-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'roles_permissions_migration'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Alter roles table to add is_default and updated_at columns
    op.add_column('roles', sa.Column('is_default', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('updated_at', sa.DateTime(), nullable=True))

    # Create ResourceType table
    op.create_table(
        'resource_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resource_types_id'), 'resource_types', ['id'], unique=False)
    op.create_index(op.f('ix_resource_types_name'), 'resource_types', ['name'], unique=True)

    # Create role_permission association table
    op.create_table(
        'role_permission',
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.Column('permission_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], )
    )

    # Drop foreign key constraint from permissions to roles
    op.drop_constraint('permissions_role_id_fkey', 'permissions', type_='foreignkey')
    
    # Add resource_type_id and action columns to permissions table
    op.add_column('permissions', sa.Column('resource_type_id', sa.Integer(), nullable=True))
    op.add_column('permissions', sa.Column('action', sa.String(), nullable=True))
    op.add_column('permissions', sa.Column('updated_at', sa.DateTime(), nullable=True))
    
    # Add foreign key constraint to resource_types
    op.create_foreign_key('permissions_resource_type_id_fkey', 'permissions', 'resource_types', ['resource_type_id'], ['id'])
    
    # Make resource_type_id and action columns not nullable
    op.execute("UPDATE permissions SET resource_type_id = 1, action = 'default' WHERE resource_type_id IS NULL")
    op.alter_column('permissions', 'resource_type_id', nullable=False)
    op.alter_column('permissions', 'action', nullable=False)
    
    # Drop role_id column from permissions
    op.drop_column('permissions', 'role_id')


def downgrade() -> None:
    # Add role_id column back to permissions
    op.add_column('permissions', sa.Column('role_id', sa.Integer(), nullable=True))
    op.create_foreign_key('permissions_role_id_fkey', 'permissions', 'roles', ['role_id'], ['id'])
    
    # Drop resource_type_id and action columns from permissions
    op.drop_constraint('permissions_resource_type_id_fkey', 'permissions', type_='foreignkey')
    op.drop_column('permissions', 'resource_type_id')
    op.drop_column('permissions', 'action')
    op.drop_column('permissions', 'updated_at')
    
    # Drop role_permission association table
    op.drop_table('role_permission')
    
    # Drop resource_types table
    op.drop_index(op.f('ix_resource_types_name'), table_name='resource_types')
    op.drop_index(op.f('ix_resource_types_id'), table_name='resource_types')
    op.drop_table('resource_types')
    
    # Drop is_default and updated_at columns from roles
    op.drop_column('roles', 'is_default')
    op.drop_column('roles', 'updated_at') 