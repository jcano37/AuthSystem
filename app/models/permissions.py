from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.roles import role_permission


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    resource_type_id = Column(Integer, ForeignKey("resource_types.id"), nullable=False)
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    roles = relationship(
        "Role", secondary=role_permission, back_populates="permissions"
    )
    resource_type = relationship("ResourceType", back_populates="permissions")
