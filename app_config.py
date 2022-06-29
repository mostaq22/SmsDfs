import json
from os.path import join, dirname


def get_config(key: [str, list, None] = None) -> dict:
    """
    This function will receive a key as string or list or None.

    :param key: str/list/None
    :return: dict
    """
    file_path = join(dirname(__file__), 'app_config.json')
    with open(file_path) as json_file:
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
