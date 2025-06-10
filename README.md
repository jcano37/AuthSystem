# Sistema de Autenticación

Un servicio robusto de autenticación y autorización construido con FastAPI, que soporta JWT y OAuth2 Password Flow. Este sistema proporciona una base sólida para la gestión de usuarios, roles y permisos en aplicaciones modernas.

## 🚀 Características Principales

- 🔐 Autenticación de usuarios con tokens JWT
- 👥 Control de acceso basado en roles (RBAC)
- 💾 Gestión de sesiones con Redis
- 🔒 Cifrado de contraseñas con bcrypt
- 📧 Verificación de correo electrónico
- 🔄 Funcionalidad de restablecimiento de contraseña
- 🛡️ Limitación de tasa de solicitudes
- 🐳 Soporte para Docker
- 📦 Migraciones de base de datos con Alembic
- ✅ Validación de datos con Pydantic
- 🧪 Suite completa de pruebas

## 📋 Requisitos Previos

- Docker y Docker Compose
- Python 3.11+
- PostgreSQL 16+
- Redis 7+

## 🛠️ Dependencias Principales

- FastAPI 0.109.2
- Uvicorn 0.27.1
- SQLAlchemy 2.0.27
- Pydantic 2.6.1
- Python-Jose 3.3.0
- Passlib 1.7.4
- Redis 5.0.1
- Alembic 1.13.1
- Pytest 8.0.0

## 🚀 Inicio Rápido

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd auth-service
```

2. Crea un archivo `.env` en el directorio raíz:
```env
# Base de datos
DATABASE_URL=postgresql://postgres:postgres@db:5432/auth_db

# Redis
REDIS_URL=redis://redis:6379/0

# Seguridad
SECRET_KEY=tu-clave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email (opcional)
SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-contraseña-de-aplicación
```

3. Construye e inicia los contenedores:
```bash
docker-compose up --build
```

4. Ejecuta las migraciones de la base de datos:
```bash
docker-compose exec app alembic upgrade head
```

El servicio estará disponible en `http://localhost:8000`

## 📚 Documentación de la API

Una vez que el servicio esté en ejecución, puedes acceder a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔌 Endpoints de la API

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión con usuario/correo y contraseña
- `POST /api/v1/auth/register` - Registrar un nuevo usuario
- `POST /api/v1/auth/refresh` - Renovar token de acceso
- `POST /api/v1/auth/logout` - Cerrar sesión e invalidar sesión
- `POST /api/v1/auth/verify-email` - Verificar correo electrónico
- `POST /api/v1/auth/reset-password` - Solicitar restablecimiento de contraseña
- `POST /api/v1/auth/reset-password-confirm` - Confirmar restablecimiento de contraseña

### Usuarios
- `GET /api/v1/users/me` - Obtener usuario actual
- `PUT /api/v1/users/me` - Actualizar usuario actual
- `GET /api/v1/users/{user_id}` - Obtener usuario por ID
- `GET /api/v1/users/` - Listar usuarios (solo administradores)
- `POST /api/v1/users/` - Crear usuario (solo administradores)
- `PUT /api/v1/users/{user_id}` - Actualizar usuario (solo administradores)
- `DELETE /api/v1/users/{user_id}` - Eliminar usuario (solo administradores)

### Roles y Permisos
- `GET /api/v1/roles/` - Listar roles
- `POST /api/v1/roles/` - Crear rol
- `PUT /api/v1/roles/{role_id}` - Actualizar rol
- `DELETE /api/v1/roles/{role_id}` - Eliminar rol
- `GET /api/v1/roles/permissions` - Listar permisos
- `POST /api/v1/roles/permissions` - Crear permiso
- `PUT /api/v1/roles/permissions/{permission_id}` - Actualizar permiso
- `DELETE /api/v1/roles/permissions/{permission_id}` - Eliminar permiso

## 🏗️ Estructura del Proyecto

```
auth-service/
├── alembic/              # Migraciones de base de datos
├── app/
│   ├── api/             # Endpoints de la API
│   │   ├── v1/         # Versión 1 de la API
│   │   └── deps.py     # Dependencias de la API
│   ├── core/           # Configuración y utilidades
│   │   ├── config.py   # Configuración de la aplicación
│   │   └── security.py # Funciones de seguridad
│   ├── db/             # Configuración de base de datos
│   ├── models/         # Modelos SQLAlchemy
│   └── schemas/        # Esquemas Pydantic
├── tests/              # Pruebas unitarias y de integración
├── .env               # Variables de entorno
├── docker-compose.yml # Configuración de Docker
├── Dockerfile        # Archivo de construcción Docker
└── requirements.txt  # Dependencias de Python
```

## 🧪 Desarrollo y Pruebas

### Ejecutar Pruebas
```bash
# Ejecutar todas las pruebas
docker-compose exec app pytest

# Ejecutar pruebas con cobertura
docker-compose exec app pytest --cov=app tests/

# Ejecutar pruebas específicas
docker-compose exec app pytest tests/test_auth.py
```

### Migraciones de Base de Datos
```bash
# Crear una nueva migración
docker-compose exec app alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
docker-compose exec app alembic upgrade head

# Revertir migraciones
docker-compose exec app alembic downgrade -1
```

## 🔒 Características de Seguridad

- 🔐 Cifrado de contraseñas con bcrypt
- 🎟️ Autenticación basada en tokens JWT
- ⛔ Lista negra de tokens para cierre de sesión
- 🛡️ Limitación de tasa para prevenir ataques de fuerza bruta
- 👥 Control de acceso basado en roles
- 💾 Gestión de sesiones con Redis
- 🔄 Flujo seguro de restablecimiento de contraseña
- 📧 Verificación de correo electrónico
- 🔒 Headers de seguridad (CORS, CSP, etc.)
- 🔍 Validación de datos con Pydantic

## 🤝 Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Realiza tus cambios
4. Asegúrate de que las pruebas pasen (`pytest`)
5. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
6. Push a la rama (`git push origin feature/AmazingFeature`)
7. Abre un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## 📞 Soporte

Si encuentras algún problema o tienes alguna sugerencia, por favor:
1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue si es necesario

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- SQLAlchemy por el ORM
- Pydantic por la validación de datos
- La comunidad de código abierto 