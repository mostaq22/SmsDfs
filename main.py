from fastapi import FastAPI
from sms_model import SmsModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def test(name: int):
    print(name)


@app.post("/send_sms/")
async def say_hello(sms: SmsModel):
    return sms
