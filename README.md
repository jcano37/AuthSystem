# 🔐 Authentication & Authorization System

A modern, robust authentication and authorization service built with FastAPI, featuring comprehensive user management, role-based access control (RBAC), session management, and enterprise-grade security features.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7+-red.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Features

### Core Authentication
- **JWT Authentication**: Secure access and refresh token system
- **OAuth2 Password Flow**: Industry-standard authentication flow
- **Session Management**: Redis-based session tracking with device info
- **Token Blacklisting**: Secure logout with token invalidation
- **Password Security**: bcrypt hashing with configurable policies

### User Management
- **User Registration & Verification**: Email verification workflow
- **Profile Management**: Comprehensive user profile system
- **Password Reset**: Secure password reset with time-limited tokens
- **Account Status**: Active/inactive user management
- **Two-Factor Authentication**: 2FA support (configurable)

### Authorization & Access Control
- **Role-Based Access Control (RBAC)**: Flexible role and permission system
- **Resource-Based Permissions**: Fine-grained access control
- **Permission Inheritance**: Hierarchical permission structure
- **Dynamic Role Assignment**: Runtime role management

### Security Features
- **Rate Limiting**: Configurable request rate limiting
- **CORS Protection**: Cross-origin resource sharing controls
- **Input Validation**: Comprehensive data validation with Pydantic
- **SQL Injection Protection**: SQLAlchemy ORM security
- **Password Policies**: Configurable complexity requirements

### Developer Experience
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **Database Migrations**: Alembic-powered schema management
- **Comprehensive Testing**: Unit and integration test suite
- **Code Quality**: Automated formatting and linting
- **Docker Support**: Complete containerization
- **Development Tools**: PowerShell scripts for workflow automation

## 🏗️ Architecture

### Technology Stack
- **Framework**: FastAPI 0.115.0
- **Database**: PostgreSQL 16+ with SQLAlchemy 2.0.27
- **Cache**: Redis 7+ for sessions and rate limiting
- **Authentication**: JWT with python-jose
- **Password Security**: bcrypt via passlib
- **Validation**: Pydantic 2.6.1 for data validation
- **Migrations**: Alembic 1.13.1
- **Testing**: pytest 8.0.0 with coverage
- **ASGI Server**: Uvicorn 0.27.1

### Database Schema

The system uses a sophisticated database schema with the following key entities:

- **Users**: Core user information with authentication data
- **Roles**: Named permission groups (admin, user, moderator, etc.)
- **Permissions**: Fine-grained access rights tied to resources and actions
- **ResourceTypes**: Categorization for permission targets
- **Sessions**: Active user sessions with device tracking
- **Password Reset Tokens**: Secure password reset mechanism
- **Email Verification Tokens**: Account verification system

## 📋 Prerequisites

- **Python**: 3.11 or higher
- **Docker**: Latest version with Docker Compose
- **PostgreSQL**: 16+ (if running locally)
- **Redis**: 7+ (if running locally)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd auth-backend
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# Database Configuration
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=auth_db

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# JWT Security
SECRET_KEY=your-super-secure-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
PASSWORD_RESET_TOKEN_EXPIRE_HOURS=1

# Email Configuration (Optional)
SMTP_TLS=true
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-app-password
EMAILS_FROM_EMAIL=noreply@yourapp.com
EMAILS_FROM_NAME=YourApp

# Security Settings
RATE_LIMIT_PER_MINUTE=60
MIN_PASSWORD_LENGTH=8
REQUIRE_SPECIAL_CHAR=true
REQUIRE_NUMBER=true
REQUIRE_UPPERCASE=true

# Features
ENABLE_2FA=false
```

### 3. Docker Deployment

```bash
# Build and start all services
docker-compose up --build -d

# Run database migrations
docker-compose exec app alembic upgrade head

# Verify the setup
curl http://localhost:8000/
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/login` | User login with credentials |
| `POST` | `/api/v1/auth/register` | New user registration |
| `POST` | `/api/v1/auth/refresh` | Refresh access token |
| `POST` | `/api/v1/auth/logout` | Logout and invalidate session |
| `POST` | `/api/v1/auth/password-reset-request` | Request password reset |
| `POST` | `/api/v1/auth/password-reset` | Confirm password reset |

### User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/users/me` | Get current user profile |
| `PUT` | `/api/v1/users/me` | Update current user profile |
| `GET` | `/api/v1/users/{user_id}` | Get user by ID (admin) |
| `GET` | `/api/v1/users/` | List all users (admin) |
| `POST` | `/api/v1/users/` | Create new user (admin) |
| `PUT` | `/api/v1/users/{user_id}` | Update user (admin) |
| `DELETE` | `/api/v1/users/{user_id}` | Delete user (admin) |

