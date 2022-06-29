class SmsResponseCollection:
    __data = None

    def __init__(self, data):
        self.__data = data

    @property
    def data(self):
        if self.__data is not None:
            return {
                "message_id": self.__data.message_id,
                "campaign_id": self.__data.campaign_id,
                "masking": self.__data.masking,
                "msisdn": self.__data.msisdn,
                "status": self.__data.status,
                "mno": self.__data.mno,
                "sms_type": self.__data.sms_type,
                "created_at": str(self.__data.created_at)
            }
