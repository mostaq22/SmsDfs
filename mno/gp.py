from mno.base import MnoBase
from app_config import get_config
import requests


class Gp(MnoBase):

    def __init__(self, sms: object):
        self.sms = sms
        # print(self.sms.msisdn)

    def dispatch(self):
        gp = get_config('API_CREDENTIALS')['GP']
        base_url = gp['base_url']
        payloads = {
            "username": gp['username'],
            "password": gp['password'],
            "apicode": "1",
            "msisdn": self.sms.msisdn,
            "message": self.sms.message,
            "cli": self.sms.masking,
            "messageid": 0,
            "messagetype": "1",
            "countrycode": "880",
        }
        headers = {'Content-type': 'application/json'}
        response = requests.post(base_url, json=payloads, headers=headers)
        response_data = response.json()

        self.sms.status = 'delivered' if response_data[
                                             'statusCode'] == 200 and response.status_code == 200 else 'failed'
        self.sms.message_count = 1
        self.update()


"""
Success response
{"statusCode":"200","message":"20220620-7145-300392114770-01309920095-02"}

Error response
{"statusCode":"210","message":"Parameter Mismatch"}
"""
