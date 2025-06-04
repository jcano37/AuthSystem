# Sistema de Autenticación

Un servicio robusto de autenticación y autorización construido con FastAPI, que soporta JWT y OAuth2 Password Flow.

## Características

- Autenticación de usuarios con tokens JWT
- Control de acceso basado en roles (RBAC)
- Gestión de sesiones con Redis
- Cifrado de contraseñas con bcrypt
- Verificación de correo electrónico
- Funcionalidad de restablecimiento de contraseña
- Limitación de tasa de solicitudes
- Soporte para Docker
- Migraciones de base de datos con Alembic

## Requisitos Previos

- Docker y Docker Compose
- Python 3.11+
- PostgreSQL 16+
- Redis 7+

## Inicio Rápido

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd auth-service
```

2. Crea un archivo `.env` en el directorio raíz:
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/auth_db
REDIS_URL=redis://redis:6379/0
SECRET_KEY=tu-clave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
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

## Documentación de la API

Una vez que el servicio esté en ejecución, puedes acceder a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints de la API

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión con usuario/correo y contraseña
- `POST /api/v1/auth/register` - Registrar un nuevo usuario
- `POST /api/v1/auth/refresh` - Renovar token de acceso
- `POST /api/v1/auth/logout` - Cerrar sesión e invalidar sesión

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

## Desarrollo

### Estructura del Proyecto
```
auth-service/
├── alembic/              # Migraciones de base de datos
├── app/
│   ├── api/             # Endpoints de la API
│   ├── core/            # Funcionalidad principal
│   ├── db/              # Configuración de base de datos
│   ├── models/          # Modelos SQLAlchemy
│   └── schemas/         # Esquemas Pydantic
├── tests/               # Archivos de prueba
├── .env                 # Variables de entorno
├── docker-compose.yml   # Configuración de Docker
├── Dockerfile          # Archivo de construcción Docker
└── requirements.txt    # Dependencias de Python
```

### Ejecutar Pruebas
```bash
docker-compose exec app pytest
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

## Características de Seguridad

- Cifrado de contraseñas con bcrypt
- Autenticación basada en tokens JWT
- Lista negra de tokens para cierre de sesión
- Limitación de tasa para prevenir ataques de fuerza bruta
- Control de acceso basado en roles
- Gestión de sesiones
- Flujo seguro de restablecimiento de contraseña
- Verificación de correo electrónico

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu característica
3. Realiza tus cambios
4. Envía tus cambios a la rama
5. Crea un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles. 