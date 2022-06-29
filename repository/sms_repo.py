import time
import uuid

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse

from collection.sms import SmsResponseCollection
from database import session, Base
from utils.haser import Hasher
from utils.log import AppLog
from fastapi import Request
from repository.send_sms import SmsDispatch


class SmsRepository:
    __data = None
    request: object

    def __init__(self, data, request: Request = None, **kwargs):
        self.request = request
        sms_dict = data.dict()
        sms_dict['message_id'] = str(uuid.uuid1()) + "-" + str(time.time())
        sms_dict.pop('mno_code')
        self.username = sms_dict.pop('username')
        self.password = sms_dict.pop('password')
        self.__data = sms_dict

    def store(self):
        client = self.is_valid_client()
        if client:
            try:
                self.__data['client_id'] = client.id
                self.__data['created_by'] = client.name
                sms_obj = Base.classes.sms(**self.__data)
                session.add(sms_obj)
                session.flush()
                session.commit()
                AppLog(log_details="SMS Stored. PK:- " + str(sms_obj.id)).save()
                if sms_obj.sms_type == 'quick':
                    SmsDispatch(sms_obj).send()
                    sms_map = Base.classes.sms
                    sms_obj = session.query(sms_map).get(sms_obj.id)
                    return JSONResponse(content=SmsResponseCollection(sms_obj).data, status_code=200)
                else:
                    return JSONResponse(content=SmsResponseCollection(sms_obj).data, status_code=200)
            except SQLAlchemyError as e:
                session.rollback()
                AppLog(log_details=str(e)).save()
                raise HTTPException(status_code=500)
        else:
            AppLog(log_details="Authentication Failed: " + self.username + " " + self.password).save()
            return JSONResponse(content={"detail": "Authentication Failed"}, status_code=401)

    # validate the client from db
    def is_valid_client(self):
        client_host = self.request.client.host
        # return False
        client_map = Base.classes.client
        client = session.query(client_map).filter(client_map.username == self.username).first()
        if client:
            # ip whitelist checking
            if client.white_list and len(client.white_list) > 0 and client_host not in client.white_list:
                return False
            # password verification
            verify = Hasher.verify_password(plain_password=self.password + client.c_uuid,
                                            hashed_password=client.password)

            if verify:
                return client
            else:
                return None
        else:
            return None
