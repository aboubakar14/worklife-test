from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@patch("app.api.routes.employee.EmployeeService")
def test_get_employees(mock_employee_service):
    mock_employee_service.get_employees.return_value = [{"first_name": "work", "last_name": "Life", "id": "804abfed-5f49-40bd-b913-51643b2e8f48"}]
    response = client.get("/employee/")
    assert response.status_code == 200
    assert response.json() == [{"first_name": "work", "last_name": "Life", "id": "804abfed-5f49-40bd-b913-51643b2e8f48"}]
