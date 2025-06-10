"""
Utilities to optimize Alembic migrations.
This module provides helper functions to perform migration operations
more efficiently, especially for large operations.
"""

from typing import List, Dict, Any, Optional, Union, Callable
from sqlalchemy import Table, Column, MetaData, text
from sqlalchemy.engine import Connection
import time
import logging

logger = logging.getLogger("alembic.migration")

def batch_insert(connection: Connection, 
                table: Table, 
                rows: List[Dict[str, Any]], 
                batch_size: int = 1000) -> None:
    """
    Inserts rows in batches to improve performance.
    
    Args:
        connection: Active SQLAlchemy connection
        table: SQLAlchemy table object
        rows: List of dictionaries with data to insert
        batch_size: Batch size for each operation
    """
    if not rows:
        return
        
    total = len(rows)
    start_time = time.time()
    
    for i in range(0, total, batch_size):
        batch = rows[i:i+batch_size]
        connection.execute(table.insert(), batch)
        
        # Log progress for large operations
        if i % (batch_size * 10) == 0 and i > 0:
            elapsed = time.time() - start_time
            logger.info(f"Inserted {i}/{total} rows ({i/total:.1%}) in {elapsed:.2f}s")
    
    elapsed = time.time() - start_time
    logger.info(f"Completed inserting {total} rows in {elapsed:.2f}s")

def optimize_index_creation(connection: Connection, table_name: str, column_name: str, 
                           index_name: Optional[str] = None, unique: bool = False) -> None:
    """
    Creates an index in an optimized way using CREATE INDEX CONCURRENTLY
    to reduce table locking.
    
    Args:
        connection: Active SQLAlchemy connection
        table_name: Table name
        column_name: Column name to index
        index_name: Index name (optional)
        unique: Whether the index should be unique
    """
    if index_name is None:
        index_name = f"ix_{table_name}_{column_name}"
        
    unique_clause = "UNIQUE" if unique else ""
    
    # CONCURRENTLY requires its own transaction
    connection.execute(text("COMMIT"))
    
    sql = f"CREATE {unique_clause} INDEX CONCURRENTLY {index_name} ON {table_name} ({column_name})"
    connection.execute(text(sql))
    
    # Start a new transaction for remaining operations
    connection.execute(text("BEGIN"))
    
def batch_update(connection: Connection, 
                table_name: str,
                values: Dict[str, Any], 
                where_clause: str,
                batch_size: int = 5000) -> None:
    """
    Updates records in batches to reduce locks and improve performance.
    
    Args:
        connection: Active SQLAlchemy connection
        table_name: Table name
        values: Dictionary with columns and values to update
        where_clause: WHERE condition for the update
        batch_size: Number of rows to update in each batch
    """
    # Prepare SET clause from values dictionary
    set_clause = ", ".join([f"{k} = :p_{k}" for k in values.keys()])
    params = {f"p_{k}": v for k, v in values.items()}
    
    # Create temporary table with IDs to update
    temp_table = f"tmp_update_{table_name}"
    connection.execute(text(f"CREATE TEMPORARY TABLE {temp_table} (id INTEGER)"))
    
    # Get IDs to update
    id_query = f"INSERT INTO {temp_table} SELECT id FROM {table_name} WHERE {where_clause}"
    connection.execute(text(id_query))
    
    # Count total rows to update
    count_result = connection.execute(text(f"SELECT COUNT(*) FROM {temp_table}")).scalar()
    total_rows = count_result or 0
    
    if total_rows == 0:
        connection.execute(text(f"DROP TABLE IF EXISTS {temp_table}"))
        logger.info(f"No rows to update in {table_name}")
        return
    
    logger.info(f"Updating {total_rows} rows in {table_name}")
    start_time = time.time()
    
    # Update in batches
    offset = 0
    while offset < total_rows:
        # Get batch of IDs
        batch_ids = connection.execute(
            text(f"SELECT id FROM {temp_table} ORDER BY id LIMIT {batch_size} OFFSET {offset}")
        ).scalars().all()
        
        if not batch_ids:
            break
            
        # Update this batch
        batch_where = f"id IN ({','.join(str(id) for id in batch_ids)})"
        update_sql = f"UPDATE {table_name} SET {set_clause} WHERE {batch_where}"
        connection.execute(text(update_sql), params)
        
        offset += batch_size
        
        # Log progress
        if offset % (batch_size * 10) == 0:
            elapsed = time.time() - start_time
            logger.info(f"Updated {offset}/{total_rows} rows ({offset/total_rows:.1%}) in {elapsed:.2f}s")
    
    # Clean up
    connection.execute(text(f"DROP TABLE IF EXISTS {temp_table}"))
    
    elapsed = time.time() - start_time
    logger.info(f"Completed updating {total_rows} rows in {elapsed:.2f}s")

def with_statement_timeout(connection: Connection, timeout_ms: int, callback: Callable) -> Any:
    """
    Executes a function with a statement timeout to avoid prolonged locks.
    
    Args:
        connection: Active SQLAlchemy connection
        timeout_ms: Timeout in milliseconds
        callback: Function to execute within the timeout
        
    Returns:
        The result of the callback function
    """
    # Set timeout
    connection.execute(text(f"SET statement_timeout = {timeout_ms}"))
    
    try:
        # Execute the function
        return callback()
    finally:
        # Reset timeout to default
        connection.execute(text("SET statement_timeout = 0"))
