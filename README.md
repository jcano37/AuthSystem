# 🔐 Authentication Backend API

A robust, enterprise-grade authentication and authorization REST API built with **FastAPI**, featuring multi-tenancy, role-based access control (RBAC), session management, integrations, and comprehensive security features.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7+-red.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Features

### 🔐 Core Authentication
- **JWT Authentication**: Secure access and refresh token system with automatic renewal
- **OAuth2 Password Flow**: Industry-standard authentication implementation
- **Session Management**: Redis-based session tracking with device fingerprinting
- **Token Blacklisting**: Secure logout with token invalidation
- **Password Security**: bcrypt hashing with configurable complexity policies
- **Two-Factor Authentication**: Optional 2FA support with TOTP

### 🏢 Multi-Tenancy
- **Company Isolation**: Complete data separation between organizations
- **Root Company**: System-level administration capabilities
- **Company Management**: Create, update, and manage multiple organizations
- **User-Company Association**: Users belong to specific companies
- **Company-Scoped Resources**: Roles, permissions, and integrations per company

### 👥 User Management
- **User Registration**: Admin-controlled user creation with email verification
- **Profile Management**: Comprehensive user profile system
- **Password Reset**: Secure password reset workflow with time-limited tokens
- **Account Status Management**: Active/inactive user control
- **Login History**: Track user authentication events
- **Device Management**: View and revoke sessions across devices

### 🛡️ Authorization & Access Control
- **Role-Based Access Control (RBAC)**: Flexible role and permission system
- **Resource-Based Permissions**: Fine-grained access control with actions
- **Permission Inheritance**: Hierarchical permission structure
- **Dynamic Role Assignment**: Runtime role management
- **Company-Scoped Roles**: Roles isolated per company
- **Admin Protection**: Special handling for superuser operations

### 🔗 Integrations & Webhooks
- **API Key Management**: Generate and manage integration API keys
- **Webhook Endpoints**: Receive and process external system events
- **Integration Types**: Support for OAuth2, API key, and custom integrations
- **Secret Regeneration**: Security-focused API secret management
- **Company-Scoped Integrations**: Integrations isolated per company

### 🔒 Security Features
- **Rate Limiting**: Configurable request rate limiting per endpoint
- **CORS Protection**: Fine-grained cross-origin resource sharing controls
- **Input Validation**: Comprehensive data validation with Pydantic
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **Password Policies**: Configurable complexity requirements
- **Security Headers**: Proper HTTP security header implementation
- **API Authentication**: Middleware-based API key validation

### 🛠️ Developer Experience
- **OpenAPI Documentation**: Auto-generated Swagger/ReDoc documentation
- **Database Migrations**: Alembic-powered schema management with utilities
- **Comprehensive Testing**: Unit and integration test suites
- **Code Quality**: Automated formatting (Black) and linting (MyPy)
- **Docker Support**: Complete containerization with Docker Compose
- **Development Tools**: PowerShell scripts for workflow automation
- **Type Safety**: Full TypeScript-style type hints in Python

## 🏗️ Technology Stack

- **Framework**: FastAPI 0.115.0 with async/await support
- **Database**: PostgreSQL 16+ with SQLAlchemy 2.0.27 ORM
- **Cache**: Redis 7+ for sessions, rate limiting, and caching
- **Authentication**: JWT with python-jose and OAuth2 flows
- **Password Security**: bcrypt via passlib with configurable rounds
- **Validation**: Pydantic 2.6.1 for request/response validation
- **Migrations**: Alembic 1.13.1 with custom utilities
- **Testing**: pytest 8.0.0 with async support and coverage
- **ASGI Server**: Uvicorn 0.27.1 with hot reload

## 🗃️ Database Schema

The system implements a sophisticated multi-tenant database schema:

### Core Entities
- **Companies**: Multi-tenant isolation with root company support
- **Users**: User accounts with company association and 2FA
- **Roles**: Named permission groups scoped to companies
- **Permissions**: Fine-grained access rights with resource-action pairs
- **ResourceTypes**: Categorization for permission targets
- **Sessions**: Active user sessions with device tracking
- **Integrations**: External system connections with API keys

### Security Tables
- **PasswordResetTokens**: Secure password reset mechanism
- **EmailVerificationTokens**: Account verification system
- **UserRole**: Many-to-many user-role associations
- **RolePermission**: Many-to-many role-permission associations

### Key Relationships
- Users belong to Companies (multi-tenancy)
- Roles are scoped to Companies
- Permissions reference ResourceTypes
- Sessions track user authentication state
- Integrations are company-specific

## 📋 Prerequisites

### System Requirements
- **Python**: 3.11 or higher
- **Docker**: Latest version with Docker Compose V2
- **PostgreSQL**: 16+ (if running locally)
- **Redis**: 7+ (if running locally)

### Development Tools
- **Git**: Version control
- **PowerShell**: For automation scripts (Windows)
- **curl**: For API testing
- **OpenSSL**: For generating secure keys

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd auth-backend

# Verify project structure
ls -la
```

### 2. Environment Configuration

Create your environment file:

```bash
# Copy the environment template
cp .env.example .env

# Generate a secure JWT secret key
openssl rand -hex 32
```

Edit `.env` with your configuration:

```env
# Database Configuration
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-super-secure-db-password
POSTGRES_DB=auth_db

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# JWT Security (CRITICAL - Change in production)
SECRET_KEY=your-generated-secret-key-from-openssl
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
PASSWORD_RESET_TOKEN_EXPIRE_HOURS=1

# Email Configuration (Required for password reset)
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

# Session & Features
SESSION_EXPIRE_DAYS=30
ENABLE_2FA=false

# CORS Origins (Add your frontend URLs)
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

### 3. Docker Deployment (Recommended)

```bash
# Build and start all services (backend + database + redis)
docker-compose up --build -d

# Run database migrations
docker-compose exec app alembic upgrade head

# Verify the deployment
curl http://localhost:8000/
```

### 4. Access the API

- **API Base**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/api/v1/openapi.json

### 5. Create Initial Admin User

Use the API to create your first admin user:

```bash
# Using curl (replace with your data)
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@yourapp.com",
    "username": "admin",
    "full_name": "System Administrator",
    "password": "SecurePassword123!",
    "is_superuser": true
  }'
```

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/auth/login` | User login with credentials | No |
| `POST` | `/api/v1/auth/refresh` | Refresh access token | No |
| `POST` | `/api/v1/auth/logout` | Logout and invalidate session | Yes |
| `POST` | `/api/v1/auth/password-reset-request` | Request password reset | No |
| `POST` | `/api/v1/auth/password-reset` | Confirm password reset | No |

### User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/users/me` | Get current user profile | Yes |
| `PUT` | `/api/v1/users/me` | Update current user profile | Yes |
| `GET` | `/api/v1/users/{user_id}` | Get user by ID | Admin |
| `GET` | `/api/v1/users/` | List all users (paginated) | Admin |
| `POST` | `/api/v1/users/` | Create new user | Admin |
| `PUT` | `/api/v1/users/{user_id}` | Update user | Admin |
| `DELETE` | `/api/v1/users/{user_id}` | Delete user | Admin |

### Session Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/users/me/sessions` | List user's active sessions | Yes |
| `DELETE` | `/api/v1/users/me/sessions/{session_id}` | Revoke specific session | Yes |
| `DELETE` | `/api/v1/users/me/sessions` | Revoke all other sessions | Yes |
| `GET` | `/api/v1/sessions/` | List all sessions | Admin |
| `DELETE` | `/api/v1/sessions/{session_id}` | Admin revoke session | Admin |

### Roles & Permissions

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/roles/` | List all roles | Yes |
| `POST` | `/api/v1/roles/` | Create new role | Admin |
| `PUT` | `/api/v1/roles/{role_id}` | Update role | Admin |
| `DELETE` | `/api/v1/roles/{role_id}` | Delete role | Admin |
| `POST` | `/api/v1/roles/{role_id}/permissions/{permission_id}` | Assign permission to role | Admin |
| `DELETE` | `/api/v1/roles/{role_id}/permissions/{permission_id}` | Remove permission from role | Admin |
| `GET` | `/api/v1/permissions/` | List all permissions | Yes |
| `POST` | `/api/v1/permissions/` | Create permission | Admin |
| `PUT` | `/api/v1/permissions/{permission_id}` | Update permission | Admin |
| `DELETE` | `/api/v1/permissions/{permission_id}` | Delete permission | Admin |

### Resource Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/resources/` | List resource types | Yes |
| `POST` | `/api/v1/resources/` | Create resource type | Admin |
| `PUT` | `/api/v1/resources/{resource_id}` | Update resource type | Admin |
| `DELETE` | `/api/v1/resources/{resource_id}` | Delete resource type | Admin |

### Company Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/companies/` | List companies | Root Admin |
| `POST` | `/api/v1/companies/` | Create company | Root Admin |
| `PUT` | `/api/v1/companies/{company_id}` | Update company | Root Admin |
| `DELETE` | `/api/v1/companies/{company_id}` | Delete company | Root Admin |

