import time
import uuid

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse

from collection.sms import SmsResponseCollection
from database import session, Base
from utils.log import AppLog
from fastapi import Request


class SmsRepository:
    __data = None

    def __init__(self, data, request: Request = None, **kwargs):
        sms_dict = data.dict()
        sms_dict['created_by'] = 'test'  # will assign from request
        sms_dict['client_id'] = 1  # will assign from request
        sms_dict['message_id'] = str(uuid.uuid1()) + "-" + str(time.time())
        sms_dict.pop('mno_code')
        self.__data = sms_dict

    def store(self):
        try:
            sms_obj = Base.classes.sms(**self.__data)
            session.add(sms_obj)
            session.flush()
            session.commit()
            AppLog(log_details="SMS Stored. PK:- " + str(sms_obj.id)).save()
            return JSONResponse(content=SmsResponseCollection(sms_obj).data, status_code=200)
        except SQLAlchemyError as e:
            session.rollback()
            AppLog(log_details=str(e)).save()
            raise HTTPException(status_code=500)
