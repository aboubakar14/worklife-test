from sqlalchemy.orm import Session
from uuid import UUID

from app.schema import VacationBase, VacationUpdate
from app.repository.vacation import VacationRepository
from app.repository.employee import EmployeeRepository


class _VacationService:

    def __init__(self):
        self.repository = VacationRepository

    def __get_employee(self, session: Session, employee_id: UUID):
        """
        Retrieve an employee by their unique identifier.

        Args:
            session (Session): The database session used to query the employee.
            employee_id (UUID): The unique identifier of the employee.

        Returns:
            EmployeeModel: The employee object if found.

        Raises:
            ValueError: If no employee with the given ID exists.
        """

        employee = EmployeeRepository.get(session=session, id=employee_id)
        if not employee:
            raise ValueError("Employee not found")
        return employee

    def create_vacation(
        self, session: Session, employee_id: UUID, vacation_data: VacationBase
    ):
        """
        Create a new vacation for the given employee.

        If any existing vacations of the same type overlap or are contiguous with the
        given date range, they are deleted and merged into a single vacation.

        Args:
            session (Session): The database session used to create the vacation.
            employee_id (UUID): The unique identifier of the employee.
            vacation_data (VacationBase): The data for the new vacation.

        Returns:
            VacationModel: The new vacation object.

        Raises:
            ValueError: If no employee with the given ID exists.
        """
        employee = self.__get_employee(session=session, employee_id=employee_id)

        existing_vacations = VacationRepository.get_overlapping_or_contiguous(
            session,
            employee_id,
            vacation_data.type,
            vacation_data.start_date,
            vacation_data.end_date,
        )

        if existing_vacations:
            new_start = min(vacation_data.start_date, existing_vacations[0].start_date)
            new_end = max(vacation_data.end_date, existing_vacations[-1].end_date)

            for vac in existing_vacations:
                VacationRepository.delete(session, vac.id)

            vacation = VacationBase(
                type=vacation_data.type, start_date=new_start, end_date=new_end
            )
            return VacationRepository.create(
                session=session, obj_in=vacation, employee_id=employee.id
            )

        vacation = VacationRepository.create(
            session=session, obj_in=vacation_data, employee_id=employee.id
        )

        return vacation

    def get_vacations_by_employee_id(self, session: Session, employee_id: UUID):
        """
        Retrieve a list of all vacations for the given employee.

        Args:
            session (Session): The database session used to query the employee's vacations.
            employee_id (UUID): The unique identifier of the employee.

        Returns:
            List[VacationModel]: A list of vacation objects for the given employee.
        """
        employee = self.__get_employee(session=session, employee_id=employee_id)

        return employee.vacations

    def update_vacation(
        self,
        session: Session,
        employee_id: UUID,
        vacation_id: UUID,
        vacation_data: VacationUpdate,
    ):
        """
        Update the given vacation, merging the given data with the existing vacation.

        If the given vacation data overlaps or is contiguous with existing vacations, merge them into one.

        Args:
            session (Session): The database session used to update the vacation.
            employee_id (UUID): The unique identifier of the employee.
            vacation_id (UUID): The unique identifier of the vacation to update.
            vacation_data (VacationUpdate): The data to update the vacation with.

        Returns:
            VacationModel: The updated vacation object.

        Raises:
            ValueError: If the given vacation does not exist.
        """
        employee = self.__get_employee(session=session, employee_id=employee_id)

        vacation = [
            vacation for vacation in employee.vacations if vacation.id == vacation_id
        ]

        if not vacation:
            raise ValueError("Vacation not found")

        update_data = vacation_data.dict(exclude_unset=True)

        existing_vacations = VacationRepository.get_overlapping_or_contiguous(
            session,
            employee_id,
            vacation_data.type,
            vacation_data.start_date,
            vacation_data.end_date,
        )

        if existing_vacations:
            new_start = min(vacation_data.start_date, existing_vacations[0].start_date)
            new_end = max(vacation_data.end_date, existing_vacations[-1].end_date)

            for vac in existing_vacations:
                VacationRepository.delete(session, vac.id)

            update_data["start_date"] = new_start
            update_data["end_date"] = new_end
            return VacationRepository.patch(
                session=session, vacation_id=vacation_id, obj_in=update_data
            )

        updated_vacation = VacationRepository.patch(
            session=session, vacation_id=vacation_id, obj_in=update_data
        )

        return updated_vacation

    def search_vacations(
        self, session, start_date, end_date, type, employee_id, first_name, last_name
    ):
        """
        Search for vacations by date, type, employee_id, first_name, and last_name.

        Args:
            session (Session): The database session used to query the vacations.
            start_date (Optional[date]): The start date to search for.
            end_date (Optional[date]): The end date to search for.
            type (Optional[int]): The vacation type to search for.
            employee_id (Optional[UUID]): The employee_id to search for.
            first_name (Optional[str]): The first name to search for.
            last_name (Optional[str]): The last name to search for.

        Returns:
            List[VacationModel]: A list of vacation objects that match the search criteria.
        """
        return self.repository.search(
            session=session,
            start_date=start_date,
            end_date=end_date,
            vacation_type=type,
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
        )

    def delete_vacation(
        self, session: Session, employee_id: UUID, vacation_id: UUID
    ) -> bool:
        """
        Delete a vacation by its unique identifier.

        Args:
            session (Session): The database session used to delete the vacation.
            employee_id (UUID): The unique identifier of the employee.
            vacation_id (UUID): The unique identifier of the vacation to delete.

        Returns:
            bool: True if the vacation was deleted successfully, False otherwise.

        Raises:
            ValueError: If the given vacation does not exist.
        """
        employee = self.__get_employee(session=session, employee_id=employee_id)

        vacation = VacationRepository.get(session=session, id=vacation_id)
        if not vacation:
            raise ValueError("Vacation not found")

        VacationRepository.delete(session=session, vacation_id=vacation_id)


VacationService = _VacationService()
