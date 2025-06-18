from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import CustomBase as Base


class UserRole(Base):
    __tablename__ = "user_role"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)


class RolePermission(Base):
    __tablename__ = "role_permission"
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_default = Column(Boolean, default=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Relationships
    users = relationship("User", secondary="user_role", back_populates="roles")
    permissions = relationship(
        "Permission", secondary="role_permission", back_populates="roles"
    )
    company = relationship("Company", back_populates="roles")
