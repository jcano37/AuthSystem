# 🔐 Full-Stack Authentication & Authorization System

A comprehensive, enterprise-grade authentication and authorization platform built with **FastAPI** (backend) and **React** (frontend), featuring multi-tenancy, role-based access control (RBAC), session management, integrations, and modern security practices.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.1.0-blue.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7+-red.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Overview

This is a complete authentication and authorization solution designed for modern applications requiring sophisticated user management, multi-tenant architecture, and enterprise-level security. The system provides both a robust API backend and a sleek administrative frontend.

## 🚀 Key Features

### 🔐 Core Authentication
- **JWT Authentication**: Secure access and refresh token system with automatic renewal
- **OAuth2 Password Flow**: Industry-standard authentication implementation
- **Session Management**: Redis-based session tracking with device fingerprinting
- **Token Blacklisting**: Secure logout with token invalidation
- **Password Security**: bcrypt hashing with configurable complexity policies
- **Two-Factor Authentication**: Optional 2FA support with TOTP

### 👥 User Management
- **User Registration**: Admin-controlled user creation with email verification
- **Profile Management**: Comprehensive user profile system with avatar support
- **Password Reset**: Secure password reset workflow with time-limited tokens
- **Account Status Management**: Active/inactive user control
- **Login History**: Track user authentication events
- **Device Management**: View and revoke sessions across devices

### 🏢 Multi-Tenancy & Companies
- **Company Isolation**: Complete data separation between organizations
- **Root Company**: System-level administration capabilities
- **Company Management**: Create, update, and manage multiple organizations
- **User-Company Association**: Users belong to specific companies
- **Company-Scoped Resources**: Roles, permissions, and integrations per company

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

### 🖥️ Modern Frontend
- **React 19**: Latest React with modern hooks and patterns
- **Tailwind CSS**: Beautiful, responsive UI with dark mode support
- **Admin Dashboard**: Comprehensive administrative interface
- **User Self-Service**: Profile management and session control
- **Real-time Updates**: Live session monitoring and management
- **Mobile Responsive**: Optimized for all device sizes

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

## 🏗️ Architecture

### Technology Stack

#### Backend
- **Framework**: FastAPI 0.115.0 with async/await support
- **Database**: PostgreSQL 16+ with SQLAlchemy 2.0.27 ORM
- **Cache**: Redis 7+ for sessions, rate limiting, and caching
- **Authentication**: JWT with python-jose and OAuth2 flows
- **Password Security**: bcrypt via passlib with configurable rounds
- **Validation**: Pydantic 2.6.1 for request/response validation
- **Migrations**: Alembic 1.13.1 with custom utilities
- **Testing**: pytest 8.0.0 with async support and coverage
- **ASGI Server**: Uvicorn 0.27.1 with hot reload

#### Frontend
- **Framework**: React 19.1.0 with modern hooks
- **Styling**: Tailwind CSS 4.1.10 with custom components
- **Routing**: React Router DOM 7.6.2 with protected routes
- **HTTP Client**: Axios 1.9.0 with interceptors
- **Forms**: React Hook Form 7.57.0 with validation
- **Icons**: Heroicons 2.2.0 for consistent iconography
- **Build Tool**: Vite 6.3.5 with hot module replacement
- **State Management**: React Context with reducers

### Database Schema

The system implements a sophisticated multi-tenant database schema:

#### Core Entities
- **Companies**: Multi-tenant isolation with root company support
- **Users**: User accounts with company association and 2FA
- **Roles**: Named permission groups scoped to companies
- **Permissions**: Fine-grained access rights with resource-action pairs
- **ResourceTypes**: Categorization for permission targets
- **Sessions**: Active user sessions with device tracking
- **Integrations**: External system connections with API keys

#### Security Tables
- **PasswordResetTokens**: Secure password reset mechanism
- **EmailVerificationTokens**: Account verification system
- **UserRole**: Many-to-many user-role associations
- **RolePermission**: Many-to-many role-permission associations

#### Key Relationships
- Users belong to Companies (multi-tenancy)
- Roles are scoped to Companies
- Permissions reference ResourceTypes
- Sessions track user authentication state
- Integrations are company-specific

