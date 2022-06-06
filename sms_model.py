from typing import Union, Optional
from pydantic import BaseModel, validator
from exceptions import MobileNumber

MNO_CODE = ["018", "011", "017", "011", "019", "012"]  # Will be Read from env file
MNO_LIST = ['RB', "GP", "BL", "TL", ]
PRIORITY = ['OTP', 'CNF', 'GRL']
DEFAULT_PRIORITY = 'GRL'


class SmsModel(BaseModel):
    msisdn: str
    message: str
    mno: Union[str, None]
    priority: Union[str, None] = 'GRL'  # GRL - General. If priority is None
    mno_code: Union[str] = None

    @validator('msisdn')
    def is_valid_mobile_number(cls, value):
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
        elif value[-11:-8] not in MNO_CODE:
            MobileNumber.invalid_mno_code()
        else:
            return value

    @validator('mno')
    def is_valid_mno(cls, value, values):
        print(value)
        if value and value in MNO_LIST:
            return value
        elif len(value) < 1:
            return values['msisdn'][-11:-8]
        MobileNumber.invalid_mno()

    @validator('message')
    def is_valid_message(cls, value):
        if len(value.strip()) > 0:
            return value
        MobileNumber.invalid_message()

    @validator('priority')
    def is_valid_priority(cls, value):
        if value in PRIORITY:
            return value
        MobileNumber.invalid_priority()

    @validator('mno_code')
    def is_valid_mno_code(cls, value):
        if value and value in MNO_CODE:
            return value
        return MobileNumber.invalid_mno_code()


#
# data = {
#     "msisdn": "01813208359",
#     "message": " ",
#     "mno": "Ud",
#     "priority": "OTP"
# }
#
# try:
#     sms = SmsModel(**data)
# except ValidationError as e:
#     print(e)
print("sms_model")
