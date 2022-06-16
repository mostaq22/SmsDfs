from pydantic import BaseModel
from database import Base


class MnoModel(BaseModel):
    name: str
    mno_code: str = None
    current_credit: str


Mno = Base.classes.mno
