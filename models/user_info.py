from datetime import datetime


class UserInfo:
    def __init__(self):
        pass

    def __init__(self, temp):
        self.unix_secs = datetime.utcfromtimestamp(temp[0])
        self.sys_up_time = datetime.utcfromtimestamp(temp[1])
        self.dpkts = temp[2]
        self.doctate = temp[3]
        # self.doctate_dkpts = temp[4]
        self.rfp = datetime.utcfromtimestamp(temp[5] / 1000)
        self.rep = datetime.utcfromtimestamp(temp[6] / 1000)
        # self.first = temp[7]
        # self.last = temp[8]
        self.duration = temp[9]
        self.oct_duration = self.doctate / self.duration

    unix_secs = datetime.utcfromtimestamp(0)
    sys_up_time = datetime.utcfromtimestamp(0)
    dpkts = 0
    doctate =  0
    # doctate_dkpts = 0
    rfp = datetime.utcfromtimestamp(0)
    rep = datetime.utcfromtimestamp(0)
    # first = 0
    # last = 0
    duration = 0
    oct_duration = 0.0

