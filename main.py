import time
from fastapi import FastAPI, Request

from models.sms import SmsModel
from repository.sms_repo import SmsRepository
from middleware import client_authentication

app = FastAPI()

app.middleware('http')(
    client_authentication
)


@app.post("/send_sms/")
async def store_sms(sms: SmsModel, request: Request):
    print(sms)
    return await SmsRepository(data=sms, request=request).store()
