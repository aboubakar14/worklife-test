from typing import Optional, List
from uuid import UUID
from datetime import date

from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.vacation import VacationService
from app.schema import VacationResponse

router = APIRouter()


@router.get("/", response_model=List[VacationResponse])
def search_vacations(
    session: Session = Depends(get_db),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    type: Optional[int] = Query(
        None, description="Vacation type: 0 for Unpaid, 1 for Paid"
    ),
    employee_id: Optional[UUID] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
):
    return VacationService.search_vacations(
        session=session,
        start_date=start_date,
        end_date=end_date,
        vacation_type=type,
        employee_id=employee_id,
        first_name=first_name,
        last_name=last_name,
    )
