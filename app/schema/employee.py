from pydantic import BaseModel, ConfigDict, UUID4


class EmployeeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str


class EmployeeResponse(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
