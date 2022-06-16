from pydantic import BaseModel
from database import Base


class RoleModel(BaseModel):
    name: str
    status: bool
    permissions: dict


Role = Base.classes.role
