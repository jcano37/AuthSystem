from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import CustomBase as Base


class ResourceType(Base):
    __tablename__ = "resource_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Relationship with permissions
    permissions = relationship("Permission", back_populates="resource_type")
    company = relationship("Company", back_populates="resource_types")
