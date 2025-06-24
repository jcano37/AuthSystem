from typing import Any

from sqlalchemy.orm import declarative_base, declared_attr

Base = declarative_base()


class CustomBase(Base):
    __abstract__ = True
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
