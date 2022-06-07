def generate_mno_list(mno_list: list) -> list:
    """
    This function will loop through the mno_list & generate a concatenated list

    :param mno_list:
    :return: list
    """
    temp_list = []
    for code in mno_list:
        temp_list = temp_list + code
    return temp_list


def get_mno_by_code(mno_code: str, mno_data: dict) -> str:
    """
    This function will take following params and loop through the mno list.

    :param mno_code:
    :param mno_data:
    :return: string
    """
    try:
        for key in list(mno_data.keys()):
            if mno_code in mno_data[key]:
                return key
    except ValueError:
        raise ValueError("Params are not not valid")
