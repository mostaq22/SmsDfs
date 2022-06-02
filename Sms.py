from typing import Union

"""
class name: SmsEngine
description: This class is responsible for initiate the sms.
    - validate mobile number
    - validate mno
    - set mno (mobile network operator)
    - store to db
"""


class SmsEngine:
    _mobile_number: str
    _message: str
    _mno: Union[str, None] = None
    _mno_list = ("GP", "ROBI", "BL", 'SSL')  # The new MNO will be added based on new integration
    _priority = ('OTP', 'CONFIRM', 'GENERAL')  # Base on the priority the sms will be disbursed
    _default_mno = None

    def __init__(self, mobile_number: str, message: str, mno: Union[str, None] = None):
        self._mobile_number = mobile_number
        self._message = message
        self._mno = mno
        self.is_valid()

    def get_mno_list(self):
        return self._mno_list

    # validate class related attributes
    def is_valid(self) -> bool:
        if self.validate_mobile_number():
            print("Next")
        else:
            print("Mobile number wrong")
            return False
        # self.validate_mno()

    # validate mobile number
    def validate_mobile_number(self) -> bool:
        print("validate_mobile_number")
        return True

    # validate mno
    def validate_mno(self) -> bool:
        print("validate_mno")
        return True

    # set mno for a mobile number if the MNO validation is failed
    def set_mno(self):
        pass

    # get MNO for a mobile number
    def get_mno(self) -> str:
        return self._default_mno


sms = SmsEngine(
    mobile_number="01813208359",
    message="Hi!"
)
