from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.model import VacationModel, EmployeeModel
from typing import Optional, List
from datetime import date, timedelta
from uuid import UUID

from app.model import VacationModel
from app.repository.base import BaseRepository


class _VacationRepository(BaseRepository):
    def get_by_id(self, session, vacation_id):
        """
        Retrieve a vacation by its unique identifier.

        Args:
            session (Session): The database session used to query the vacation.
            vacation_id (UUID): The unique identifier of the vacation.

        Returns:
            VacationModel: The vacation object if found.
        """
        return self._query(session).filter(self.model.id == vacation_id).first()

    def get_by_employee(self, session, employee_id):
        """
        Retrieve a list of all vacations for the given employee.

        Args:
            session (Session): The database session used to query the employee's vacations.
            employee_id (UUID): The unique identifier of the employee.

        Returns:
            List[VacationModel]: A list of vacation objects for the given employee.
        """
        return self._query(session).filter(self.model.employee_id == employee_id).all()

    def create(self, session, obj_in, employee_id):
        """
        Create a new vacation record for the given employee.

        Args:
            session (Session): The database session used to create the vacation.
            obj_in: The data for the new vacation, typically a Pydantic model.
            employee_id (UUID): The unique identifier of the employee.

        Returns:
            VacationModel: The newly created vacation object.
        """

        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, employee_id=employee_id)
        session.add(db_obj)
        session.commit()
        return db_obj

    def delete(self, session, vacation_id):
        """
        Delete a vacation by its unique identifier.

        Args:
            session (Session): The database session used to delete the vacation.
            vacation_id (UUID): The unique identifier of the vacation to delete.

        Returns:
            VacationModel: The deleted vacation object if found, None otherwise.
        """
        vacation = self.get_by_id(session, vacation_id)
        if vacation:
            session.delete(vacation)
            session.commit()
            return vacation
        return None

    def patch(self, session, vacation_id, obj_in: dict):
        """
        Update an existing vacation record.

        Args:
            session (Session): The database session used to update the vacation.
            vacation_id (UUID): The unique identifier of the vacation to update.
            obj_in (dict): The dictionary of values to update the vacation with.

        Returns:
            VacationModel: The updated vacation object if found, None otherwise.
        """
        vacation = self.get_by_id(session, vacation_id)
        if vacation:
            for key, value in obj_in.items():
                setattr(vacation, key, value)
            session.commit()
            return vacation
        return None

    def search(
        self,
        session: Session,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        vacation_type: Optional[int] = None,
        employee_id: Optional[UUID] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> List[VacationModel]:
        """
        Search for vacations by date, type, employee_id, first_name, and last_name.

        If `start_date` and/or `end_date` are provided, the query will filter on vacations that
        overlap or are contiguous with the given date range.

        If `first_name` and/or `last_name` are provided, the query will filter on vacations that
        match the given name criteria.

        Args:
            session (Session): The database session used to query the vacations.
            start_date (Optional[date]): The start date to search for.
            end_date (Optional[date]): The end date to search for.
            vacation_type (Optional[int]): The vacation type to search for.
            employee_id (Optional[UUID]): The employee_id to search for.
            first_name (Optional[str]): The first name to search for.
            last_name (Optional[str]): The last name to search for.

        Returns:
            List[VacationModel]: A list of vacation objects that match the search criteria.
        """
        filters = []

        if start_date:
            filters.append(VacationModel.start_date == start_date)
        if end_date:
            filters.append(VacationModel.end_date == end_date)
        if vacation_type is not None:
            filters.append(VacationModel.type == vacation_type)
        if employee_id:
            filters.append(VacationModel.employee_id == employee_id)

        query = select(VacationModel)
        # If filtering by name, we must join EmployeeModel
        if first_name or last_name:
            query = query.join(EmployeeModel)
            if first_name:
                filters.append(EmployeeModel.first_name.ilike(f"%{first_name}%"))
            if last_name:
                filters.append(EmployeeModel.last_name.ilike(f"%{last_name}%"))

        if filters:
            query = query.where(*filters)

        return session.execute(query).scalars().all()

    def get_overlapping_or_contiguous(
        self,
        session: Session,
        employee_id: UUID,
        vacation_type: str,
        start_date,
        end_date,
    ) -> List[VacationModel]:
        """
        Retrieve a list of existing vacations for the given employee that overlap or are contiguous with the given date range.

        A vacation is considered overlapping if its start date is before the given end date and its end date is after the given start date.
        A vacation is considered contiguous if its start date is one day after the given end date, or if its end date is one day before the given start date.

        Args:
            session (Session): The database session used to query the employee's vacations.
            employee_id (UUID): The unique identifier of the employee.
            vacation_type (str): The type of vacation to filter by.
            start_date (date): The start date of the vacation to filter by.
            end_date (date): The end date of the vacation to filter by.

        Returns:
            List[VacationModel]: A list of overlapping or contiguous vacation objects for the given employee.
        """
        return (
            session.query(VacationModel)
            .filter(
                VacationModel.employee_id == employee_id,
                VacationModel.type == vacation_type,
                or_(
                    # right overlap
                    (VacationModel.start_date <= end_date)
                    & (VacationModel.end_date >= start_date),
                    # left overlap
                    (VacationModel.start_date >= start_date)
                    & (VacationModel.start_date <= end_date),
                    (VacationModel.end_date == start_date - timedelta(days=1)),
                    (VacationModel.start_date == end_date + timedelta(days=1)),
                ),
            )
            .order_by(VacationModel.start_date)
            .all()
        )


VacationRepository = _VacationRepository(model=VacationModel)
