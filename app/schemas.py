"""
Pydantic schemas for Employee CRUD API.
Uses Pydantic v2 with proper validation and type hints.
"""

from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
import re
from pydantic import field_validator

class EmployeeBase(BaseModel):
    """Base schema with common employee fields."""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Employee's full name"
    )
    
    email: EmailStr = Field(
        ...,
        max_length=255,
        description="Unique email address"
    )
    
    department: Optional[str] = Field(
        None,
        max_length=100,
        description="Department name"
    )
    
    salary: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Annual salary (must be ≥ 0)"
    )
    @field_validator("name", "department")
    @classmethod
    def reject_html(cls, value):
        if value is not None and re.search(r"<[^>]+>", value):
            raise ValueError("HTML content is not allowed")
        return value


class EmployeeCreate(EmployeeBase):
    """Schema for creating a new employee."""
    pass


class EmployeeUpdate(BaseModel):
    """Schema for updating an employee (all fields optional)."""
    
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Employee's full name"
    )
    
    email: Optional[EmailStr] = Field(
        None,
        max_length=255,
        description="Unique email address"
    )
    
    department: Optional[str] = Field(
        None,
        max_length=100,
        description="Department name"
    )
    
    salary: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Annual salary (must be ≥ 0)"
    )


class EmployeeResponse(EmployeeBase):
    """Schema for employee responses (reads from database)."""
    
    id: int = Field(
        ...,
        gt=0,
        description="Employee ID"
    )
    
    # Pydantic config to work with SQLAlchemy ORM objects
    model_config = ConfigDict(from_attributes=True)


class EmployeeList(BaseModel):
    """Schema for paginated list of employees."""
    
    employees: List[EmployeeResponse] = Field(
        ...,
        description="List of employees"
    )
    
    total: int = Field(
        ...,
        ge=0,
        description="Total number of employees"
    )
    
    page: int = Field(
        ...,
        gt=0,
        description="Current page number"
    )
    
    size: int = Field(
        ...,
        gt=0,
        description="Number of items per page"
    )   


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str