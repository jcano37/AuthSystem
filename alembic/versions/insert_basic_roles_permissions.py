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
    column('resource', sa.String),
    column('action', sa.String),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime)
)

role_permission_table = table('role_permission',
    column('role_id', sa.Integer),
    column('permission_id', sa.Integer)
)

def upgrade() -> None:
    connection = op.get_bind()
    current_time = datetime.utcnow()
    
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
    
    # Usar utilidad de batch_insert para insertar roles de manera optimizada
    batch_insert(connection, roles_table, roles_data)
    
    # Usar una sola consulta para obtener todos los roles
    roles_query = select(roles_table.c.id, roles_table.c.name).order_by(roles_table.c.id)
    roles_result = connection.execute(roles_query).fetchall()
    roles = {role_name: role_id for role_id, role_name in roles_result}
    
    # Definir permisos con tiempo uniforme para reducir variaciones
    permissions_data = [
        # User resource permissions
        {
            'name': 'users:read',
            'description': 'Ver usuarios',
            'resource': 'users',
            'action': 'read',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'users:create',
            'description': 'Crear usuarios',
            'resource': 'users',
            'action': 'create',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'users:update',
            'description': 'Actualizar usuarios',
            'resource': 'users',
            'action': 'update',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'users:delete',
            'description': 'Eliminar usuarios',
            'resource': 'users',
            'action': 'delete',
            'created_at': current_time,
            'updated_at': current_time
        },
        # Role resource permissions
        {
            'name': 'roles:read',
            'description': 'Ver roles',
            'resource': 'roles',
            'action': 'read',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'roles:create',
            'description': 'Crear roles',
            'resource': 'roles',
            'action': 'create',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'roles:update',
            'description': 'Actualizar roles',
            'resource': 'roles',
            'action': 'update',
            'created_at': current_time,
            'updated_at': current_time
        },
        {
            'name': 'roles:delete',
            'description': 'Eliminar roles',
            'resource': 'roles',
            'action': 'delete',
            'created_at': current_time,
            'updated_at': current_time
        },
        # Profile permission
        {
            'name': 'profile:update',
            'description': 'Actualizar perfil propio',
            'resource': 'profile',
            'action': 'update',
            'created_at': current_time,
            'updated_at': current_time
        }
    ]
    
    # Usar utilidad de batch_insert para insertar permisos de manera optimizada
    batch_insert(connection, permissions_table, permissions_data)
    
    # Crear índice optimizado para name en permisos (de manera concurrente para evitar bloqueos)
    with_statement_timeout(connection, 30000, lambda: optimize_index_creation(
        connection, 'permissions', 'name', 'ix_permissions_name_optimized', unique=True
    ))
    
    # Usar una sola consulta para obtener todos los permisos
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
    
    # Preparar todos los datos para role-permission
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
    
    # Usar utilidad de batch_insert para insertar relaciones de manera optimizada
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