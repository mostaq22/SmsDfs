from pydantic import BaseModel
from database import Base


class LogModel(BaseModel):
    content_type: str
    object_id: str = None
    log_type: str
    log_details: str
    created_by: str
    updated_by: str = None


Log = Base.classes.log
