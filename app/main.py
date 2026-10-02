"""
Main FastAPI application for Employee CRUD API.
Minimal setup with database table creation on startup.
"""

import os

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_tables
from app.routers import employees,auth

from fastapi.middleware.cors import CORSMiddleware
from app.security.headers import SecurityHeadersMiddleware
from app.middleware.rate_limit import RateLimitMiddleware   
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    
    Creates database tables on startup.
    No shutdown operations needed for SQLite.
    """
    # Startup: create database tables
    create_tables()
    print("Database tables created")
    
    yield
    
    # Shutdown: (optional cleanup can go here)
    # No cleanup needed for SQLite in this minimal setup

# Create FastAPI application with lifespan
app = FastAPI(
    title="Employee CRUD API",
    description="Minimal Employee CRUD API for security audit project",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    RateLimitMiddleware,
    max_requests=15,
    window_seconds=60
)

if os.getenv("FORCE_HTTPS", "false").lower() == "true":
    app.add_middleware(HTTPSRedirectMiddleware)

# Include routers
app.include_router(employees.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    """
    Root endpoint for health check and API information.
    """
    return {
        "message": "Employee CRUD API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }