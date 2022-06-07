from pydantic import BaseModel, validator
from exceptions import MobileNumber
from app_config import get_config
from utils import generate_mno_list, get_mno_by_code

# Get all config related to sms class
CONFIG = get_config(['MNO', 'PRIORITY', 'DEFAULT_PRIORITY'])  # required values for sms_model
MNO_CODE_LIST = generate_mno_list(list(CONFIG.get('MNO').values()))  # list of mno code - 018, 017 etc
MNO_LIST = list(CONFIG.get('MNO').keys())  # list mno RB, GP etc
PRIORITY = CONFIG.get('PRIORITY', None)  # get priority of sms - OTO, CNF etc
DEFAULT_PRIORITY = CONFIG.get('DEFAULT_PRIORITY', None)  # get default priority of sms - GRL


class SmsModel(BaseModel):
    msisdn: str
    message: str
    mno: str
    priority: str = DEFAULT_PRIORITY  # GRL - General. If priority is None
    mno_code: str

    @validator('msisdn')
    def is_valid_mobile_number(cls, value, **kwargs):
        """
          Rules of validation of a mobile number

          * Length must be 11
          * Start with 01
          * Must be string
          * Must be in MNO CODE [018, 011, 017 etc]
        """
        if len(value) != 11:
            MobileNumber.invalid_length()
        elif not value.startswith('01'):
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
        elif len(value) < 1 and 'msisdn' in values:
            return get_mno_by_code(mno_code=values['msisdn'][-11:-8], mno_data=CONFIG.get('MNO'))
        MobileNumber.invalid_mno()

    @validator('message')
    def is_valid_message(cls, value):
        """
        Validate the message from payload. Length must be more than zero

        :param value:
        :return:
        """
        if len(value.strip()) > 0:
            return value
        MobileNumber.invalid_message()

    @validator('priority')
    def is_valid_priority(cls, value):
        """
        Validate the priority from payload. If empty then set to default priority.

        :param value:
        :return:
        """
        if len(value.strip()) < 1:
            return DEFAULT_PRIORITY
        if len(value.strip()) > 0 and value in PRIORITY:
            return value
        MobileNumber.invalid_priority()

    @validator('mno_code')
    def is_valid_mno_code(cls, value, values):
        if value and value in MNO_CODE_LIST and values['msisdn'][-11:-8] == value:
            return value
        elif len(value) < 1 and 'msisdn' in values:
            return values['msisdn'][-11:-8]
        return MobileNumber.invalid_mno_code()
