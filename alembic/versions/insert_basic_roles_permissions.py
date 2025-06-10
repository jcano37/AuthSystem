"""Insert basic roles and permissions

Revision ID: insert_basic_roles_permissions
Revises: roles_permissions_migration
Create Date: 2024-06-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, select, text
from datetime import datetime

# Import migration utilities
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from migration_utils import batch_insert, optimize_index_creation, with_statement_timeout

# revision identifiers, used by Alembic.
revision = 'insert_basic_roles_permissions'
down_revision = 'roles_permissions_migration'
branch_labels = None
depends_on = None

# Define table representations for raw SQL operations
roles_table = table('roles',
    column('id', sa.Integer),
    column('name', sa.String),
    column('description', sa.String),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime),
    column('is_default', sa.Boolean)
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

role_permission_table = table('role_permission',
    column('role_id', sa.Integer),
    column('permission_id', sa.Integer)
)

resource_types_table = table('resource_types',
    column('id', sa.Integer),
    column('name', sa.String),
    column('description', sa.String),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime)
)


def upgrade() -> None:
    connection = op.get_bind()
    current_time = datetime.utcnow()
    
    # Insert basic resource types
    resource_types_data = [
        {
            'name': 'users',
            'description': 'Recursos relacionados con usuarios',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'roles',
            'description': 'Recursos relacionados con roles',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'profile',
            'description': 'Recursos relacionados con perfiles',
            'created_at': current_time,
            'updated_at': current_time
        }
    ]
    
    # Insert resource types
    batch_insert(connection, resource_types_table, resource_types_data)
    
    # Get resource types
    resource_types_query = select(resource_types_table.c.id, resource_types_table.c.name)
    resource_types_result = connection.execute(resource_types_query).fetchall()
    resource_types = {name: id for id, name in resource_types_result}
    
    # Insert basic roles with returning IDs
    roles_data = [
        {
            'name': 'admin',
            'description': 'Administrador con acceso completo',
            'created_at': current_time,
            'updated_at': current_time,
            'is_default': False
        },
        {
            'name': 'user',
            'description': 'Usuario estándar con acceso limitado',
            'created_at': current_time,
            'updated_at': current_time,
            'is_default': True
        },
        {
            'name': 'guest',
            'description': 'Usuario invitado con acceso solo de lectura',
            'created_at': current_time,
            'updated_at': current_time,
            'is_default': False
        }
    ]
    
    # Insert roles
    batch_insert(connection, roles_table, roles_data)
    
    # Get roles
    roles_query = select(roles_table.c.id, roles_table.c.name).order_by(roles_table.c.id)
    roles_result = connection.execute(roles_query).fetchall()
    roles = {role_name: role_id for role_id, role_name in roles_result}
    
    # Define permissions with resource_type_id
    permissions_data = [
        # User resource permissions
        {
            'name': 'users:read',
            'description': 'Ver usuarios',
            'resource_type_id': resource_types['users'],
            'action': 'read',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'users:create',
            'description': 'Crear usuarios',
            'resource_type_id': resource_types['users'],
            'action': 'create',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'users:update',
            'description': 'Actualizar usuarios',
            'resource_type_id': resource_types['users'],
            'action': 'update',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'users:delete',
            'description': 'Eliminar usuarios',
            'resource_type_id': resource_types['users'],
            'action': 'delete',
            'created_at': current_time,
            'updated_at': current_time
        },
        # Role resource permissions
        {
            'name': 'roles:read',
            'description': 'Ver roles',
            'resource_type_id': resource_types['roles'],
            'action': 'read',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'roles:create',
            'description': 'Crear roles',
            'resource_type_id': resource_types['roles'],
            'action': 'create',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'roles:update',
            'description': 'Actualizar roles',
            'resource_type_id': resource_types['roles'],
            'action': 'update',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'roles:delete',
            'description': 'Eliminar roles',
            'resource_type_id': resource_types['roles'],
            'action': 'delete',
            'created_at': current_time,
            'updated_at': current_time
        },
        # Profile permission
        {
            'name': 'profile:update',
            'description': 'Actualizar perfil propio',
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
        batch_insert(connection, role_permission_table, role_permissions)


def downgrade() -> None:
    # Optimización: Usar transacción explícita para las eliminaciones
    connection = op.get_bind()
    
    with connection.begin():
        # Eliminaciones en orden inverso para respetar restricciones de clave foránea
        connection.execute(text("TRUNCATE role_permission CASCADE"))
        connection.execute(text("TRUNCATE permissions CASCADE"))
        connection.execute(text("TRUNCATE roles CASCADE"))
        connection.execute(text("TRUNCATE resource_types CASCADE"))