### Session Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/users/me/sessions` | List user's active sessions |
| `DELETE` | `/api/v1/users/me/sessions/{session_id}` | Revoke specific session |
| `DELETE` | `/api/v1/users/me/sessions` | Revoke all sessions |

### Roles & Permissions

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/roles/` | List all roles |
| `POST` | `/api/v1/roles/` | Create new role |
| `PUT` | `/api/v1/roles/{role_id}` | Update role |
| `DELETE` | `/api/v1/roles/{role_id}` | Delete role |
| `GET` | `/api/v1/permissions/` | List all permissions |
| `POST` | `/api/v1/permissions/` | Create permission |
| `PUT` | `/api/v1/permissions/{permission_id}` | Update permission |
| `DELETE` | `/api/v1/permissions/{permission_id}` | Delete permission |

### Resource Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/resources/` | List resource types |
| `POST` | `/api/v1/resources/` | Create resource type |
| `PUT` | `/api/v1/resources/{resource_id}` | Update resource type |
| `DELETE` | `/api/v1/resources/{resource_id}` | Delete resource type |

## 🏗️ Project Structure

```
auth-backend/
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration files
│   │   ├── initial_migration.py
│   │   ├── roles_permissions_migration.py
│   │   └── insert_basic_roles_permissions.py
│   ├── env.py                    # Alembic environment
│   └── migration_utils.py        # Migration utilities
├── app/                          # Main application
│   ├── api/                      # API layer
│   │   ├── deps.py              # Dependencies
│   │   └── v1/endpoints/        # API endpoints
│   │       ├── auth.py          # Authentication
│   │       ├── users.py         # User management
│   │       ├── sessions.py      # Session management
│   │       ├── roles.py         # Role management
│   │       ├── permissions.py   # Permission management
│   │       └── resources.py     # Resource management
│   ├── core/                     # Core utilities
│   │   ├── config.py            # Configuration
│   │   ├── security.py          # Security functions
│   │   └── redis.py             # Redis utilities
│   ├── crud/                     # Database operations
│   │   ├── user.py              # User CRUD
│   │   ├── role.py              # Role CRUD
│   │   ├── permission.py        # Permission CRUD
│   │   ├── session.py           # Session CRUD
│   │   └── resource.py          # Resource CRUD
│   ├── db/                       # Database setup
│   │   ├── base.py              # Database base
│   │   ├── base_class.py        # SQLAlchemy base
│   │   └── session.py           # Database session
│   ├── models/                   # SQLAlchemy models
│   │   ├── user.py              # User models
│   │   ├── resource.py          # Resource models
│   │   └── sessions.py          # Session models
│   ├── schemas/                  # Pydantic schemas
│   │   ├── user.py              # User schemas
│   │   ├── resource.py          # Resource schemas
│   │   └── session.py           # Session schemas
│   └── main.py                   # Application entry point
├── tests/                        # Test suite
│   ├── conftest.py              # Test configuration
│   ├── test_auth.py             # Authentication tests
│   └── test_main.py             # Main application tests
├── cURL/                         # API testing collection
│   └── Auth System.postman_collection.json
├── docs/                         # Documentation
│   └── CODE_QUALITY.md          # Code quality guidelines
├── docker-compose.yml            # Docker orchestration
├── Dockerfile                    # Docker image definition
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── pyproject.toml               # Python project configuration
├── alembic.ini                  # Alembic configuration
├── format_and_check.ps1         # Code quality automation
├── quick_format.ps1             # Quick formatting script
└── reset-and-rebuild.ps1        # Environment reset script
```

## 🧪 Development

### Local Development Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

2. **Start services locally**:
```bash
# Start PostgreSQL and Redis
docker-compose up db redis -d

# Set environment variables for local development
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/auth_db"
export REDIS_URL="redis://localhost:6379/0"

# Run migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_auth.py

# Run tests in Docker
docker-compose exec app pytest
```

### Code Quality

The project includes automated code quality tools:

