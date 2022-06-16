from pydantic import BaseModel

from database import Base


class ClientModel(BaseModel):
    name: str
    client_id: str
    api_key: str


Client = Base.classes.client
