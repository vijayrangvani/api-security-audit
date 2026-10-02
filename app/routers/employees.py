"""
Employee CRUD router for FastAPI API.
Implements all CRUD operations with proper error handling.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Employee
from app.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeList
)
from app.security.api_key import verify_api_key
from app.security.jwt_auth import get_current_user

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    dependencies=[Depends(verify_api_key),
    Depends(get_current_user)]
)


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
) -> EmployeeResponse:
    """
    Create a new employee.
    
    Checks for duplicate email before creation.
    Returns the created employee with generated ID.
    """
    # Check for existing email
    existing_employee = db.query(Employee).filter(
        Employee.email == employee_data.email
    ).first()
    
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Create new employee
    employee = Employee(
        name=employee_data.name,
        email=employee_data.email,
        department=employee_data.department,
        salary=employee_data.salary
    )
    
    try:
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database constraint violation"
        )


@router.get(
    "/",
    response_model=EmployeeList
)
def list_employees(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
) -> EmployeeList:
    """
    List employees with pagination.
    
    Returns paginated list of employees with total count.
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # Get employees for current page
    employees = db.query(Employee).offset(offset).limit(size).all()
    
    # Get total count
    total = db.query(Employee).count()
    
    return EmployeeList(
        employees=employees,
        total=total,
        page=page,
        size=size
    )


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
) -> EmployeeResponse:
    """
    Get employee by ID.
    
    Returns 404 if employee not found.
    """
    employee = db.get(Employee, employee_id)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return employee


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db)
) -> EmployeeResponse:
    """
    Update employee (full or partial update).
    
    All fields are optional. Returns 404 if employee not found.
    Checks for duplicate email if email is being updated.
    """
    employee = db.get(Employee, employee_id)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Check for duplicate email if email is being updated
    if employee_data.email is not None and employee_data.email != employee.email:
        existing_employee = db.query(Employee).filter(
            Employee.email == employee_data.email
        ).first()
        
        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
    
    # Update fields if provided
    update_data = employee_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    try:
        db.commit()
        db.refresh(employee)
        return employee
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database constraint violation"
        )


@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def patch_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db)
) -> EmployeeResponse:
    """
    Partial update employee (alias for PUT).
    
    Same implementation as PUT since EmployeeUpdate has all optional fields.
    """
    return update_employee(employee_id, employee_data, db)


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete employee by ID.
    
    Returns 404 if employee not found.
    Returns 204 No Content on success.
    """
    employee = db.get(Employee, employee_id)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    db.delete(employee)
    db.commit()
    
    return None