import json
from mno.base import MnoBase
from app_config import get_config
import requests
import xmltodict

from utils.log import AppLog


class Robi(MnoBase):

    def __init__(self, sms: object):
        self.sms = sms
        # print(self.sms.msisdn)

    def dispatch(self):
        robi = get_config('API_CREDENTIALS')['RB']
        base_url = robi['base_url']
        payloads = {
            "Username": robi['username'],
            "Password": robi['password'],
            "From": self.sms.masking,
            "To": self.sms.msisdn,
            "Message": self.sms.message
        }
        response = requests.get(base_url + "/SendTextMessage", params=payloads)
        response_json_string = json.dumps(xmltodict.parse(response.text))
        AppLog(log_details=response_json_string).save()
        response_dict = json.loads(response_json_string)
        self.sms.status = 'delivered' if response_dict["ArrayOfServiceClass"]["ServiceClass"][
                                             "Status"] == '0' else 'failed'
        self.sms.message_count = response_dict["ArrayOfServiceClass"]["ServiceClass"]["SMSCount"]
        self.update()


"""
Sample Error Response
{'ArrayOfServiceClass': {'ServiceClass': {'MessageId': '0', 'Status': '-1', 'StatusText': 'Error occurred', 'ErrorCode': '1504', 'ErrorText': 'auth_fail', 'SMSCount': '1', 'CurrentCredit': '0'}}}


Sample Success Response

{'ArrayOfServiceClass': {'ServiceClass': {'MessageId': '1655716911004748', 'Status': '0', 'StatusText': 'success', 'ErrorCode': '0', 'ErrorText': None, 'SMSCount': '1', 'CurrentCredit': '104991.27'}}}

"""
