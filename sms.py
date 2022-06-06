from typing import Union
from validator import is_valid_mobile_number, is_valid_mno


class SmsEngine:
    """
    Class Name: SmsEngine
    Description: The SmsEngine class will take some param during class initialization.
        Based on the init params this class will generate & validate some properties like MNO, mobile number etc.
        For future new MNO integration the __mno_list properties will be updated
    params:
        - mobile
        - message
        - mno
    """
    __mobile_number: str
    __message: str
    __mno: Union[str, None] = None
    __mno_list = {
        "GP": ["013", "017"],  # GrameenPhone
        "RB": ["016", "018"],  # Robi 018 - 1320859
        "BL": ["014", "019"],  # Banglalink
    }  # The new MNO will be added based on new integration
    __priority = ('OTP', 'CNF', 'GRL')  # Base on the priority the sms will be disbursed.
    __default_mno = None
    __mno_code: Union[str, None] = None

    def __init__(self, mobile_number: str, message: str, mno: Union[str, None] = None,
                 priority: Union[str, None] = 'GRL'):
        self.__mobile_number = mobile_number
        self.__message = message
        self.__mno = mno
        self.__priority = priority if priority in self.__priority else 'GRL'
        self.is_valid()

    def get_mno_list(self) -> list:
        return list(self.__mno_list.keys())

    """
    The is_valid function is responsible to validate following attributes
    * Mobile number
    * Provided MNO
    """

    # validate class related attributes
    def is_valid(self) -> bool:
        try:
            is_valid_mobile_number(self.__mobile_number)
            is_valid_mno(self.__mno)

            # self.validate_mobile_number()
            # self.validate_mno()
            return True
        except TypeError:
            raise TypeError

    # validate mobile number
    def validate_mobile_number(self) -> bool:
        import re
        pattern = re.compile(r"(^(\+8801|8801|01|008801))[1|3-9]{1}(\d){8}$")

        if re.match(pattern, self.__mobile_number):
            return True
        else:
            raise Exception("Invalid mobile number")

    """
    The validate_mno method is responsible to validate the provided MNO in class initialization.
    * validate MNO
    * set MNO - if validation fails
    * set MNO code from mobile number
    """

    def validate_mno(self) -> bool:
        if self.__mno is not None and self.__mno in self.__mno_list.keys():
            self.__set_mno_code()
            return True
        else:
            self.__set_mno_code()
            self.__set_mno()
            return True

    # set mno for a mobile number if the MNO validation is failed
    def __set_mno(self) -> None:
        for key in self.__mno_list:
            if self.__mno_code in self.__mno_list[key]:
                self.__mno = key

    # set MNO code from provided mobile number
    def __set_mno_code(self) -> None:
        self.__mno_code = self.__mobile_number[-11:-8]

    # get MNO for a mobile number
    @property
    def mno_code(self) -> str:
        return self.__mno_code

    # get MNO for a mobile number
    @property
    def mno(self) -> str:
        return self.__mno

    # get message
    @property
    def message(self) -> str:
        return self.__message

    @property
    def priority(self) -> str:
        return self.__priority

    """
    The send method is responsible for store the data into database
    """

    def send(self) -> dict:
        return {"message": self.__message + " - Stored Successfully"}


sms = SmsEngine(
    mobile_number="01816253638",
    message="Hi!",
    mno='NL',
    priority='OTP'
)
print(
    sms.send(),
    sms.priority,
    sms.mno,
)
