import Programme
import database as db
import datetime as dt

f = open('texts', 'r', encoding="utf8")
nots = f.read().split(sep='__')
day = 1
hour = 0
num = 0
prg = 0
type = 0

for nt in nots:
    text = ''
    strs = nt.split(sep='\n')
    while '' in strs:
        strs.remove('')
    while ' ' in strs:
        strs.remove(' ')
    if len(strs) is 0:
        continue

    for str in strs:
        nums = [int(s) for s in str.split() if s.isdigit()]
        # if 'Программа тренинга' in str:
        # prg = 1
        if ':00' in str:
            x = str.find(':00')
            hour = int(str[x - 2:x]) + 1
            type = 1
        elif 'настраиваемое' in str:
            type = 0
            if 'ервое' in str:
                num = 0
            if 'торое' in str:
                num = 1
            if 'ретье' in str:
                num = 2
        elif 'День' in str:
            x = str.find('День')
            day = nums[0]
        elif not 'Промежуточное' in str and not 'Элемент картины' in str and not 'Файл' in str and not 'файл' in str \
                and not 'Изображение' in str:
            text += str+'\n'
    if len(text) > len('Второе настраиваемое сообщение: '):
        db.add_event(Programme.Event(text, None, type, num, dt.datetime.utcnow().replace(year=day, hour=hour, minute=0)))

    # print(strs)

# print(nots)
