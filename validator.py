"""
MobileNumber is a validation class which will validate a give mobile number
min length: 11
type: string
starts with
    - 016, 018 -> Robi
    - 013, 017 -> Grameenphone,
    - 014, 019 -> Banglalink
    - 015 -> TeleTalk,
    - 011 -> CityCell
"""


class MobileNumber:

    def __init__(self, mobile_number: str):
        pass
