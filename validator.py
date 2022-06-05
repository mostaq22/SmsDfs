"""
Rules of validation of a mobile number

* Length must be 11
* Start with 01
* Must be string
* Must be in MNO CODE [018, 011, 017 etc]
"""


def is_valid_mobile_number(mobile_number: str):
    print(mobile_number, type(mobile_number))
    if mobile_number.startswith('01') and len(mobile_number):
        pass
    elif mobile_number[:]:
        pass


if __name__ == '__main__':
    is_valid_mobile_number(71813208359)
