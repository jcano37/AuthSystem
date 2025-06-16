from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class ResourceType(Base):
    __tablename__ = "resource_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with permissions
    permissions = relationship("Permission", back_populates="resource_type")
