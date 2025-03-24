from pydantic import ConfigDict, BaseModel, UUID4, field_validator, ValidationInfo
from datetime import date
from typing import Literal, Optional


class VacationBase(BaseModel):
    start_date: date
    end_date: date
    type: Literal[0, 1]

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, end_date: date, values: ValidationInfo):
        start_date = values.data.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("end_date cannot be before start_date")
        return end_date


class VacationResponse(VacationBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    employee_id: UUID4


class VacationUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    type: Optional[Literal[0, 1]] = None

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, end_date: Optional[date], values):
        start_date = values.data.get("start_date")
        if start_date and end_date and end_date < start_date:
            raise ValueError("end_date cannot be before start_date")
        return end_date
