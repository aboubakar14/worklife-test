from app.model import EmployeeModel
from app.repository.base import BaseRepository


class _EmployeeRepository(BaseRepository):
    def get_by_id(self, session, employee_id):
        return self._query(session).filter(self.model.id == employee_id)

    def create(self, session, obj_in):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        session.commit()
        return db_obj


EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
