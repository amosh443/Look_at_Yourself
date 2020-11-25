import datetime as dt
import database as db


class Event:
    # attachment = document.file_id
    def __init__(self, text='sample', attachment='', type=-1, number=0, datetime=dt.datetime.utcnow(), id_=0):
        # types: 0 - Настраиваемое напоминание, 1 - Промежуточное напоминание, 2 - Другое сообщение
        self.text = text
        self.attachment = attachment
        self.datetime = datetime.replace(microsecond=0)
        self.type = type
        self.number = number
        self.id_ = id_
        self.day=datetime.year

    def list(self):
        return [self.text, self.attachment, self.type, self.datetime, self.number, self.id_]

    def fresh_list(self):
        return [self.text, self.attachment, self.type, self.datetime, self.number]

def from_list(list):
    #print(str(list[1]))
    return Event(list[1], list[2], list[4], list[5], dt.datetime.strptime(list[3], '%Y-%m-%d %H:%M:%S'), list[0])
