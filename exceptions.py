class MobileNumber:
    """
    Class Name: Mobile
    Description: This Mobile class is responsible for handling the exception message of mobile number validation.

    * invalid_length() - ValueError - Mobile number length isn't correct
    * invalid_prefix() - ValueError - Mobile number prefix isn't correct (prefix is 01)
    * type() - TypeError - Given mobile number type is not correct (string required)
    * invalid_mno_code() - ValueError - MNO code (018,017 etc isn't correct as per given mobile number
    * invalid_mno() - ValueError - MNO name isn't correct as per given mobile number
    """

    @staticmethod
    def invalid_msisdn():
        raise ValueError("Invalid msisdn")

    @staticmethod
    def invalid_length():
        raise ValueError("MSISDN length must be 11")

    @staticmethod
    def invalid_prefix():
        raise ValueError("MSISDN must be start with 01")

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
    def invalid_sms_type():
        raise ValueError("Invalid sms type")

    @staticmethod
    def invalid_masking():
        raise ValueError("Invalid masking")

    @staticmethod
    def invalid_end_datetime():
        raise ValueError("Invalid end_datetime value")

    @staticmethod
    def invalid_end_datetime_interval():
        raise ValueError("Interval between current & end datetime less than 30 min")

    @staticmethod
    def invalid_start_datetime():
        raise ValueError("Value must be greater than current datetime")
