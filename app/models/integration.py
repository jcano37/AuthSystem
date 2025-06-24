from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import CustomBase as Base


class Integration(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    api_key = Column(String, unique=True, index=True, nullable=False)
    api_secret = Column(String, nullable=False)
    integration_type = Column(String, nullable=False)  # "oauth2", "api_key", etc.
    configuration = Column(JSON, nullable=True)  # Configuración específica
    callback_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Relationships
    company = relationship("Company", back_populates="integrations")
