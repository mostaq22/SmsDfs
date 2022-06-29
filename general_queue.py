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
        sms = Base.classes.sms
        sms_map = Base.classes.sms
        sms_list = session.query(sms_map).filter(sms_map.status == 'pending', sms_map.sms_type == 'queue',
                                                 sms.start_datetime == None,
                                                 sms.end_datetime == None).all()
        print(len(sms_list))
        for sms_row in sms_list:
            self.sms_obj = sms_row
            SmsDispatch(sms_row).send()


if __name__ == "__main__":
    SmsQueue().start()
