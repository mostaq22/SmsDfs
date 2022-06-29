from datetime import datetime, timedelta
from unittest import TestCase

import pytest

from models.sms import SmsModel, MNO_LIST, DEFAULT_SMS_TYPE, MNO_CODE_LIST


class TestValidation:

    def setup(self) -> None:
        self.sms = {
            "msisdn": "01712972063",
            "message": "MyMessage",
            "mno": "GP",
            "sms_type": "queue",
            "mno_code": "017",
            "campaign_id": "example_campaign",
            "masking": "CITY BANK",
            "start_datetime": None,
            "end_datetime": None,
            "username": "client1",
            "password": "1234"
        }

    def test_msisdn(self):
        # positive
        assert self.sms['msisdn'] == "01712972063"

        # negative assignment
        self.sms['msisdn'] = "01813208359"
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

        # with character
        self.sms['msisdn'] = "018gdhysgey"  # positive
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

        # with numeric
        self.sms['msisdn'] = 178654323456
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

    def test_message(self):
        # positive
        assert self.sms['message'] == "MyMessage"

        # empty string
        self.sms['message'] = ""
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

        # empty string with blank space
        self.sms['message'] = " "
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

    def test_mno(self):
        # default - positive
        assert self.sms['mno'] == "GP"

        # invalid value
        self.sms['mno'] = 'XY'
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

        # valid but empty string
        self.sms['mno'] = ''
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

        # valid but null
        self.sms['mno'] = None
        sms = SmsModel(**self.sms)
        assert sms.mno in MNO_LIST

    def test_sms_type(self):
        # default - positive
        assert self.sms['sms_type'] == "queue"

        # valid but null
        self.sms['sms_type'] = None
        sms = SmsModel(**self.sms)
        assert sms.sms_type == DEFAULT_SMS_TYPE

        # invalid
        self.sms['sms_type'] = "garbage"
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

    def test_mno_code(self):
        # default - positive
        sms = SmsModel(**self.sms)
        assert self.sms['mno_code'] == sms.mno_code

        # valid but null
        self.sms['mno_code'] = None
        sms = SmsModel(**self.sms)
        assert sms.mno_code in MNO_CODE_LIST

        # invalid
        self.sms['mno_code'] = 4848
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

    def test_campaign_id(self):
        # default - positive
        sms = SmsModel(**self.sms)
        assert self.sms['campaign_id'] in sms.campaign_id

        # valid but null
        self.sms['campaign_id'] = None
        sms = SmsModel(**self.sms)
        assert sms.campaign_id == self.sms['campaign_id']

        # invalid
        self.sms['campaign_id'] = 43343  # dummy value
        sms = SmsModel(**self.sms)
        assert sms.campaign_id == str(self.sms['campaign_id'])

    def test_masking(self):
        # default - positive
        sms = SmsModel(**self.sms)
        assert self.sms['masking'] == sms.masking

        # valid but null
        self.sms['masking'] = "garbage"
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

        # integer
        self.sms['masking'] = 23334
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

        # null
        self.sms['masking'] = None
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

    def test_start_datetime(self):
        # default - positive
        sms = SmsModel(**self.sms)
        assert self.sms['start_datetime'] == sms.start_datetime

        # invalid value
        self.sms['start_datetime'] = "garbage_string"
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

        # 10 min prior from current time
        self.sms['start_datetime'] = datetime.now() - timedelta(minutes=10)
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

        # 10 min forward from current time
        self.sms['start_datetime'] = datetime.now() + timedelta(minutes=10)
        sms = SmsModel(**self.sms)
        assert self.sms['start_datetime'] == sms.start_datetime

    def test_end_datetime(self):
        # default assignment
        self.sms["start_datetime"] = None
        sms = SmsModel(**self.sms)
        assert self.sms['end_datetime'] == sms.end_datetime

        # invalid input -> exception output
        invalid_end_datetime = [

            str(datetime.now()),  # valid value but invalid type

            3232324282,  # invalid type

            datetime.now() + timedelta(minutes=10),  # 10 min < 30 min (config) forward from current time

            datetime.now() - timedelta(minutes=10),  # value < current time
        ]
        for invalid in invalid_end_datetime:
            self.sms['end_datetime'] = invalid
            with pytest.raises(ValueError):
                SmsModel(**self.sms)

        # start_datetime > end_datetime
        self.sms["start_datetime"] = datetime.now() + timedelta(minutes=50)
        self.sms['end_datetime'] = datetime.now() + timedelta(minutes=40)
        with pytest.raises(ValueError):
            SmsModel(**self.sms)

    def test_username(self):
        # value assignment
        sms = SmsModel(**self.sms)
        assert self.sms["username"] == sms.username

        # invalid value but casting by function
        self.sms["username"] = 123213
        sms = SmsModel(**self.sms)
        assert str(self.sms["username"]) == sms.username

        for invalid in ['', ' ', None]:
            self.sms['username'] = invalid
            with pytest.raises(ValueError):
                SmsModel(**self.sms)

    def test_password(self):
        # value assignment
        sms = SmsModel(**self.sms)
        assert self.sms["username"] == sms.password

        # invalid value but casting by function
        self.sms["password"] = 123213
        sms = SmsModel(**self.sms)
        assert str(self.sms["password"]) == sms.password

        for invalid in ['', ' ', None]:
            self.sms['password'] = invalid
            with pytest.raises(ValueError):
                SmsModel(**self.sms)
