from pydantic import BaseModel


class MnpModel(BaseModel):
    mobile_number: str
    mno_code: str = None
