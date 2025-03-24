import sqlalchemy as sa
from sqlalchemy.orm import relationship
from .base import BaseModel


class EmployeeModel(BaseModel):
    __tablename__ = "employee"
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)

    vacations = relationship(
        "VacationModel", back_populates="employee", cascade="all, delete-orphan"
    )
