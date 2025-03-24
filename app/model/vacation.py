import sqlalchemy as sa
from sqlalchemy.orm import relationship
from .base import BaseModel


class VacationModel(BaseModel):
    __tablename__ = "vacation"

    employee_id = sa.Column(
        BaseModel.id.type,
        sa.ForeignKey("employee.id", ondelete="CASCADE"),
        nullable=False,
    )
    type = sa.Column(
        sa.SmallInteger, nullable=False, comment="Vacation type: 0 = Unpaid, 1 = Paid"
    )
    start_date = sa.Column(sa.Date, nullable=False)
    end_date = sa.Column(sa.Date, nullable=False)

    __table_args__ = (sa.CheckConstraint("type IN (0, 1)", name="check_vacation_type"),)

    employee = relationship("EmployeeModel", back_populates="vacations")
