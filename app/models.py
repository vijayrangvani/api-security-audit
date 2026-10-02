from sqlalchemy import String, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    
    department: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    
    salary: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True
    )