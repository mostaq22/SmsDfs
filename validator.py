import pydantic
import json
# from functools import lru_cache

from exceptions import MobileNumber

MNO_CODE = ["018", "011", "017", "011", "019", "012"]  # Will be Read from env file
MNO_LIST = ['RB', "GP", "BL", "TL", ]


def is_valid_mobile_number(mobile_number: str):
    """
      Rules of validation of a mobile number

      * Length must be 11
      * Start with 01
      * Must be string
      * Must be in MNO CODE [018, 011, 017 etc]
    """
    if type(mobile_number) is not str:
        return MobileNumber.invalid_type()
    elif len(mobile_number) != 11:
        MobileNumber.invalid_length()
    elif not mobile_number.startswith('01'):
        MobileNumber.invalid_prefix()
    elif mobile_number[-11:-8] not in MNO_CODE:
        MobileNumber.invalid_mno_code()
    else:
        return True


def is_valid_mno(mno: str):
    return mno in MNO_LIST or MobileNumber.invalid_mno()


# @lru_cache(maxsize=128)
def read_config():
    with open('app_config.json') as json_file:
        data = json.load(json_file)
        print(data)


if __name__ == '__main__':
    read_config()
