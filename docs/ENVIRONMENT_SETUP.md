# Environment Configuration Setup

## Overview
This guide explains how to configure the environment variables for the Auth System backend. All sensitive configuration has been moved from hardcoded values to environment variables for security.

## Quick Setup

### 1. Copy Environment Template
```bash
# Copy the template to create your environment file
cp .env.example .env
```

### 2. Configure Required Variables
Edit the `.env` file and replace the placeholder values:

#### Critical Security Settings (MUST CHANGE)
- `SECRET_KEY`: Generate with `openssl rand -hex 32`
- `POSTGRES_PASSWORD`: Use a strong database password
- `SMTP_PASSWORD`: Your email app password for password reset emails

#### Database Configuration
- `POSTGRES_SERVER`: Database host (localhost for local dev, db for docker)
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password (CHANGE FROM DEFAULT!)
- `POSTGRES_DB`: Database name

#### Email Configuration (Required for password reset)
- `SMTP_USER`: Your email address
- `SMTP_PASSWORD`: Your email app password
- `SMTP_HOST`: SMTP server (e.g., smtp.gmail.com)

## Environment Files Structure

### `.env` (Git Ignored)
Your actual environment configuration with real sensitive values.

### `.env.example` (Git Tracked)
Template with placeholder values for team reference.

### `development.env` (Git Tracked)
Example development configuration with secure defaults.

## Security Notes

### JWT Secret Key
The JWT secret key is critical for security. Generate a secure one:
```bash
# Generate a secure secret key
openssl rand -hex 32
```

### Database Security
- Never use default passwords in production
- Use strong passwords with mixed characters
- Consider using database connection pooling

### Email Configuration
For Gmail, use App Passwords instead of your regular password:
1. Enable 2FA on your Google account
2. Generate an App Password
3. Use the App Password in `SMTP_PASSWORD`

## Development vs Production

### Development Environment
The provided `development.env` contains secure defaults suitable for local development.

### Production Environment
For production, ensure:
- Generate new SECRET_KEY
- Use strong database passwords
- Configure proper CORS origins
- Set `DEBUG=false`
- Use production email service

## Docker Compose Integration

The `docker-compose.yml` has been updated to:
- Load environment variables from `.env` file
- Override specific settings for containerized services
- Use environment variables for database configuration

### Running with Docker
```bash
# The docker-compose will automatically use your .env file
docker-compose up -d
```

## Environment Variables Reference

### Application
- `PROJECT_NAME`: Application name
- `VERSION`: Application version
- `API_V1_STR`: API prefix path

### Database
- `POSTGRES_SERVER`: Database host
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name

### JWT Security
- `SECRET_KEY`: JWT signing key (CRITICAL)
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration

### Redis
- `REDIS_HOST`: Redis server host
- `REDIS_PORT`: Redis server port
- `REDIS_DB`: Redis database number
- `REDIS_PASSWORD`: Redis password (optional)

### Email
- `SMTP_TLS`: Use TLS encryption
- `SMTP_PORT`: SMTP port
- `SMTP_HOST`: SMTP server
- `SMTP_USER`: Email username
- `SMTP_PASSWORD`: Email password
- `EMAILS_FROM_EMAIL`: From email address
- `EMAILS_FROM_NAME`: From name

### Security
- `RATE_LIMIT_PER_MINUTE`: API rate limiting
- `MIN_PASSWORD_LENGTH`: Minimum password length
- `REQUIRE_SPECIAL_CHAR`: Require special characters
- `REQUIRE_NUMBER`: Require numbers
- `REQUIRE_UPPERCASE`: Require uppercase letters

### CORS
- `BACKEND_CORS_ORIGINS`: Allowed origins list

### Session & 2FA
- `SESSION_EXPIRE_DAYS`: Session expiration
- `ENABLE_2FA`: Enable two-factor authentication

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure all variables are defined in `.env`
2. **Database Connection**: Check database credentials and server availability
3. **Email Issues**: Verify SMTP configuration and app passwords
4. **JWT Errors**: Ensure SECRET_KEY is properly set and consistent

### Validation
Test your configuration:
```bash
# Run the application in development mode
python -m uvicorn app.main:app --reload

# Check if environment variables are loaded
python -c "from app.core.config import settings; print('Config loaded successfully')"
```

## Security Checklist

- [ ] Changed default SECRET_KEY
- [ ] Updated database passwords
- [ ] Configured email credentials
- [ ] Set appropriate CORS origins
- [ ] Verified .env is in .gitignore
- [ ] Removed any hardcoded secrets from code
- [ ] Tested application startup with new configuration 