## 📋 Prerequisites

### System Requirements
- **Python**: 3.11 or higher
- **Node.js**: 18+ with npm (for frontend)
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

# CORS Origins (Add your frontend URL)
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

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd ../auth-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 5. Access the Application

- **API Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend Application**: http://localhost:5173
- **ReDoc Documentation**: http://localhost:8000/redoc

### 6. Create Initial Admin User

Use the API to create your first admin user:

```bash
# Using the API directly (replace with your data)
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

## 🖥️ Frontend Features

### User Interface
- **Modern Design**: Clean, professional interface with Tailwind CSS
- **Responsive Layout**: Mobile-first design that works on all devices
- **Dark Mode Ready**: Prepared for dark theme implementation
- **Loading States**: Proper loading indicators and skeleton screens
- **Error Handling**: User-friendly error messages and retry mechanisms

### Pages & Components

#### Public Pages
- **Login**: Secure authentication with remember me option
- **Forgot Password**: Password reset request and confirmation

#### User Pages
- **Dashboard**: Overview of user account and recent activity
- **Profile**: Edit personal information and change password
- **My Sessions**: View and manage active sessions across devices

#### Admin Pages
- **Users**: Complete user management with creation, editing, and role assignment
- **Roles**: Role management with permission assignment
- **Permissions**: Permission management with resource-action pairs
- **Sessions**: System-wide session monitoring and management
- **Companies**: Multi-tenant company management (root admin only)
- **Integrations**: External system integration management

### Security Features
- **Protected Routes**: Route-level authentication and authorization
- **Role-Based Access**: Different interfaces for users and admins
- **Session Management**: Automatic token refresh and logout on expiry
- **CSRF Protection**: Built-in protection against cross-site request forgery

## 🔧 Development

### Backend Development

```bash
# Install dependencies
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

### Frontend Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
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
```

## 🧪 Testing

### Backend Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run tests with verbose output
pytest -v
```

### API Testing

The project includes a comprehensive Postman collection:

```bash
# Import the collection
curl/Auth System.postman_collection.json
```

Test scenarios included:
- Authentication flows (login, refresh, logout)
- User management operations
- Role and permission management
- Session management
- Integration and webhook testing

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

## 📊 Monitoring & Observability

### Health Checks

```bash
# Backend health
curl http://localhost:8000/

# Database connectivity
curl http://localhost:8000/api/v1/health/db

# Redis connectivity
curl http://localhost:8000/api/v1/health/redis
```

### Metrics & Logging

- **Application Logs**: Structured logging with correlation IDs
- **Database Metrics**: Connection pool and query performance
- **Redis Metrics**: Cache hit rates and session statistics
- **Security Events**: Authentication failures and suspicious activity

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

## 🤝 Contributing

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards

- **Python**: Follow PEP 8, use Black for formatting
- **TypeScript/JavaScript**: Follow ESLint configuration
- **Documentation**: Update README and API docs for new features
- **Testing**: Add tests for new functionality
- **Type Hints**: Use comprehensive type annotations

### Pull Request Guidelines

- Provide clear description of changes
- Include relevant tests
- Update documentation as needed
- Ensure all CI checks pass
- Follow semantic versioning for releases

## 📖 Additional Documentation

- **[Environment Setup](docs/ENVIRONMENT_SETUP.md)**: Detailed configuration guide
- **[Code Quality](docs/CODE_QUALITY.md)**: Development standards and practices
- **[API Reference](http://localhost:8000/docs)**: Interactive API documentation
- **[Database Schema](alembic/versions/)**: Migration files with schema details

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI**: For the excellent web framework
- **React**: For the powerful frontend library
- **PostgreSQL**: For reliable data storage
- **Redis**: For high-performance caching
- **Tailwind CSS**: For beautiful, responsive styling
- **SQLAlchemy**: For robust database ORM
- **Alembic**: For database migration management

## 📞 Support

For support, email support@yourapp.com or create an issue in the repository.

---

**Built with ❤️ for modern authentication and authorization needs**