```bash
# Format code and run checks (Windows)
.\format_and_check.ps1

# Quick format only
.\quick_format.ps1

# Manual tools
python -m black app
python -m isort app
python -m flake8 app
python -m mypy app
```

### Database Operations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Revert last migration
alembic downgrade -1

# Reset database (development only)
.\reset-and-rebuild.ps1
```

## 🔒 Security Considerations

### Production Deployment

1. **Environment Security**:
   - Use strong, unique `SECRET_KEY`
   - Configure proper database credentials
   - Enable HTTPS/TLS
   - Set restrictive CORS origins

2. **Database Security**:
   - Use connection pooling
   - Enable SSL connections
   - Regular backups
   - Restrict network access

3. **Redis Security**:
   - Configure password authentication
   - Use SSL/TLS connections
   - Restrict network access
   - Set appropriate timeout values

4. **Application Security**:
   - Enable rate limiting
   - Configure strong password policies
   - Implement proper logging
   - Monitor authentication attempts

### Password Policy

The system supports configurable password policies:

```env
MIN_PASSWORD_LENGTH=8          # Minimum password length
REQUIRE_SPECIAL_CHAR=true      # Require special characters
REQUIRE_NUMBER=true            # Require numbers
REQUIRE_UPPERCASE=true         # Require uppercase letters
```

### Rate Limiting

Built-in rate limiting protects against brute force attacks:

```env
RATE_LIMIT_PER_MINUTE=60      # Requests per minute per IP
```

## 📊 Monitoring & Observability

### Health Checks

The application includes health check endpoints:

- **Application Health**: `GET /`
- **Database Health**: Built into Docker Compose
- **Redis Health**: Built into Docker Compose

### Logging

The application uses structured logging with different levels:

- **INFO**: Normal operations
- **WARNING**: Unusual but handled situations
- **ERROR**: Error conditions
- **DEBUG**: Detailed debugging information (development only)

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests and quality checks**:
   ```bash
   .\format_and_check.ps1
   pytest
   ```
5. **Commit your changes**:
   ```bash
   git commit -m "Add: Amazing feature description"
   ```
6. **Push to your branch**:
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Code Standards

- **Python Style**: PEP 8 compliance via Black
- **Import Sorting**: isort configuration
- **Type Hints**: Comprehensive type annotations
- **Documentation**: Docstrings for all public functions
- **Testing**: Unit tests for all new functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help

1. **Documentation**: Check this README and API docs
2. **Issues**: Search existing GitHub issues
3. **Discussions**: Start a GitHub discussion
4. **Security**: Email security issues privately

### Troubleshooting

#### Common Issues

1. **Database Connection**:
   - Verify PostgreSQL is running
   - Check connection string
   - Ensure database exists

2. **Redis Connection**:
   - Verify Redis is running
   - Check Redis URL configuration
   - Test Redis connectivity

3. **JWT Errors**:
   - Verify SECRET_KEY is set
   - Check token expiration settings
   - Ensure algorithm matches

4. **Migration Issues**:
   - Check Alembic configuration
   - Verify database permissions
   - Review migration files

### Performance Tuning

#### Database Optimization

```env
# Connection pool settings (in alembic.ini)
sqlalchemy.pool_size=10
sqlalchemy.max_overflow=20
sqlalchemy.pool_timeout=30
sqlalchemy.pool_recycle=3600
```

#### Redis Optimization

```env
# Redis memory and persistence settings
REDIS_MAXMEMORY=256mb
REDIS_MAXMEMORY_POLICY=allkeys-lru
```

## 📈 Roadmap

### Planned Features

- [ ] Advanced audit logging
- [ ] Multi-tenancy support
- [ ] Advanced 2FA methods (TOTP, WebAuthn)
- [ ] OAuth2 provider support
- [ ] Advanced session analytics
- [ ] Webhook notifications
- [ ] Admin dashboard
- [ ] API rate limiting per user
- [ ] Advanced password policies
- [ ] SSO integration

### Version History

- **v1.0.0**: Initial release with core authentication
- **Current**: Enhanced RBAC and session management

## Pre-commit Hooks

### Setup

1. Install pre-commit:
```bash
pip install pre-commit
```

2. Install the pre-commit hooks:
```bash
pre-commit install
```

The pre-commit hook will run code quality checks before each commit. If the checks fail, the commit will be aborted.

### Manual Checks

You can also run the checks manually:
```bash
./format_and_check.ps1
```

---

**Built with ❤️ using FastAPI and modern Python practices**