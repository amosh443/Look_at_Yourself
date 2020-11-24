import datetime as dt


class Message:
    def __init__(self, login='', text='', attachment='', datetime=dt.datetime.utcnow(), id_=''):
        self.login = login
        self.text = text
        self.attachment = attachment
        self.datetime = datetime.replace(microsecond=0)
        self.id = id

    def list(self):
        return [self.login, self.text, self.attachment, self.datetime]


def from_list(list):
    return Message(list[0], list[1], list[4], dt.datetime.strptime(list[3], '%Y-%m-%d %H:%M:%S'))
