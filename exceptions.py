class MobileNumber:
    """
    Class Name: Mobile
    Description: This Mobile class is responsible for handling the exception message of mobile number validation.

    * length() - ValueError - Mobile number length isn't correct
    * prefix() - ValueError - Mobile number prefix isn't correct (prefix is 01)
    * type() - TypeError - Given mobile number type is not correct (string required)
    * mno() - ValueError - MNO code isn't correct as per given mobile number
    """

    @staticmethod
    def invalid_length():
        raise ValueError("Mobile number length must be 11")

    @staticmethod
    def invalid_prefix():
        raise ValueError("Mobile number must be start with 01")

    @staticmethod
    def invalid_mno_code():
        raise ValueError("Invalid MNO code")

    @staticmethod
    def invalid_mno():
        raise ValueError("Invalid MNO name")

    @staticmethod
    def invalid_message():
        raise ValueError("Invalid message body")

    @staticmethod
    def invalid_priority():
        raise ValueError("Invalid priority")
