"""
Minimal database configuration for FastAPI with SQLAlchemy 2.x
Uses DeclarativeBase pattern and environment variables
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

# Database URL from environment variable, default to SQLite for development
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./employee_db.sqlite"
)

# SQLAlchemy 2.x engine with SQLite configuration
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Session factory for creating database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all SQLAlchemy models using DeclarativeBase
class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    All model classes should inherit from this Base class.
    """
    pass

# FastAPI dependency to provide database session
def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session to FastAPI routes.
    
    Yields:
        Session: SQLAlchemy database session
        
    Important: Does NOT automatically commit - you must handle 
    commits explicitly in your route handlers or services.
    
    Usage:
        @app.get("/employees")
        def get_employees(db: Session = Depends(get_db)):
            # Use db session here
            # Commit or rollback as needed
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional helper function to create tables
def create_tables():
    """
    Create all database tables defined in models.
    Call this during application startup.
    """
    Base.metadata.create_all(bind=engine)