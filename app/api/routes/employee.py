from typing import Optional
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.employee import EmployeeService
from app.services.vacation import VacationService
from app.schema import (
    EmployeeBase,
    EmployeeResponse,
    VacationBase,
    VacationResponse,
    VacationUpdate,
)

router = APIRouter()


@router.post("/", response_model=Optional[EmployeeResponse])
def create_employee(session: Session = Depends(get_db), *, employee: EmployeeBase):
    return EmployeeService.create_employee(session=session, employee_data=employee)


@router.get("/", response_model=Optional[list[EmployeeResponse]])
def get_employees(session: Session = Depends(get_db)):
    """
    Retrieve a list of all employees.

    This endpoint returns a list of employees from the database. If no employees
    are found, it returns an empty list.

    Returns:
    - A list of employee data or None if no employees exist.
    """

    return EmployeeService.get_employees(session=session)


@router.get("/{employee_id}", response_model=Optional[EmployeeResponse])
def get_employee(session: Session = Depends(get_db), *, employee_id: UUID):
    result = EmployeeService.get_employee(session=session, employee_id=employee_id)
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result


@router.post("/{employee_id}/vacations", response_model=VacationResponse)
def create_vacation(
    session: Session = Depends(get_db),
    *,
    employee_id: UUID,
    vacation_data: VacationBase
):
    try:
        return VacationService.create_vacation(
            session=session, employee_id=employee_id, vacation_data=vacation_data
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{employee_id}/vacations", response_model=Optional[list[VacationResponse]])
def get_vacations(session: Session = Depends(get_db), *, employee_id: UUID):
    try:
        return VacationService.get_vacations_by_employee_id(
            session=session, employee_id=employee_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{employee_id}/vacations/{vacation_id}", response_model=VacationResponse)
def patch_vacation(
    session: Session = Depends(get_db),
    *,
    employee_id: UUID,
    vacation_id: UUID,
    vacation_data: VacationUpdate
):
    return VacationService.update_vacation(
        session=session,
        employee_id=employee_id,
        vacation_id=vacation_id,
        vacation_data=vacation_data,
    )


@router.delete("/{employee_id}/vacations/{vacation_id}", status_code=204)
def delete_vacation(
    session: Session = Depends(get_db), *, employee_id: UUID, vacation_id: UUID
):
    VacationService.delete_vacation(
        session=session, employee_id=employee_id, vacation_id=vacation_id
    )
