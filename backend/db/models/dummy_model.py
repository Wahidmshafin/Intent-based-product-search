from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String
from pgvector.sqlalchemy import Vector
from backend.db.base import Base


class DummyModel(Base):
    """Model for demo purpose."""

    __tablename__ = "dummy_model"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=200))


class ProductTable(Base):
    """Product Table"""
    __tablename__ = "product_table"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    colorname: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    name: Mapped[str] = mapped_column(String())
    fulldescription: Mapped[str] = mapped_column(String())
    embedding: Mapped[list[float]] = mapped_column(Vector())
    