### Integrations & Webhooks

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/integrations/` | List integrations | Yes |
| `POST` | `/api/v1/integrations/` | Create integration | Admin |
| `PUT` | `/api/v1/integrations/{integration_id}` | Update integration | Admin |
| `DELETE` | `/api/v1/integrations/{integration_id}` | Delete integration | Admin |
| `POST` | `/api/v1/integrations/{integration_id}/regenerate-secret` | Regenerate API secret | Admin |
| `POST` | `/api/v1/webhooks/{integration_type}` | Receive webhook | API Key |

## 🏗️ Project Structure

```
auth-backend/
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration files
│   │   ├── unified_migration.py  # Main database schema
│   │   └── add_integrations_table.py
│   ├── env.py                    # Alembic environment
│   └── migration_utils.py        # Migration utilities
├── app/                          # Main application
│   ├── api/                      # API layer
│   │   ├── deps.py              # Dependencies
│   │   ├── middlewares/         # Custom middlewares
│   │   │   └── api_auth.py      # API key authentication
│   │   └── v1/endpoints/        # API endpoints
│   │       ├── auth.py          # Authentication
│   │       ├── users.py         # User management
│   │       ├── sessions.py      # Session management
│   │       ├── roles.py         # Role management
│   │       ├── permissions.py   # Permission management
│   │       ├── resources.py     # Resource management
│   │       ├── companies.py     # Company management
│   │       ├── integrations.py  # Integration management
│   │       └── webhooks.py      # Webhook endpoints
│   ├── core/                     # Core utilities
│   │   ├── config.py            # Configuration
│   │   ├── security.py          # Security functions
│   │   └── redis.py             # Redis utilities
│   ├── crud/                     # Database operations
│   │   ├── user.py              # User CRUD
│   │   ├── role.py              # Role CRUD
│   │   ├── permission.py        # Permission CRUD
│   │   ├── session.py           # Session CRUD
│   │   ├── resource.py          # Resource CRUD
│   │   ├── company.py           # Company CRUD
│   │   └── integration.py       # Integration CRUD
│   ├── db/                       # Database setup
│   │   ├── base.py              # Database base
│   │   ├── base_class.py        # SQLAlchemy base
│   │   └── session.py           # Database session
│   ├── models/                   # SQLAlchemy models
│   │   ├── user.py              # User models
│   │   ├── roles.py             # Role models
│   │   ├── permissions.py       # Permission models
│   │   ├── resource.py          # Resource models
│   │   ├── sessions.py          # Session models
│   │   ├── company.py           # Company models
│   │   └── integration.py       # Integration models
│   ├── schemas/                  # Pydantic schemas
│   │   ├── user.py              # User schemas
│   │   ├── role.py              # Role schemas
│   │   ├── permission.py        # Permission schemas
│   │   ├── resource.py          # Resource schemas
│   │   ├── session.py           # Session schemas
│   │   ├── company.py           # Company schemas
│   │   └── integration.py       # Integration schemas
│   └── main.py                   # Application entry point
├── tests/                        # Test suite
│   ├── conftest.py              # Test configuration
│   ├── test_auth.py             # Authentication tests
│   └── test_main.py             # Main application tests
├── cURL/                         # API testing collection
│   └── Auth System.postman_collection.json
├── docs/                         # Documentation
│   ├── ENVIRONMENT_SETUP.md     # Environment configuration
│   └── CODE_QUALITY.md          # Code quality guidelines
├── k8s/                          # Kubernetes manifests
├── scripts/                      # Utility scripts
├── docker-compose.yml            # Docker orchestration
├── Dockerfile                    # Docker image definition
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── pyproject.toml               # Python project configuration
├── alembic.ini                  # Alembic configuration
├── format_and_check.ps1         # Code quality automation
└── reset-and-rebuild.ps1        # Environment reset script
```

## 🔧 Development

### Local Development Setup

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Format code
black app/
isort app/

# Type checking
mypy app/

# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"
```

### Database Management

```bash
# Reset database (development only)
./reset-and-rebuild.ps1

# Create migration
docker-compose exec app alembic revision --autogenerate -m "Add new feature"

# Apply migrations
docker-compose exec app alembic upgrade head

# View migration history
docker-compose exec app alembic history

# Revert last migration
docker-compose exec app alembic downgrade -1
```

### Code Quality

```bash
# Run all quality checks (Windows)
./format_and_check.ps1

# Manual tools
python -m black app
python -m isort app
python -m flake8 app
python -m mypy app
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run tests with verbose output
pytest -v

# Run tests in Docker
docker-compose exec app pytest
```

