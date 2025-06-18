"""Unified Database Migration

Revision ID: unified_migration
Revises: 
Create Date: 2024-06-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, select, text
from datetime import datetime, timezone

# Import migration utilities
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from migration_utils import batch_insert, optimize_index_creation, with_statement_timeout

# revision identifiers, used by Alembic.
revision = 'unified_migration'
down_revision = None
branch_labels = None
depends_on = None

# Define table representations for raw SQL operations
users_table = table('users',
    column('id', sa.Integer),
    column('email', sa.String),
    column('username', sa.String),
    column('hashed_password', sa.String),
    column('full_name', sa.String),
    column('is_active', sa.Boolean),
    column('is_superuser', sa.Boolean),
    column('is_verified', sa.Boolean),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime),
    column('last_login', sa.DateTime),
    column('two_factor_enabled', sa.Boolean),
    column('two_factor_secret', sa.String),
    column('company_id', sa.Integer)
)

companies_table = table('companies',
    column('id', sa.Integer),
    column('name', sa.String),
    column('description', sa.String),
    column('is_active', sa.Boolean),
    column('is_root', sa.Boolean),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime)
)

roles_table = table('roles',
    column('id', sa.Integer),
    column('name', sa.String),
    column('description', sa.String),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime),
    column('is_default', sa.Boolean),
    column('company_id', sa.Integer)
)

permissions_table = table('permissions',
    column('id', sa.Integer),
    column('name', sa.String),
    column('description', sa.String),
    column('resource_type_id', sa.Integer),
    column('action', sa.String),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime)
)

resource_types_table = table('resource_types',
    column('id', sa.Integer),
    column('name', sa.String),
    column('description', sa.String),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime),
    column('company_id', sa.Integer)
)

def upgrade() -> None:
    connection = op.get_bind()
    current_time = datetime.now(timezone.utc)

    # Create companies table first
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_root', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_companies_id'), 'companies', ['id'], unique=False)
    op.create_index(op.f('ix_companies_name'), 'companies', ['name'], unique=True)

    # Insert the root company
    root_company = {
        'name': 'Root Company',
        'description': 'System root company with full access',
        'is_active': True,
        'is_root': True,
        'created_at': current_time,
        'updated_at': current_time
    }
    
    batch_insert(connection, companies_table, [root_company])
    
    # Get the company ID
    root_company_query = select(companies_table.c.id).where(companies_table.c.is_root == True)
    root_company_id = connection.execute(root_company_query).scalar()

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('two_factor_enabled', sa.Boolean(), nullable=True),
        sa.Column('two_factor_secret', sa.String(), nullable=True),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=True),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_id'), 'roles', ['id'], unique=False)
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=False)

    # Create resource_types table
    op.create_table(
        'resource_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resource_types_id'), 'resource_types', ['id'], unique=False)
    op.create_index(op.f('ix_resource_types_name'), 'resource_types', ['name'], unique=False)

    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('resource_type_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['resource_type_id'], ['resource_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permissions_id'), 'permissions', ['id'], unique=False)
    op.create_index(op.f('ix_permissions_name'), 'permissions', ['name'], unique=False)

    # Create user_role association table
    op.create_table(
        'user_role',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )

    # Create role_permission association table
    op.create_table(
        'role_permission',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )

    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('refresh_token', sa.String(), nullable=True),
        sa.Column('device_info', sa.String(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sessions_id'), 'sessions', ['id'], unique=False)
    op.create_index(op.f('ix_sessions_refresh_token'), 'sessions', ['refresh_token'], unique=True)

    # Create password_reset_tokens table
    op.create_table(
        'password_reset_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('token', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('is_used', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_password_reset_tokens_id'), 'password_reset_tokens', ['id'], unique=False)
    op.create_index(op.f('ix_password_reset_tokens_token'), 'password_reset_tokens', ['token'], unique=True)

    # Create email_verification_tokens table
    op.create_table(
        'email_verification_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('token', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('is_used', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_email_verification_tokens_id'), 'email_verification_tokens', ['id'], unique=False)
    op.create_index(op.f('ix_email_verification_tokens_token'), 'email_verification_tokens', ['token'], unique=True)

    # Insert basic resource types
    resource_types_data = [
        {
            'name': 'users',
            'description': 'Resources related to users',
            'created_at': current_time,
            'updated_at': current_time,
            'company_id': root_company_id
        },
        {
            'name': 'roles',
            'description': 'Resources related to roles',
            'created_at': current_time,
            'updated_at': current_time,
            'company_id': root_company_id
        },
        {
            'name': 'profile',
            'description': 'Resources related to profiles',
            'created_at': current_time,
            'updated_at': current_time,
            'company_id': root_company_id
        },
        {
            'name': 'companies',
            'description': 'Resources related to companies',
            'created_at': current_time,
            'updated_at': current_time,
            'company_id': root_company_id
        }
    ]

    # Insert resource types
    batch_insert(connection, resource_types_table, resource_types_data)

    # Get resource types
    resource_types_query = select(resource_types_table.c.id, resource_types_table.c.name)
    resource_types_result = connection.execute(resource_types_query).fetchall()
    resource_types = {name: id for id, name in resource_types_result}

    # Insert basic roles
    roles_data = [
        {
            'name': 'admin',
            'description': 'Administrator with full access',
            'created_at': current_time,
            'updated_at': current_time,
            'is_default': False,
            'company_id': root_company_id
        },
        {
            'name': 'user',
            'description': 'Standard user with limited access',
            'created_at': current_time,
            'updated_at': current_time,
            'is_default': True,
            'company_id': root_company_id
        }
    ]

    # Insert roles
    batch_insert(connection, roles_table, roles_data)

    # Get roles
    roles_query = select(roles_table.c.id, roles_table.c.name).where(roles_table.c.company_id == root_company_id)
    roles_result = connection.execute(roles_query).fetchall()
    roles = {name: id for id, name in roles_result}

    # Create the root user
    from app.core.security import get_password_hash
    root_user_data = {
        'username': 'root',
        'email': 'root@example.com',
        'full_name': 'System Root',
        'hashed_password': get_password_hash('Root1234!'),
        'is_active': True,
        'is_superuser': True,
        'is_verified': True,
        'created_at': current_time,
        'updated_at': current_time,
        'company_id': root_company_id
    }
    
    # Insert root user
    batch_insert(connection, users_table, [root_user_data])
    
    # Get the user ID
    root_user_query = select(users_table.c.id).where(users_table.c.username == 'root')
    root_user_id = connection.execute(root_user_query).scalar()
    
    # Assign admin role to root user
    user_role_table = table('user_role',
        column('user_id', sa.Integer),
        column('role_id', sa.Integer)
    )
    
    user_role_data = [
        {
            'user_id': root_user_id,
            'role_id': roles['admin']
        }
    ]
    
    batch_insert(connection, user_role_table, user_role_data)

    # Add company permissions
    company_permissions = []
    
    for action in ['create', 'read', 'update', 'delete', 'list']:
        company_permissions.append({
            'name': f'company:{action}',
            'description': f'Permission to {action} companies',
            'resource_type_id': resource_types['companies'],
            'action': action,
            'created_at': current_time,
            'updated_at': current_time
        })
    
    batch_insert(connection, permissions_table, company_permissions)
    
    # Get company permission IDs
    company_perm_query = select(permissions_table.c.id).where(
        permissions_table.c.resource_type_id == resource_types['companies']
    )
    company_perm_ids = [row[0] for row in connection.execute(company_perm_query).fetchall()]
    
    # Assign company permissions to admin role
    role_permission_table = table('role_permission',
        column('role_id', sa.Integer),
        column('permission_id', sa.Integer)
    )
    
    role_perm_data = []
    for perm_id in company_perm_ids:
        role_perm_data.append({
            'role_id': roles['admin'],
            'permission_id': perm_id
        })
    
    batch_insert(connection, role_permission_table, role_perm_data)
    
    # Create a companies resource type for the root company
    companies_resource_type = {
        'name': 'root_companies',
        'description': 'Resources related to managing companies by root',
        'created_at': current_time,
        'updated_at': current_time,
        'company_id': root_company_id
    }
    
    batch_insert(connection, resource_types_table, [companies_resource_type])

    # Create a super_admin role for root company
    super_admin_role = {
        'name': 'super_admin',
        'description': 'Super Admin with access to all companies',
        'created_at': current_time,
        'updated_at': current_time,
        'is_default': False,
        'company_id': root_company_id
    }
    
    batch_insert(connection, roles_table, [super_admin_role])
    
    # Get super_admin role ID
    super_admin_query = select(roles_table.c.id).where(
        (roles_table.c.name == 'super_admin') & 
        (roles_table.c.company_id == root_company_id)
    )
    super_admin_id = connection.execute(super_admin_query).scalar()
    
    # Assign super_admin role to root user
    super_admin_role_data = [
        {
            'user_id': root_user_id,
            'role_id': super_admin_id
        }
    ]
    
    batch_insert(connection, user_role_table, super_admin_role_data)

    # Define permissions
    permissions_data = [
        # User resource permissions
        {
            'name': 'users:read',
            'description': 'View users',
            'resource_type_id': resource_types['users'],
            'action': 'read',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'users:create',
            'description': 'Create users',
            'resource_type_id': resource_types['users'],
            'action': 'create',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'users:update',
            'description': 'Update users',
            'resource_type_id': resource_types['users'],
            'action': 'update',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'users:delete',
            'description': 'Delete users',
            'resource_type_id': resource_types['users'],
            'action': 'delete',
            'created_at': current_time,
            'updated_at': current_time
        },
        # Role resource permissions
        {
            'name': 'roles:read',
            'description': 'View roles',
            'resource_type_id': resource_types['roles'],
            'action': 'read',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'roles:create',
            'description': 'Create roles',
            'resource_type_id': resource_types['roles'],
            'action': 'create',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'roles:update',
            'description': 'Update roles',
            'resource_type_id': resource_types['roles'],
            'action': 'update',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'roles:delete',
            'description': 'Delete roles',
            'resource_type_id': resource_types['roles'],
            'action': 'delete',
            'created_at': current_time,
            'updated_at': current_time
        },
        # Profile permission
        {
            'name': 'profile:update',
            'description': 'Update own profile',
            'resource_type_id': resource_types['profile'],
            'action': 'update',
            'created_at': current_time,
            'updated_at': current_time
        }
    ]

    # Insert permissions
    batch_insert(connection, permissions_table, permissions_data)

    # Create optimized index for name in permissions
    with_statement_timeout(connection, 30000, lambda: optimize_index_creation(
        connection, 'permissions', 'name', 'ix_permissions_name_optimized', unique=True
    ))

    # Get permissions
    permissions_query = select(permissions_table.c.id, permissions_table.c.name).order_by(permissions_table.c.id)
    permissions_result = connection.execute(permissions_query).fetchall()
    permissions = {perm_name: perm_id for perm_id, perm_name in permissions_result}

    # Define role-permission associations
    role_permissions_mapping = {
        'admin': [
            'users:read', 'users:create', 'users:update', 'users:delete',
            'roles:read', 'roles:create', 'roles:update', 'roles:delete',
            'profile:update'
        ],
        'user': ['users:read', 'profile:update'],
        'guest': ['users:read']
    }

    # Prepare all data for role-permission
    role_permissions = []
    for role_name, perm_names in role_permissions_mapping.items():
        role_id = roles.get(role_name)
        if role_id:
            for perm_name in perm_names:
                perm_id = permissions.get(perm_name)
                if perm_id:
                    role_permissions.append({
                        'role_id': role_id,
                        'permission_id': perm_id
                    })

    # Use batch_insert utility to insert relationships in an optimized way
    if role_permissions:
        batch_insert(connection, table('role_permission', 
            column('role_id', sa.Integer), 
            column('permission_id', sa.Integer)
        ), role_permissions)


def downgrade() -> None:
    # Drop all tables in reverse order of creation
    op.drop_index(op.f('ix_email_verification_tokens_token'), table_name='email_verification_tokens')
    op.drop_index(op.f('ix_email_verification_tokens_id'), table_name='email_verification_tokens')
    op.drop_table('email_verification_tokens')

    op.drop_index(op.f('ix_password_reset_tokens_token'), table_name='password_reset_tokens')
    op.drop_index(op.f('ix_password_reset_tokens_id'), table_name='password_reset_tokens')
    op.drop_table('password_reset_tokens')

    op.drop_index(op.f('ix_sessions_refresh_token'), table_name='sessions')
    op.drop_index(op.f('ix_sessions_id'), table_name='sessions')
    op.drop_table('sessions')

    op.drop_table('role_permission')
    op.drop_table('user_role')

    op.drop_index(op.f('ix_permissions_name'), table_name='permissions')
    op.drop_index(op.f('ix_permissions_id'), table_name='permissions')
    op.drop_table('permissions')

    op.drop_index(op.f('ix_resource_types_name'), table_name='resource_types')
    op.drop_index(op.f('ix_resource_types_id'), table_name='resource_types')
    op.drop_table('resource_types')

    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_index(op.f('ix_roles_id'), table_name='roles')
    op.drop_table('roles')

    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

    op.drop_index(op.f('ix_companies_name'), table_name='companies')
    op.drop_index(op.f('ix_companies_id'), table_name='companies')
    op.drop_table('companies') 