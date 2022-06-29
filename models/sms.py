from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator, Field
from exceptions import MobileNumber
from app_config import get_config
from utils.general import generate_mno_list, get_mno_by_code
from database import Base, session

# Get all config related to sms class
CONFIG = get_config(
    ['MNO', 'SMS_TYPE', 'DEFAULT_SMS_TYPE', 'MASKING', 'TIME_INTERVAL'])  # required values for sms_model
MNO_CODE_LIST = generate_mno_list(list(CONFIG.get('MNO').values()))  # list of mno code - 018, 017 etc
MNO_LIST = list(CONFIG.get('MNO').keys())  # list mno RB, GP etc
SMS_TYPE = CONFIG.get('SMS_TYPE', None)  # get priority of sms - OTO, CNF etc
DEFAULT_SMS_TYPE = CONFIG.get('DEFAULT_SMS_TYPE', None)  # get default type of sms
MASKING = CONFIG.get('MASKING', None)  # get masking for sms


# print(MASKING)


class SmsModel(BaseModel):
    msisdn: str = Field(min_length=11, max_length=11)
    message: str = Field(min_length=1)
    mno: Union[str, None]
    sms_type: Union[str, None] = DEFAULT_SMS_TYPE  # Queue/quick
    mno_code: Union[str, None]
    campaign_id: Union[str, None]
    masking: str = Field(min_length=1)
    start_datetime: Union[datetime, None]
    end_datetime: Union[datetime, None]
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)

    class Config:
        """Extra configuration options"""
        anystr_strip_whitespace = True  # remove trailing whitespace

    @validator('msisdn')
    def is_valid_mobile_number(cls, value, **kwargs):
        """
          Rules of validation of a mobile number

          * Length must be 11
          * Start with 01
          * Must be string
          * Must be in MNO CODE [018, 011, 017 etc]
        """
        try:
            int(value)
        except ValueError:
            MobileNumber.invalid_msisdn()

        if not value.startswith('01'):
            MobileNumber.invalid_prefix()
        elif value[-11:-8] not in MNO_CODE_LIST:
            MobileNumber.invalid_mno_code()

        else:
            return value

    @validator('mno')
    def is_valid_mno(cls, value, values, **kwargs):
        """
        Validate the mno from payload. If empty then set mno from msisdn prefix

        :param value:
        :param values:
        :param kwargs:
        :return:
        """
        if value and value in MNO_LIST:
            return value
        elif value is None and 'msisdn' in values:
            mnp_map = Base.classes.mnp
            mnp = session.query(mnp_map).filter(mnp_map.mobile_number == values['msisdn']).first()
            if mnp:
                return mnp.mno_code
            else:
                return get_mno_by_code(mno_code=values['msisdn'][-11:-8], mno_data=CONFIG.get('MNO'))
        MobileNumber.invalid_mno()

    @validator('sms_type')
    def is_valid_sms_type(cls, value):
        """
        Validate the priority from payload. If empty then set to default priority.

        :param value:
        :return:
        """
        if value is None:
            return DEFAULT_SMS_TYPE
        elif len(value) > 0 and value in SMS_TYPE:
            return value
        MobileNumber.invalid_sms_type()

    @validator('mno_code')
    def is_valid_mno_code(cls, value, values):
        """
        :param value:
        :param values:
        :return:
        """
        if value is None and 'msisdn' in values:
            return values['msisdn'][-11:-8]
        elif value in MNO_CODE_LIST and 'msisdn' in values and values['msisdn'][-11:-8] == value:
            return value
        return MobileNumber.invalid_mno_code()

    @validator('masking')
    def is_valid_masking(cls, value):
        if value and value in MASKING and MASKING:
            return value
        MobileNumber.invalid_masking()

    @validator('end_datetime')
    def is_valid_end_datetime(cls, value, values):
        # print(((value - datetime.now()).total_seconds() / 60), ((value - datetime.now()).total_seconds() / 60) < 30)
        if value and values['start_datetime'] and 'start_datetime' in values and value <= values['start_datetime']:
            MobileNumber.invalid_end_datetime()
        elif value and ((value - datetime.now()).total_seconds() / 60) < CONFIG.get('TIME_INTERVAL', 30):
            MobileNumber.invalid_end_datetime_interval()

        return value

    @validator('start_datetime')
    def is_valid_start_datetime(cls, value, values):
        print(value, type(value))
        if value and value <= datetime.now():
            MobileNumber.invalid_start_datetime()
        return value
