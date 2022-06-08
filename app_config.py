import json


def get_config(key: [str, list, None] = None) -> dict:
    """
    This function will receive a key as string or list or None.

    :param key: str/list/None
    :return: dict
    """
    with open('app_config.json') as json_file:
        data = json.load(json_file)
        if key is None:
            return data
        elif type(key) is str:
            return data.get(key, None)
        elif type(key) is list:
            temp_data = {}
            for k in key:
                temp_data[k] = data.get(k, None)
            return temp_data
