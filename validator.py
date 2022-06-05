MNO_CODE = ["018", "011", "017", "011", "019", "012"]  # Will be Read from env file

"""
Rules of validation of a mobile number

* Length must be 11
* Start with 01
* Must be string
* Must be in MNO CODE [018, 011, 017 etc]
"""


def is_valid_mobile_number(mobile_number: str):
    if len(mobile_number) != 11:
        print("length is not 11")
    elif not mobile_number.startswith('01'):
        print("not start with 01")
    elif not type(mobile_number) is str:
        print("not string")
    elif mobile_number[-11:-8] in MNO_CODE:
        print("MNO code invalid")


# try:
#     if len(mobile_number) == 11 and \
#             mobile_number.startswith('01') and \
#             type(mobile_number) is str and \
#             mobile_number[-11:-8] in MNO_CODE:
#         return True
# finally:
#     raise Exception("Mobile number is not valid")


if __name__ == '__main__':
    is_valid_mobile_number('')
