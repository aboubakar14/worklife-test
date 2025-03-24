from sqlalchemy.orm import Session
from uuid import UUID
from app.repository.employee import EmployeeRepository


class _EmployeeService:
    def __init__(self):
        self.repository = EmployeeRepository

    def create_employee(self, session: Session, employee_data: dict):
        """
        Create a new employee.

        Args:
            session (Session): The database session used to create the employee.
            employee_data (dict): The data for the new employee.

        Returns:
            EmployeeModel: The new employee object.
        """
        return self.repository.create(session=session, obj_in=employee_data)

    def get_employee(self, session: Session, employee_id: UUID):
        """
        Retrieve an employee by their unique identifier.

        Args:
            session (Session): The database session used to query the employee.
            employee_id (UUID): The unique identifier of the employee.

        Returns:
            EmployeeModel: The employee object if found, otherwise None.
        """

        return self.repository.get(session=session, id=employee_id)

    def get_employees(self, session: Session):
        """
        Retrieve a list of all employees from the repository.

        Args:
            session (Session): The database session used to query the employees.

        Returns:
            List[EmployeeModel]: A list of employee objects.
        """

        return self.repository.get_many(session=session)


EmployeeService = _EmployeeService()
