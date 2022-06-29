from database import Base, session


class MnoBase:
    sms: object

    def update(self):
        sms_map = Base.classes.sms
        sms_obj = session.query(sms_map).get(self.sms.id)
        sms_obj.status = self.sms.status
        sms_obj.message_count = self.sms.message_count
        session.commit()

