from pydantic import BaseModel
from database import Base


class MnpModel(BaseModel):
    mobile_number: str
    mno_code: str = None


Mnp = Base.classes.mnp
