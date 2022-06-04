from typing import Union


class SmsEngine:
    __mobile_number: str
    __message: str
    __mno: Union[str, None] = None
    __mno_list = {
        "GP": ["013", "017"],  # GrameenPhone
        "RB": ["016", "018"],  # Robi 018 - 1320859
        "BL": ["014", "019"],  # Banglalink
        "SS": []
    }  # The new MNO will be added based on new integration
    __priority = ('OTP', 'CNF', 'GRL')  # Base on the priority the sms will be disbursed.
    __default_mno = None
    __operator_code: Union[str, None] = None
    MOBILE_NUMBER_LENGTH = 11

    def __init__(self, mobile_number: str, message: str, mno: Union[str, None] = None,
                 priority: Union[str, None] = 'GRL'):
        self.__mobile_number = mobile_number
        self.__message = message
        self.__mno = mno
        self.__priority = priority
        self.is_valid()

        self.__operator_code = self.__mobile_number[:2]

    def get_mno_list(self):
        return self.__mno_list.keys()

    # validate class related attributes
    def is_valid(self) -> bool:
        try:
            self.validate_mobile_number()
            # self.validate_mno()
            return True
        except TypeError:
            raise TypeError

    # validate mobile number
    def validate_mobile_number(self) -> bool:
        import re
        pattern = re.compile(r"(^(\+8801|8801|01|008801))[1|3-9]{1}(\d){8}$")

        if re.match(pattern, self.__mobile_number):
            self.__operator_code = self.__mobile_number[-11:-8]
            return True
        else:
            raise Exception("Invalid mobile number")

    # validate mno
    def validate_mno(self) -> bool:
        if self.__mno in self.__mno_list.keys():
            return True
        else:
            self.__set_mno()

    def setup_mno(self):
        pass

    # set mno for a mobile number if the MNO validation is failed
    def __set_mno(self) -> None:
        for mno, number in self.__mno_list:
            self.__mno = mno if self.__operator_code in number else None


    # get MNO for a mobile number
    @property
    def get_mno(self) -> str:
        return self.__mno

    # get message
    @property
    def get_message(self) -> str:
        return self.__message

    @property
    def get_priority(self) -> str:
        return self.__priority

    """
    The send method is responsible for store the data into database
    """

    def send(self) -> dict:
        return {"message": self.__message + " - Stored Successfully"}


sms = SmsEngine(
    mobile_number="+8801716253638",
    message="Hi!",
    mno='NL',
    priority='SSS'
)
print(
    sms.send(),
    sms.get_priority,
    sms.get_mno,
)
