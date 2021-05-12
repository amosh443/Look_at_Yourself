import database as db
import datetime as dt

class User:
    def __init__(self, time_diff=0, chat_id=0, login='', reg_stage=0, start = dt.datetime.utcnow(), weeks_paid = 0, events_picked = '111'):
        self.time_diff = time_diff
        self.chat_id = chat_id
        self.login = login
        self.stage = reg_stage  # 0 - set timezone, 1 - configure notifications
        self.start = start.replace(hour=0, minute=0, microsecond=0)
        self.times = [[8, 0], [13, 0], [22, 0]]
        self.done = ''
        self.weeks_paid = weeks_paid
        self.events_picked = str(events_picked)
        for i in range(44):
            self.done += '0'

    def next_stage(self):
        self.stage = self.stage + 1

    def list(self):
        return [self.time_diff, self.chat_id, self.login, self.stage, self.start, self.weeks_paid, self.events_picked]


def from_list(list):
    return User(list[0], list[1], list[2], list[3], dt.datetime.strptime(list[4], '%Y-%m-%d %H:%M:%S'), list[5], list[6])
