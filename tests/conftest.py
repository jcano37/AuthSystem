import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import patch

# Create test database - use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    from app.db.base import Base
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def mock_redis_functions():
    """Mock Redis functions to avoid Redis dependency in tests"""
    pass


@pytest.fixture(scope="function") 
def client():
    # Mock Redis functions before importing the app
    with patch("app.core.redis.add_to_blacklist", mock_redis_functions), \
         patch("app.core.redis.is_blacklisted", return_value=False):
        
        from app.main import app
        from app.db.session import get_db
        
        # Override database dependency
        app.dependency_overrides[get_db] = override_get_db
        
        with TestClient(app) as c:
            yield c
        
        # Clean up
        app.dependency_overrides.clear() 