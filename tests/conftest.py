import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set test environment variables BEFORE any app imports
os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
os.environ["POSTGRES_SERVER"] = "localhost"  # Won't be used due to override
os.environ["POSTGRES_USER"] = "test"
os.environ["POSTGRES_PASSWORD"] = "test"
os.environ["POSTGRES_DB"] = "test"
os.environ["REDIS_HOST"] = "localhost"

# Create test database engine (SQLite in-memory)
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Database dependency override for tests using SQLite."""
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test."""
    # Import models to register them with Base
    from app.models import user, resource, sessions, company, roles, permissions
    from app.db.base_class import Base
    
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestSessionLocal()
    
    # Create root company and user for tests
    from app.models.company import Company
    from app.models.user import User
    from app.models.roles import Role
    from app.models.permissions import Permission
    from app.models.resource import ResourceType
    from app.core.security import get_password_hash
    from datetime import datetime, timezone
    
    # Create root company
    root_company = Company(
        name="Root Company",
        description="Root company for system administration",
        is_active=True,
        is_root=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    session.add(root_company)
    session.flush()  # Get the ID
    
    # Create root user
    root_user = User(
        email="root@example.com",
        username="root",
        full_name="Root User",
        hashed_password=get_password_hash("Root1234!"),
        is_active=True,
        is_verified=True,
        is_superuser=True,
        company_id=root_company.id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    session.add(root_user)
    session.commit()
    
    yield session
    
    # Cleanup
    session.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client():
    """Create a test client with all necessary mocks and overrides."""
    
    # Mock Redis operations completely
    redis_mock = MagicMock()
    redis_mock.get.return_value = None
    redis_mock.set.return_value = True
    redis_mock.delete.return_value = True
    redis_mock.sadd.return_value = True
    redis_mock.sismember.return_value = False
    
    # Also patch the database engine and session at module level
    with patch("app.core.redis.redis_client", redis_mock), \
         patch("app.core.redis.add_to_blacklist") as mock_blacklist, \
         patch("app.core.redis.is_blacklisted", return_value=False) as mock_is_blacklisted, \
         patch("app.core.redis.increment_rate_limit", return_value=1), \
         patch("app.core.redis.check_rate_limit", return_value=True), \
         patch("app.db.session.engine", test_engine), \
         patch("app.db.session.SessionLocal", TestSessionLocal):
        
        # Import app and dependencies
        from app.main import app
        from app.db.session import get_db
        
        # Override the database dependency to use SQLite
        app.dependency_overrides[get_db] = override_get_db
        
        # Import models and create tables
        from app.models import user, resource, sessions, company, roles, permissions
        from app.db.base_class import Base
        Base.metadata.create_all(bind=test_engine)
        
        # Create root company and user for tests
        from app.models.company import Company
        from app.models.user import User
        from app.core.security import get_password_hash
        from datetime import datetime, timezone
        
        # Create session for setup
        setup_session = TestSessionLocal()
        
        # Create root company
        root_company = Company(
            name="Root Company",
            description="Root company for system administration",
            is_active=True,
            is_root=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        setup_session.add(root_company)
        setup_session.flush()  # Get the ID
        
        # Create root user
        root_user = User(
            email="root@example.com",
            username="root",
            full_name="Root User",
            hashed_password=get_password_hash("Root1234!"),
            is_active=True,
            is_verified=True,
            is_superuser=True,
            company_id=root_company.id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        setup_session.add(root_user)
        setup_session.commit()
        setup_session.close()
        
        # Create test client
        with TestClient(app) as test_client:
            yield test_client
        
        # Cleanup
        Base.metadata.drop_all(bind=test_engine)
        app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def db():
    """Database session fixture (alias for test_db)."""
    # Import models to register them with Base
    from app.models import user, resource, sessions, company, roles, permissions
    from app.db.base_class import Base
    
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestSessionLocal()
    
    # Create root company and user for tests
    from app.models.company import Company
    from app.models.user import User
    from app.core.security import get_password_hash
    from datetime import datetime, timezone
    
    # Create root company
    root_company = Company(
        name="Root Company",
        description="Root company for system administration",
        is_active=True,
        is_root=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    session.add(root_company)
    session.flush()  # Get the ID
    
    # Create root user
    root_user = User(
        email="root@example.com",
        username="root",
        full_name="Root User",
        hashed_password=get_password_hash("Root1234!"),
        is_active=True,
        is_verified=True,
        is_superuser=True,
        company_id=root_company.id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    session.add(root_user)
    session.commit()
    
    yield session
    
    # Cleanup
    session.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def root_token(client):
    """Get authentication token for root user."""
    login_data = {
        "username": "root",
        "password": "Root1234!"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    return data["access_token"]


@pytest.fixture(scope="function") 
def auth_headers(root_token):
    """Get authorization headers for API requests."""
    return {"Authorization": f"Bearer {root_token}"} 