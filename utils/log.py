import logging
from inspect import getframeinfo, stack
from database import session
from models.log import Log


class AppLog:
    content_type: str
    object_id: str
    log_type: str
    log_details: str
    created_by: str

    def __init__(self, log_details: str, content_type: str = 'APP', created_by: str = 'system', object_id: str = None,
                 log_type: str = 'INFO'):
        """

        :param log_details:
        :param content_type:
        :param created_by:
        :param object_id:
        :param log_type:
        """
        self.content_type = content_type
        self.object_id = object_id
        self.log_type = log_type.upper()
        self.created_by = created_by
        caller = getframeinfo(stack()[1][0])
        self.log_details = f"{caller.filename}: {caller.lineno} \n {log_details}"

    def console(self):
        logging.addLevelName(level=20, levelName=self.log_type)
        logging.basicConfig(level=logging.INFO)
        logging.info(self.log_details)

    def save(self):
        log = {"content_type": self.content_type, "object_id": self.object_id, "log_type": self.log_type,
               "created_by": self.created_by, "log_details": self.log_details}

        session.add(Log(**log))
        session.commit()
        return log
