# Authentication System

A robust authentication and authorization service built with FastAPI, supporting JWT and OAuth2 Password Flow. This system provides a solid foundation for managing users, roles, and permissions in modern applications.

## Main Features

- User authentication with JWT tokens
- Role-based access control (RBAC)
- Session management with Redis
- Password encryption with bcrypt
- Email verification
- Password reset functionality
- Request rate limiting
- Docker support
- Database migrations with Alembic
- Data validation with Pydantic
- Complete test suite

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL 16+
- Redis 7+

## Main Dependencies

- FastAPI 0.109.2
- Uvicorn 0.27.1
- SQLAlchemy 2.0.27
- Pydantic 2.6.1
- Python-Jose 3.3.0
- Passlib 1.7.4
- Redis 5.0.1
- Alembic 1.13.1
- Pytest 8.0.0

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd auth-service
```

2. Create a `.env` file in the root directory:
```env
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/auth_db

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email (optional)
SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-application-password
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Run the database migrations:
```bash
docker-compose exec app alembic upgrade head
```

The service will be available at `http://localhost:8000`

## API Documentation

Once the service is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login with user/email and password
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout and invalidate session
- `POST /api/v1/auth/verify-email` - Verify email
- `POST /api/v1/auth/reset-password` - Request password reset
- `POST /api/v1/auth/reset-password-confirm` - Confirm password reset

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users/` - List users (admins only)
- `POST /api/v1/users/` - Create user (admins only)
- `PUT /api/v1/users/{user_id}` - Update user (admins only)
- `DELETE /api/v1/users/{user_id}` - Delete user (admins only)

### Roles and Permissions
- `GET /api/v1/roles/` - List roles
- `POST /api/v1/roles/` - Create role
- `PUT /api/v1/roles/{role_id}` - Update role
- `DELETE /api/v1/roles/{role_id}` - Delete role
- `GET /api/v1/roles/permissions` - List permissions
- `POST /api/v1/roles/permissions` - Create permission
- `PUT /api/v1/roles/permissions/{permission_id}` - Update permission
- `DELETE /api/v1/roles/permissions/{permission_id}` - Delete permission

## Project Structure

```
auth-service/
├── alembic/              # Database migrations
├── app/
│   ├── api/             # API Endpoints
│   │   ├── v1/         # API Version 1
│   │   └── deps.py     # API Dependencies
│   ├── core/           # Configuration and utilities
│   │   ├── config.py   # Application configuration
│   │   └── security.py # Security functions
│   ├── db/             # Database configuration
│   ├── models/         # SQLAlchemy models
│   └── schemas/        # Pydantic schemas
├── tests/              # Unit and integration tests
├── .env               # Environment variables
├── docker-compose.yml # Docker configuration
├── Dockerfile        # Docker build file
└── requirements.txt  # Python dependencies
```

## Development and Testing

### Run Tests
```bash
# Run all tests
docker-compose exec app pytest

# Run tests with coverage
docker-compose exec app pytest --cov=app tests/

# Run specific tests
docker-compose exec app pytest tests/test_auth.py
```

### Database Migrations
```bash
# Create a new migration
docker-compose exec app alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec app alembic upgrade head

# Revert migrations
docker-compose exec app alembic downgrade -1
```

## Security Features

- Password encryption with bcrypt
- JWT-based token authentication
- Token blacklist for logout
- Rate limiting to prevent brute-force attacks
- Role-based access control
- Session management with Redis
- Secure password reset flow
- Email verification
- Security headers (CORS, CSP, etc.)
- Data validation with Pydantic

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Make sure the tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for more details.

## Support

If you encounter any issues or have suggestions, please:
1. Review the documentation
2. Search existing issues
3. Create a new issue if necessary

## Acknowledgements

- FastAPI for the excellent framework
- SQLAlchemy for the ORM
- Pydantic for data validation
- The open-source community