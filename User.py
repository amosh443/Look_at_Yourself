import database as db
import datetime as dt

class User:
    def __init__(self, time_diff=0, chat_id=0, login='', reg_stage=0, start = dt.datetime.utcnow()):
        self.time_diff = time_diff
        self.chat_id = chat_id
        self.login = login
        self.stage = reg_stage  # 0 - set timezone, 1 - configure notifications
        self.start = start.replace(hour=0, minute=0, microsecond=0)
        self.times = [[10, 00], [16, 30], [21, 30]]
        self.done = ''
        for i in range(44):
            self.done += '0'

    def next_stage(self):
        self.stage = self.stage + 1

    def list(self):
        return [self.time_diff, self.chat_id, self.login, self.stage, self.start]


def from_list(list):
    return User(list[0], list[1], list[2], list[3], dt.datetime.strptime(list[4], '%Y-%m-%d %H:%M:%S'))
