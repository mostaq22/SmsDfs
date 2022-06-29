import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from repository.send_sms import SmsDispatch

print(os.path.dirname(os.path.realpath(__file__)) + "/.env")
dotenv_path = '/home/mostaq/PycharmProjects/SmsService/.env'
dotenv_path = os.path.dirname(os.path.realpath(__file__)) + "/.env"
load_dotenv(dotenv_path)
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)  # exporting


class SmsQueue:
    sms_list: list
    sms_obj: object

    def start(self):
        with engine.connect() as con:
            sms_list = con.execute("""
            select *
            from sms
            where sms_type = 'queue'
              and status = 'pending'
              and ((start_datetime <= CURRENT_TIMESTAMP and end_datetime is NULL)
              or (start_datetime is NULL and end_datetime > CURRENT_TIMESTAMP )
            or (CURRENT_TIMESTAMP between start_datetime and end_datetime))
            """)

        for sms_row in sms_list:
            sms_obj = Base.classes.sms(**dict(sms_row))
            print(sms_obj, "\n")
            SmsDispatch(sms_obj).send()


if __name__ == "__main__":
    SmsQueue().start()
