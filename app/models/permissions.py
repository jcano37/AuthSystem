from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import CustomBase as Base


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    resource_type_id = Column(Integer, ForeignKey("resource_types.id"), nullable=False)
    action = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    resource_type = relationship("ResourceType", back_populates="permissions")
    roles = relationship(
        "Role", secondary="role_permission", back_populates="permissions"
    )
