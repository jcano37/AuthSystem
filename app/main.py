from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth, companies, integrations, permissions
from app.api.v1.endpoints import resources as resources_router
from app.api.v1.endpoints import roles, sessions, users, webhooks
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(
    sessions.router, prefix=f"{settings.API_V1_STR}/users", tags=["sessions"]
)
app.include_router(roles.router, prefix=f"{settings.API_V1_STR}/roles", tags=["roles"])
app.include_router(
    permissions.router,
    prefix=f"{settings.API_V1_STR}/permissions",
    tags=["permissions"],
)
app.include_router(
    resources_router.router,
    prefix=f"{settings.API_V1_STR}/resources",
    tags=["resources"],
)
app.include_router(
    companies.router,
    prefix=f"{settings.API_V1_STR}/companies",
    tags=["companies"],
)
app.include_router(
    integrations.router,
    prefix=f"{settings.API_V1_STR}/integrations",
    tags=["integrations"],
)
app.include_router(
    webhooks.router,
    prefix=f"{settings.API_V1_STR}/webhooks",
    tags=["webhooks"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Authentication Service",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }
