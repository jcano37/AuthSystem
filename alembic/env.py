import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.db.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    return settings.SQLALCHEMY_DATABASE_URI


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    # Optimized pool settings
    if not configuration.get("sqlalchemy.pool_size"):
        configuration["sqlalchemy.pool_size"] = "5"
    if not configuration.get("sqlalchemy.max_overflow"):
        configuration["sqlalchemy.max_overflow"] = "10"
    
    # Set connection arguments directly
    connect_args = {
        "connect_timeout": 15,  # Connection timeout in seconds
    }
        
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.QueuePool,  # Using QueuePool for better performance
        connect_args=connect_args  # Pass connection arguments explicitly
    )

    with connectable.connect() as connection:
        # Enable batch operations for better performance
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # Enable batch mode for better performance with larger migrations
            render_as_batch=True,
            # Optimize index creation
            compare_type=True,
            compare_server_default=True,
            # Set a larger transaction batch size for better performance
            transaction_per_migration=True,
            # Set a reasonable batch size for large operations
            batch_size=1000
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
