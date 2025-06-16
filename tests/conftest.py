import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set test environment variables before any imports
os.environ["POSTGRES_SERVER"] = "test-server"
os.environ["POSTGRES_USER"] = "test"
os.environ["POSTGRES_PASSWORD"] = "test"
os.environ["POSTGRES_DB"] = "test"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
os.environ["REDIS_HOST"] = "localhost"

# Create test database engine
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Database dependency override for tests."""
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    # Import all models to register them with Base
    from app.models import user, resource, sessions
    from app.db.base_class import Base
    
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function") 
def client():
    # Mock Redis operations to avoid Redis dependency
    with patch("app.core.redis.add_to_blacklist"), \
         patch("app.core.redis.is_blacklisted", return_value=False):
        
        from app.main import app
        from app.db.session import get_db
        
        # Override database dependency
        app.dependency_overrides[get_db] = override_get_db
        
        # Import all models and create tables for this test
        from app.models import user, resource, sessions
        from app.db.base_class import Base
        Base.metadata.create_all(bind=test_engine)
        
        with TestClient(app) as c:
            yield c
        
        # Clean up
        from app.db.base_class import Base
        Base.metadata.drop_all(bind=test_engine)
        app.dependency_overrides.clear() 