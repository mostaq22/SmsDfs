from mno.base import MnoBase
from app_config import get_config
import requests


class BanglaLink(MnoBase):

    def __init__(self, sms: object):
        self.sms = sms

    def dispatch(self):
        bl = get_config('API_CREDENTIALS')['BL']
        base_url = bl['base_url']
        payloads = {
            "userID": bl['username'],
            "passwd": bl['password'],
            "msisdn": self.sms.msisdn,
            "message": self.sms.message,
            "sender": self.sms.masking,
        }
        response = requests.get(base_url + "/sendSMS/sendSMS", params=payloads)
        processed_response = response_processor(response=response.text)
        if processed_response:
            self.sms.message_count = processed_response.get('message_count')
            self.sms.status = 'delivered'
            self.update()


def response_processor(response: str = None):
    if response:
        data = response.split("and")
        if len(data) == 2:
            first_part = data[0].strip()[-1]
            second_part = data[1].strip()[-1]
            if int(first_part) > 0 and int(second_part) == 0:
                return {'message_count': first_part}
            else:
                return False
    else:
        return False


"""
Success response
200 Success Count : 1 and Fail Count : 0

Error response
200 Sorry you send wrong password
"""