### API Testing

The project includes a comprehensive Postman collection:

```bash
# Import the collection
cURL/Auth System.postman_collection.json
```

Test scenarios included:
- Authentication flows (login, refresh, logout)
- User management operations
- Role and permission management
- Session management
- Integration and webhook testing
- Multi-tenant operations

## 🚀 Deployment

### Docker Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with production configuration
docker-compose -f docker-compose.prod.yml up -d

# Run migrations in production
docker-compose -f docker-compose.prod.yml exec app alembic upgrade head
```

### Environment Variables for Production

Ensure these are properly configured:

```env
# Security (CRITICAL)
SECRET_KEY=production-secret-key-64-chars-minimum
POSTGRES_PASSWORD=super-secure-production-password

# Performance
RATE_LIMIT_PER_MINUTE=100
SESSION_EXPIRE_DAYS=7

# Email (Required)
SMTP_HOST=your-production-smtp-server
SMTP_USER=your-production-email
SMTP_PASSWORD=your-production-email-password

# CORS (Restrict to your domains)
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

### Kubernetes Deployment

Kubernetes manifests are available in the `k8s/` directory:

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get services
```

## 📊 Monitoring & Health Checks

### Health Endpoints

```bash
# Application health
curl http://localhost:8000/

# Database connectivity
curl http://localhost:8000/health/db

# Redis connectivity
curl http://localhost:8000/health/redis
```

### Logging

The application uses structured logging with different levels:

- **INFO**: Normal operations
- **WARNING**: Unusual but handled situations
- **ERROR**: Error conditions
- **DEBUG**: Detailed debugging information (development only)

## 🔒 Security Considerations

### Production Security Checklist

- [ ] **JWT Secret**: Use a cryptographically secure secret key (64+ characters)
- [ ] **Database**: Strong passwords and connection encryption
- [ ] **HTTPS**: Enable TLS/SSL for all communications
- [ ] **CORS**: Restrict origins to your specific domains
- [ ] **Rate Limiting**: Configure appropriate limits for your use case
- [ ] **Email Security**: Use app passwords and secure SMTP
- [ ] **Environment Variables**: Never commit secrets to version control
- [ ] **Database Backups**: Regular automated backups with encryption
- [ ] **Session Security**: Configure appropriate session timeouts
- [ ] **Password Policies**: Enforce strong password requirements

### Security Features

- **Password Hashing**: bcrypt with configurable work factor
- **JWT Security**: Signed tokens with expiration and refresh mechanism
- **Session Invalidation**: Secure logout with token blacklisting
- **Rate Limiting**: Protection against brute force attacks
- **Input Validation**: Comprehensive data validation and sanitization
- **SQL Injection Protection**: Parameterized queries with SQLAlchemy
- **CORS Configuration**: Fine-grained cross-origin controls
- **API Key Management**: Secure integration authentication

### Password Policy Configuration

```env
MIN_PASSWORD_LENGTH=8          # Minimum password length
REQUIRE_SPECIAL_CHAR=true      # Require special characters
REQUIRE_NUMBER=true            # Require numbers
REQUIRE_UPPERCASE=true         # Require uppercase letters
```

### Rate Limiting Configuration

```env
RATE_LIMIT_PER_MINUTE=60      # Requests per minute per IP
```

## 🤝 Contributing

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Run** tests and quality checks (`./format_and_check.ps1`)
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Code Standards

- **Python Style**: PEP 8 compliance via Black
- **Import Sorting**: isort configuration
- **Type Hints**: Comprehensive type annotations
- **Documentation**: Docstrings for all public functions
- **Testing**: Unit tests for all new functionality

## 📖 Additional Documentation

- **[Environment Setup](docs/ENVIRONMENT_SETUP.md)**: Detailed configuration guide
- **[Code Quality](docs/CODE_QUALITY.md)**: Development standards and practices
- **[API Reference](http://localhost:8000/docs)**: Interactive API documentation
- **[Database Schema](alembic/versions/)**: Migration files with schema details

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI**: For the excellent web framework
- **SQLAlchemy**: For robust database ORM
- **Alembic**: For database migration management
- **PostgreSQL**: For reliable data storage
- **Redis**: For high-performance caching
- **Pydantic**: For data validation and serialization

## 📞 Support

For backend-specific support:
- **Issues**: Create an issue in the repository with the `backend` label
- **Documentation**: Check this README and the `/docs` directory
- **API Testing**: Use the provided Postman collection
- **Security Issues**: Email security issues privately

---

**Built with ❤️ using FastAPI and modern Python practices**