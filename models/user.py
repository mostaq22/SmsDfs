from pydantic import BaseModel
from database import Base


class UserModel(BaseModel):
    pass


User = Base.classes.user
