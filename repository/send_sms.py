class SmsDispatch:
    sms: object

    def __init__(self, sms: object):
        self.sms = sms

    def send(self):
        self.mno_selection()

    def mno_selection(self):
        if self.sms.mno == 'RB':
            from mno.robi import Robi  # conditional import
            Robi(self.sms).dispatch()
        elif self.sms.mno == 'GP':
            from mno.gp import Gp  # conditional import
            Gp(self.sms).dispatch()
        elif self.sms.mno == 'BL':
            from mno.bl import BanglaLink  # conditional import
            BanglaLink(self.sms).dispatch()
        else:
            print("Fallback")
